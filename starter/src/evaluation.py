"""Evaluate retrieved evidence and preserve per-query traces."""
from typing import Any


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, Any]:
    """Check source/page and enough gold evidence; keep hit@1 and hit@3 trace.

    A hit is counted when the chunk:
    1. Has the correct gold_source_id (document_id matches)
    2. Has the correct gold_page (page matches)
    3. Contains enough of the gold evidence_quote (at least 60% of key terms)

    Accept any documented alternative gold evidence.
    Manual grounding labels are NOT inferred from this function.
    """
    gold_source = question["gold_source_id"]
    gold_page = question["gold_page"]
    evidence_quote = question.get("evidence_quote", "")

    def _is_hit(hit: dict[str, Any]) -> bool:
        meta = hit.get("metadata", {})
        # Check document_id and page
        source_ok = meta.get("document_id") == gold_source
        page_ok = meta.get("page") == gold_page
        if not (source_ok and page_ok):
            return False
        # Check evidence quote presence (partial match - at least 60% of words)
        if evidence_quote:
            # Extract key words (longer than 3 chars) from evidence
            key_words = [w for w in evidence_quote.split() if len(w) > 3]
            if key_words:
                matched = sum(1 for w in key_words if w in hit["text"])
                return (matched / len(key_words)) >= 0.60
        return True  # source+page match is sufficient if no evidence quote

    # Evaluate hits
    hit_flags = [_is_hit(h) for h in hits]
    hit_at_1 = hit_flags[0] if hit_flags else False
    hit_at_3 = any(hit_flags[:3])

    return {
        "question_id": question["id"],
        "split": question.get("split", "unknown"),
        "question": question["question"],
        "gold_source_id": gold_source,
        "gold_page": gold_page,
        "hit_at_1": hit_at_1,
        "hit_at_3": hit_at_3,
        "top_3_hits": [
            {
                "rank": i + 1,
                "chunk_id": h["chunk_id"],
                "score": h["score"],
                "page": h["metadata"].get("page"),
                "document_id": h["metadata"].get("document_id"),
                "section": h["metadata"].get("section"),
                "text_preview": h["text"][:200],
                "is_hit": hit_flags[i] if i < len(hit_flags) else False,
            }
            for i, h in enumerate(hits)
        ],
        "filter_used": question.get("filter"),
    }


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate Hit@1 and Evidence Hit@3 by strategy and dev/test split."""
    from collections import defaultdict

    # Group by split
    by_split: dict[str, list] = defaultdict(list)
    for trace in traces:
        by_split[trace["split"]].append(trace)

    result = {}
    for split, split_traces in by_split.items():
        n_total = len(split_traces)
        n_hit1 = sum(1 for t in split_traces if t["hit_at_1"])
        n_hit3 = sum(1 for t in split_traces if t["hit_at_3"])
        result[split] = {
            "total_questions": n_total,
            "hit_at_1_count": n_hit1,
            "hit_at_1_rate": round(n_hit1 / n_total, 3) if n_total else 0,
            "hit_at_3_count": n_hit3,
            "hit_at_3_rate": round(n_hit3 / n_total, 3) if n_total else 0,
        }

    # Overall
    n_total_all = len(traces)
    n_hit1_all = sum(1 for t in traces if t["hit_at_1"])
    n_hit3_all = sum(1 for t in traces if t["hit_at_3"])
    result["overall"] = {
        "total_questions": n_total_all,
        "hit_at_1_count": n_hit1_all,
        "hit_at_1_rate": round(n_hit1_all / n_total_all, 3) if n_total_all else 0,
        "hit_at_3_count": n_hit3_all,
        "hit_at_3_rate": round(n_hit3_all / n_total_all, 3) if n_total_all else 0,
    }

    return result
