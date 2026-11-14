"""Vector store using ChromaDB (persistent, no Docker required).

ChromaDB is used instead of PostgreSQL+pgvector because Docker Desktop is not
running in this environment. ChromaDB provides:
- Persistent local storage (DuckDB backend)
- Cosine similarity search
- Metadata filtering
- No external service required

NOTE: If you want to use PostgreSQL+pgvector, start Docker Desktop and
      run: docker compose -p day6_student_starter up -d --wait
      then switch to the PgVectorStore class below.
"""
import json
import time
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings

from .models import Chunk


CHROMA_PATH = Path(__file__).resolve().parents[1] / "results" / "chroma_db"


def _get_client() -> chromadb.PersistentClient:
    CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_PATH))


class ChromaVectorStore:
    """ChromaDB-backed vector store with metadata filtering support.

    Collections are named per-strategy: "strategy_A", "strategy_B", "strategy_C".
    Re-ingestion uses upsert (overwrite by chunk_id) to avoid duplicates.
    """

    def __init__(self, dimensions: int) -> None:
        self.dimensions = dimensions
        self._client = _get_client()
        print(f"[Store] ChromaDB initialized at {CHROMA_PATH}")

    def _collection_name(self, strategy: str) -> str:
        return f"strategy_{strategy}"

    def create_schema(self) -> None:
        """Collections are created lazily in ChromaDB; nothing to do here."""
        print("[Store] ChromaDB schema ready (collections created on first upsert).")

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        """Validate lengths/dimensions and write stable IDs without duplicates.

        Uses ChromaDB's native upsert: if chunk_id already exists, it is overwritten.
        """
        if len(chunks) != len(vectors):
            raise ValueError(
                f"Mismatch: {len(chunks)} chunks but {len(vectors)} vectors."
            )
        if vectors and len(vectors[0]) != self.dimensions:
            raise ValueError(
                f"Vector dimension mismatch: expected {self.dimensions}, got {len(vectors[0])}."
            )

        col = self._client.get_or_create_collection(
            name=self._collection_name(strategy),
            metadata={"hnsw:space": "cosine"},
        )

        # ChromaDB upsert in batches of 500
        batch_size = 500
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i + batch_size]
            batch_vectors = vectors[i:i + batch_size]

            ids = [c.chunk_id for c in batch_chunks]
            documents = [c.text for c in batch_chunks]
            metadatas = []
            for c in batch_chunks:
                meta = {
                    "document_id": c.document_id,
                    "source": c.source,
                    "page": c.page,
                }
                # merge chunk-level metadata (section, year, etc.)
                for k, v in c.metadata.items():
                    if isinstance(v, (str, int, float, bool)):
                        meta[k] = v
                metadatas.append(meta)

            col.upsert(
                ids=ids,
                embeddings=batch_vectors,
                documents=documents,
                metadatas=metadatas,
            )

        print(f"[Store] Upserted {len(chunks)} chunks into strategy '{strategy}'.")

    def search(
        self,
        strategy: str,
        query_vector: list[float],
        top_k: int = 3,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Filter metadata in ChromaDB where clause, rank by cosine distance, return top-k.

        Returns chunk_id, text, score (cosine similarity, higher=better), and metadata.
        """
        col = self._client.get_or_create_collection(
            name=self._collection_name(strategy),
            metadata={"hnsw:space": "cosine"},
        )

        # Build ChromaDB where clause from filters
        where = None
        if filters:
            if len(filters) == 1:
                key, val = next(iter(filters.items()))
                where = {key: {"$eq": val}}
            else:
                where = {"$and": [{k: {"$eq": v}} for k, v in filters.items()]}

        query_kwargs: dict[str, Any] = {
            "query_embeddings": [query_vector],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            query_kwargs["where"] = where

        results = col.query(**query_kwargs)

        hits = []
        if results and results["ids"] and results["ids"][0]:
            for idx, chunk_id in enumerate(results["ids"][0]):
                # ChromaDB distance is 1 - cosine_similarity for cosine space
                distance = results["distances"][0][idx]
                score = 1.0 - distance  # convert to similarity (higher = better)
                hits.append({
                    "chunk_id": chunk_id,
                    "text": results["documents"][0][idx],
                    "score": round(score, 4),
                    "metadata": results["metadatas"][0][idx],
                })

        return hits

    def count(self, strategy: str) -> int:
        """Return number of chunks stored for a strategy."""
        try:
            col = self._client.get_collection(self._collection_name(strategy))
            return col.count()
        except Exception:
            return 0

    def delete_strategy(self, strategy: str) -> None:
        """Delete all chunks for a strategy (for clean re-ingestion)."""
        try:
            self._client.delete_collection(self._collection_name(strategy))
            print(f"[Store] Deleted collection for strategy '{strategy}'.")
        except Exception:
            pass
