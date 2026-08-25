"""
RAG Retriever — lazy-loads the FAISS index and sentence-transformer model
on the first query. Falls back gracefully (returns "") if the index hasn't
been built yet.

Usage:
    from rag.retriever import retrieve, rag_status

    context = retrieve("how does sliding window work", k=3)
    info    = rag_status()
"""

import os
import pickle
import numpy as np

# Paths are relative to this file's location (backend/rag/)
_BASE = os.path.dirname(os.path.dirname(__file__))          # backend/
INDEX_DIR   = os.path.join(_BASE, "index")
INDEX_PATH  = os.path.join(INDEX_DIR, "faiss.index")
CHUNKS_PATH = os.path.join(INDEX_DIR, "chunks.pkl")

# Module-level singletons — loaded once, reused forever
_model  = None
_index  = None
_chunks: list[str] = []


# ── helpers ──────────────────────────────────────────────────────────────────

def _index_exists() -> bool:
    return os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH)


def _load() -> bool:
    """Load model + index into module globals. Returns True on success."""
    global _model, _index, _chunks

    if _model is not None:
        return True          # already loaded

    if not _index_exists():
        return False         # index not built yet

    try:
        import faiss
        from sentence_transformers import SentenceTransformer

        print("🔍 Loading RAG components...")
        _model  = SentenceTransformer("all-MiniLM-L6-v2")
        _index  = faiss.read_index(INDEX_PATH)
        with open(CHUNKS_PATH, "rb") as f:
            _chunks = pickle.load(f)
        print(f"✅ RAG ready — {_index.ntotal} vectors · {len(_chunks)} chunks")
        return True

    except Exception as exc:
        print(f"⚠️  RAG load failed: {exc}")
        return False


# ── public API ────────────────────────────────────────────────────────────────

def retrieve(query: str, k: int = 3, min_score: float = 0.25) -> str:
    """
    Return a formatted string of the top-k relevant DSA knowledge chunks
    for *query*, or "" if the index is unavailable.

    Args:
        query:     The user's question to embed and search.
        k:         Number of chunks to retrieve.
        min_score: Minimum cosine-similarity score to include a chunk.
    """
    if not _load():
        return ""

    try:
        vec = _model.encode([query]).astype("float32")
        vec /= np.linalg.norm(vec, axis=1, keepdims=True)   # normalise → cosine via IP

        scores, indices = _index.search(vec, k)

        results = [
            _chunks[idx]
            for score, idx in zip(scores[0], indices[0])
            if idx < len(_chunks) and float(score) >= min_score
        ]

        return "\n\n---\n\n".join(results) if results else ""

    except Exception as exc:
        print(f"⚠️  Retrieval error: {exc}")
        return ""


def rag_status() -> dict:
    """Return a status dict suitable for the /api/rag/status endpoint."""
    loaded = _model is not None
    return {
        "index_exists": _index_exists(),
        "loaded":       loaded,
        "num_vectors":  _index.ntotal if _index else 0,
        "num_chunks":   len(_chunks),
        "index_dir":    INDEX_DIR,
    }
