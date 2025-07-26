# app/services/embedder.py

from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model once
# You can switch to 'BAAI/bge-small-en-v1.5' if you prefer
model = SentenceTransformer('all-MiniLM-L6-v2')  # ~80MB, fast & accurate for general use

def embed_chunks(chunks: List[str]) -> np.ndarray:
    """
    Converts a list of text chunks into embeddings.
    """
    embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)
    return embeddings

def embed_query(query: List[str]) -> np.ndarray:
    """
    Converts a list of text chunks into embeddings.
    """
    embeddings = model.encode(query, show_progress_bar=True, convert_to_numpy=True)
    return embeddings
