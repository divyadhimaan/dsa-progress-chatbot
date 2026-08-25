#!/usr/bin/env python3
"""
Build (or rebuild) the FAISS vector index from all .md / .txt files
in backend/rag/data/.

Run once before starting the backend, and re-run after adding new data:

    # from the project root:
    python backend/rag/build_index.py

    # or from inside backend/:
    python rag/build_index.py
"""

import os
import glob
import pickle
import sys
import numpy as np


# ── paths ─────────────────────────────────────────────────────────────────────
_HERE     = os.path.dirname(os.path.abspath(__file__))   # backend/rag/
_BACKEND  = os.path.dirname(_HERE)                        # backend/
DATA_DIR  = os.path.join(_HERE, "data")
INDEX_DIR = os.path.join(_BACKEND, "index")


# ── chunking ──────────────────────────────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = 350, overlap: int = 50) -> list[str]:
    """
    Split *text* into overlapping word-count windows.
    chunk_size ≈ 350 words → ~500 tokens, fits comfortably inside most LLM context.
    """
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunk = " ".join(words[i : i + chunk_size]).strip()
        if chunk:
            chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


# ── main ──────────────────────────────────────────────────────────────────────

def build(chunk_size: int = 350, overlap: int = 50) -> None:
    try:
        import faiss
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("❌ Missing dependencies. Run:  pip install faiss-cpu sentence-transformers")
        sys.exit(1)

    os.makedirs(INDEX_DIR, exist_ok=True)

    data_files = sorted(
        glob.glob(os.path.join(DATA_DIR, "*.md"))
        + glob.glob(os.path.join(DATA_DIR, "*.txt"))
    )
    if not data_files:
        print(f"❌ No data files found in {DATA_DIR}")
        sys.exit(1)

    # ── read & chunk ──────────────────────────────────────────────────────────
    all_chunks: list[str] = []
    print("📄 Reading data files...")
    for path in data_files:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_text(text, chunk_size, overlap)
        all_chunks.extend(chunks)
        print(f"   {os.path.basename(path):30s} → {len(chunks):3d} chunks")

    print(f"\n🔢 Total chunks : {len(all_chunks)}")

    # ── embed ─────────────────────────────────────────────────────────────────
    print("⚙️  Encoding with all-MiniLM-L6-v2 ...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(
        all_chunks,
        show_progress_bar=True,
        batch_size=64,
        convert_to_numpy=True,
    ).astype("float32")

    # L2-normalise so inner-product = cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings /= np.where(norms == 0, 1, norms)

    # ── build FAISS index ─────────────────────────────────────────────────────
    dim   = embeddings.shape[1]                # 384 for MiniLM
    index = faiss.IndexFlatIP(dim)             # exact cosine search
    index.add(embeddings)

    # ── persist ───────────────────────────────────────────────────────────────
    index_path  = os.path.join(INDEX_DIR, "faiss.index")
    chunks_path = os.path.join(INDEX_DIR, "chunks.pkl")

    faiss.write_index(index, index_path)
    with open(chunks_path, "wb") as f:
        pickle.dump(all_chunks, f)

    print(f"\n✅ Index built!")
    print(f"   Vectors  : {index.ntotal}")
    print(f"   Chunks   : {len(all_chunks)}")
    print(f"   Saved to : {INDEX_DIR}/")
    print("\nYou can now (re)start the backend — RAG will load on the first query.")


if __name__ == "__main__":
    build()
