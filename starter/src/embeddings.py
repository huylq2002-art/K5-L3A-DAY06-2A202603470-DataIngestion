"""Embedding provider using local Sentence Transformers model (multilingual)."""
import os
from typing import Protocol
import warnings

# Suppress symlink warnings on Windows
warnings.filterwarnings("ignore", category=UserWarning, module="huggingface_hub")
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order."""
        ...

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        ...


class MyEmbedder:
    """Local Sentence Transformers embedder using multilingual MiniLM model.
    
    Model: paraphrase-multilingual-MiniLM-L12-v2
    Provider: sentence-transformers (local, no API key required)
    Dimensions: 384
    Language support: 50+ languages including Vietnamese
    Distance metric: Cosine similarity
    """

    MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
    DIMENSIONS = 384

    def __init__(self, model_name: str = MODEL_NAME) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise RuntimeError(
                "sentence-transformers is not installed. "
                "Run: pip install sentence-transformers"
            )

        self.model_name = model_name
        self.dimensions = self.DIMENSIONS
        print(f"[Embedder] Loading model '{model_name}'...")
        self._model = SentenceTransformer(model_name)
        print(f"[Embedder] Model loaded. Dimensions: {self.dimensions}")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text using 'passage' prompt for documents."""
        if not texts:
            return []
        # batch encode for efficiency
        vectors = self._model.encode(
            texts,
            batch_size=32,
            show_progress_bar=len(texts) > 50,
            normalize_embeddings=True,  # for cosine similarity
        )
        return [v.tolist() for v in vectors]

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with document vectors."""
        vector = self._model.encode(
            question,
            normalize_embeddings=True,
        )
        return vector.tolist()
