"""Pipeline entry point: orchestrates ingestion, embedding, retrieval and evaluation.

Usage (from the starter/ directory):
    python -m src.run

Strategies:
    A: Fixed-size chunking (500 chars, overlap 50), no metadata filter
    B: Paragraph-aware chunking (max 600 chars), no metadata filter
    C: Same as B, with metadata filter applied for filter-annotated questions

Vector store: ChromaDB (persistent local, no Docker required)
Embedding model: paraphrase-multilingual-MiniLM-L12-v2 (local, 384 dims)
"""
import json
import time
import csv
from pathlib import Path
from datetime import datetime

# ── Project paths ─────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]        # project root
STARTER = Path(__file__).resolve().parents[1]     # starter/
DATA_DIR = ROOT / "data"
BENCHMARK_DIR = ROOT / "benchmark"
RESULTS_DIR = STARTER / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

CORPUS_PDF = DATA_DIR / "handbook_sv_2025.pdf"
CORPUS_JSON = DATA_DIR / "handbook_sv_2025.json"
QUESTIONS_FILE = BENCHMARK_DIR / "questions.json"
DOCUMENT_ID = "handbook_sv_2025"
SOURCE = "data/handbook_sv_2025.pdf"  # canonical source reference (PDF)

# ── Chunking config ────────────────────────────────────────────
STRATEGY_A_SIZE = 500
STRATEGY_A_OVERLAP = 50
STRATEGY_BC_MAX_SIZE = 600


def load_questions() -> list[dict]:
    with open(QUESTIONS_FILE, encoding="utf-8") as f:
        return json.load(f)


def run_pipeline():
    print("=" * 60)
    print("DAY 06 · DATA INGESTION LAB — Pipeline Run")
    print(f"Started at: {datetime.now().isoformat()}")
    print("=" * 60)

    # ── Step 1: Load embedder (shared across all strategies) ───
    from .embeddings import MyEmbedder
    embedder = MyEmbedder()
    print(f"\n[Config] Embedding model : {embedder.model_name}")
    print(f"[Config] Dimensions      : {embedder.dimensions}")

    # ── Step 2: Initialize vector store ───────────────────────
    from .store import ChromaVectorStore
    store = ChromaVectorStore(dimensions=embedder.dimensions)
    store.create_schema()

    # ── Step 3: Ingest corpus ──────────────────────────────────
    from .ingestion import load_json, load_pdf
    print(f"\n[Corpus] Loading JSON corpus: {CORPUS_JSON}")
    print(f"[Corpus] (PDF: {CORPUS_PDF} — human-readable; text extraction from JSON for clean UTF-8)")
    t0 = time.time()
    pages = load_json(CORPUS_JSON, DOCUMENT_ID, SOURCE)
    ingest_time = time.time() - t0
    print(f"[Corpus] Loaded {len(pages)} pages in {ingest_time:.2f}s")

    # Validate minimum 30 content pages
    if len(pages) < 30:
        raise ValueError(
            f"[ERROR] Only {len(pages)} pages found. Lab requires at least 30 content pages!"
        )

    # ── Step 4: Build 3 chunking strategies ───────────────────
    from .chunking import fixed_size, by_paragraph

    strategies = {}

    print("\n── Strategy A: Fixed-size (500 chars, overlap 50) ──")
    t_a = time.time()
    all_chunks_a = []
    for page in pages:
        all_chunks_a.extend(fixed_size(page, size=STRATEGY_A_SIZE, overlap=STRATEGY_A_OVERLAP))
    t_a = time.time() - t_a
    strategies["A"] = {
        "name": "Fixed-size 500/50",
        "chunks": all_chunks_a,
        "ingest_time_s": round(t_a, 3),
        "config": {"chunking": "fixed_size", "chunk_size": STRATEGY_A_SIZE, "overlap": STRATEGY_A_OVERLAP},
    }

    print("\n── Strategy B: Paragraph-aware (max 600 chars) ──")
    t_b = time.time()
    all_chunks_b = []
    for page in pages:
        all_chunks_b.extend(by_paragraph(page, max_size=STRATEGY_BC_MAX_SIZE))
    t_b = time.time() - t_b
    strategies["B"] = {
        "name": "Paragraph max-600",
        "chunks": all_chunks_b,
        "ingest_time_s": round(t_b, 3),
        "config": {"chunking": "by_paragraph", "chunk_size": STRATEGY_BC_MAX_SIZE, "overlap": 0},
    }

    print("\n── Strategy C: Paragraph-aware + metadata filter ──")
    # Strategy C uses same chunks as B; filter is applied at query time
    strategies["C"] = {
        "name": "Paragraph max-600 + metadata filter",
        "chunks": all_chunks_b,  # same chunks as B
        "ingest_time_s": round(t_b, 3),
        "config": {"chunking": "by_paragraph", "chunk_size": STRATEGY_BC_MAX_SIZE, "overlap": 0, "filter": True},
    }

    # Print chunk statistics
    for strat_id, strat in strategies.items():
        chunks = strat["chunks"]
        lengths = [len(c.text) for c in chunks]
        print(f"\n[{strat_id}] chunks={len(chunks)}, "
              f"avg_len={sum(lengths)/len(lengths):.0f}, "
              f"min={min(lengths)}, max={max(lengths)}")

    # ── Step 5: Embed and store ────────────────────────────────
    print("\n── Embedding and storing chunks ──")
    embed_times = {}

    for strat_id in ["A", "B"]:  # C uses same as B
        strat = strategies[strat_id]
        chunks = strat["chunks"]
        texts = [c.text for c in chunks]
        print(f"\n[{strat_id}] Embedding {len(chunks)} chunks...")
        t_embed = time.time()
        vectors = embedder.embed_documents(texts)
        t_embed = time.time() - t_embed
        embed_times[strat_id] = t_embed
        print(f"[{strat_id}] Embedded in {t_embed:.2f}s")

        # Clean re-ingest (delete existing to avoid duplicates)
        store.delete_strategy(strat_id)
        store.upsert(strat_id, chunks, vectors)

    # C uses same chunks+vectors as B
    store.delete_strategy("C")
    store.upsert("C", strategies["B"]["chunks"],
                  embedder.embed_documents([c.text for c in strategies["B"]["chunks"]]))
    embed_times["C"] = embed_times["B"]

    # ── Step 6: Load benchmark questions ──────────────────────
    questions = load_questions()
    dev_qs = [q for q in questions if q["split"] == "dev"]
    test_qs = [q for q in questions if q["split"] == "test"]
    print(f"\n[Benchmark] Loaded {len(questions)} questions: {len(dev_qs)} dev / {len(test_qs)} test")
    assert len(dev_qs) >= 15, f"Need at least 15 dev questions, got {len(dev_qs)}"
    assert len(test_qs) >= 5, f"Need at least 5 test questions, got {len(test_qs)}"

    # ── Step 7: Retrieval + Evaluation ────────────────────────
    from .evaluation import evaluate_query, summarize

    all_traces = {}  # strategy -> split -> list of traces
    all_summaries = {}

    for strat_id in ["A", "B", "C"]:
        print(f"\n── Evaluating Strategy {strat_id} ──")
        strat_traces = []

        for question in questions:
            query_vector = embedder.embed_query(question["question"])

            # Strategy C applies metadata filters when question has them
            if strat_id == "C" and question.get("filter"):
                filters = question["filter"]
            else:
                filters = None

            hits = store.search(strat_id, query_vector, top_k=3, filters=filters)
            trace = evaluate_query(question, hits)
            trace["strategy"] = strat_id
            strat_traces.append(trace)

        all_traces[strat_id] = strat_traces
        summary = summarize(strat_traces)
        all_summaries[strat_id] = summary

        # Print summary
        for split_name in ["dev", "test", "overall"]:
            if split_name in summary:
                s = summary[split_name]
                print(f"  [{strat_id}][{split_name}] "
                      f"Hit@1={s['hit_at_1_count']}/{s['total_questions']} "
                      f"({s['hit_at_1_rate']*100:.1f}%)  "
                      f"Hit@3={s['hit_at_3_count']}/{s['total_questions']} "
                      f"({s['hit_at_3_rate']*100:.1f}%)")

    # ── Step 8: Save all results ───────────────────────────────
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save full traces
    trace_file = RESULTS_DIR / f"traces_{timestamp}.json"
    with open(trace_file, "w", encoding="utf-8") as f:
        json.dump(all_traces, f, ensure_ascii=False, indent=2)
    print(f"\n[Output] Traces saved → {trace_file}")

    # Save summaries
    summary_file = RESULTS_DIR / f"summaries_{timestamp}.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(all_summaries, f, ensure_ascii=False, indent=2)
    print(f"[Output] Summaries saved → {summary_file}")

    # Save experiment log CSV
    _write_experiment_log(strategies, all_summaries, embed_times, timestamp)

    # Save chunk stats
    _write_chunk_stats(strategies, timestamp)

    print("\n" + "=" * 60)
    print("Pipeline complete!")
    print("=" * 60)
    _print_results_table(all_summaries)


def _write_experiment_log(strategies, summaries, embed_times, timestamp):
    log_path = ROOT / "artifacts" / "experiment_log.csv"
    rows = []
    config_map = {
        "A": ("fixed_size", 500, 50, "source+page", "none", "paraphrase-multilingual-MiniLM-L12-v2",
              "Fixed-size thường tiết kiệm chunk, dễ so sánh baseline"),
        "B": ("by_paragraph", 600, 0, "source+page+section", "none", "paraphrase-multilingual-MiniLM-L12-v2",
              "Paragraph giữ trọn ý tốt hơn fixed-size"),
        "C": ("by_paragraph", 600, 0, "source+page+section", "section_filter", "paraphrase-multilingual-MiniLM-L12-v2",
              "Paragraph + filter metadata giúp thu hẹp không gian tìm kiếm"),
    }
    for strat_id, (chunking, size, overlap, meta, flt, model, hyp) in config_map.items():
        s_all = summaries.get(strat_id, {})
        dev = s_all.get("dev", {})
        test = s_all.get("test", {})
        rows.append({
            "strategy": strat_id,
            "chunking": chunking,
            "chunk_size": size,
            "overlap": overlap,
            "metadata": meta,
            "filter": flt,
            "vectorizer": model,
            "hypothesis": hyp,
            "dev_hit1": f"{dev.get('hit_at_1_count', 0)}/{dev.get('total_questions', 0)}",
            "dev_hit3": f"{dev.get('hit_at_3_count', 0)}/{dev.get('total_questions', 0)}",
            "test_hit1": f"{test.get('hit_at_1_count', 0)}/{test.get('total_questions', 0)}",
            "test_hit3": f"{test.get('hit_at_3_count', 0)}/{test.get('total_questions', 0)}",
            "notes": f"embed_time={embed_times.get(strat_id, 0):.1f}s",
        })

    with open(log_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"[Output] Experiment log → {log_path}")


def _write_chunk_stats(strategies, timestamp):
    stats_file = RESULTS_DIR / f"chunk_stats_{timestamp}.json"
    out = {}
    for strat_id in ["A", "B", "C"]:
        strat = strategies[strat_id]
        chunks = strat["chunks"]
        lengths = [len(c.text) for c in chunks]
        out[strat_id] = {
            "config": strat["config"],
            "chunk_count": len(chunks),
            "avg_chars": round(sum(lengths) / len(lengths), 1) if lengths else 0,
            "min_chars": min(lengths) if lengths else 0,
            "max_chars": max(lengths) if lengths else 0,
            "ingest_time_s": strat["ingest_time_s"],
            "cost_usd": 0.0,  # local model, no cost
        }
    with open(stats_file, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"[Output] Chunk stats → {stats_file}")


def _print_results_table(summaries):
    print("\n📊 RESULTS SUMMARY TABLE")
    print("-" * 70)
    print(f"{'Strategy':<10} {'Split':<8} {'Hit@1':>10} {'Hit@3':>10}")
    print("-" * 70)
    for strat_id in ["A", "B", "C"]:
        s = summaries.get(strat_id, {})
        for split in ["dev", "test"]:
            sp = s.get(split, {})
            if sp:
                h1 = f"{sp['hit_at_1_count']}/{sp['total_questions']} ({sp['hit_at_1_rate']*100:.0f}%)"
                h3 = f"{sp['hit_at_3_count']}/{sp['total_questions']} ({sp['hit_at_3_rate']*100:.0f}%)"
                print(f"  {strat_id:<8} {split:<8} {h1:>10} {h3:>10}")
    print("-" * 70)


def main() -> None:
    run_pipeline()


if __name__ == "__main__":
    main()
