# tests/test_chunker.py

import pytest
from app.services import chunker

def test_clause_chunking_basic():
    text = (
        "1. Introduction\n"
        "This policy covers the usage terms.\n\n"
        "2. Definitions\n"
        "Key terms are explained here.\n\n"
        "3. Scope\n"
        "This applies to all employees.\n"
    )

    chunks = chunker.chunk_text(text, max_tokens=50)

    assert len(chunks) == 3
    assert "Introduction" in chunks[0]
    assert "Definitions" in chunks[1]
    assert "Scope" in chunks[2]

def test_chunking_token_limit():
    # Simulate long clause
    long_text = "Clause:\n" + ("word " * 300)
    chunks = chunker.chunk_text(long_text, max_tokens=100)

    # Should be split into multiple chunks
    assert len(chunks) >= 2
    assert all(isinstance(c, str) for c in chunks)

def test_empty_text():
    chunks = chunker.chunk_text("", max_tokens=100)
    assert chunks == []

def test_single_clause_under_limit():
    text = "Section 1\nThis clause is short and should not be split."
    chunks = chunker.chunk_text(text, max_tokens=100)
    assert len(chunks) == 1
