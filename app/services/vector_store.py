# app/services/vector_store.py

import faiss
import numpy as np
from typing import List

def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """
    Creates a FAISS index from embeddings.
    """
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

def search_faiss_index(index, query_embedding, chunks, top_k=5):
    D, I = index.search(query_embedding.reshape(1, -1), top_k)  # D: distance, I: indices
    results = [
        {"chunk": chunks[i], "score": float(1 - D[0][idx])}  # if using cosine sim
        for idx, i in enumerate(I[0])
    ]
    return results

