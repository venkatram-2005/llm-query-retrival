# app/services/chunker.py

import re
from typing import List

def split_into_paragraphs(text: str) -> List[str]:
    """
    Splits text into paragraphs based on double newlines or indentation.
    """
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove excessive whitespace and standardize paragraphs
    paragraphs = re.split(r'\n\s*\n', text)
    cleaned = [para.strip() for para in paragraphs if len(para.strip()) > 30]  # filter short lines
    return cleaned

def merge_small_chunks(chunks: List[str], max_tokens: int = 512) -> List[str]:
    """
    Merges small chunks until they reach a token limit (~approximate by word count).
    Gemini Flash has ~8k token limit, we stay small for accuracy.
    """
    merged = []
    buffer = ""
    for chunk in chunks:
        if len((buffer + chunk).split()) < max_tokens:
            buffer += "\n" + chunk
        else:
            merged.append(buffer.strip())
            buffer = chunk
    if buffer:
        merged.append(buffer.strip())
    return merged

def chunk_text(text: str) -> List[str]:
    """
    Full chunking pipeline: split text into semantically meaningful chunks.
    """
    paras = split_into_paragraphs(text)
    chunks = merge_small_chunks(paras)
    return chunks
