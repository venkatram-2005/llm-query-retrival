# tests/test_embedding.py

import pytest
from unittest.mock import patch
from app.services import embedder

def test_get_embedding_success():
    sample_text = "This is a test clause."

    # Patch the embed_text function (which uses Gemini or Instructor)
    with patch("app.services.embedder.embed_text") as mock_embed:
        mock_embed.return_value = [0.1] * 768  # Mocked embedding vector

        embedding = embedder.get_embedding(sample_text)
        assert isinstance(embedding, list)
        assert len(embedding) == 768
        assert embedding[0] == 0.1

def test_get_embedding_empty_string():
    with patch("app.services.embedder.embed_text") as mock_embed:
        mock_embed.return_value = [0.0] * 768
        embedding = embedder.get_embedding("")
        assert isinstance(embedding, list)
        assert len(embedding) == 768

def test_batch_embedding_multiple_inputs():
    texts = ["Clause 1", "Clause 2", "Clause 3"]

    with patch("app.services.embedder.embed_text") as mock_embed:
        mock_embed.side_effect = lambda x: [float(len(x))] * 768

        embeddings = [embedder.get_embedding(text) for text in texts]

        assert len(embeddings) == len(texts)
        assert all(len(e) == 768 for e in embeddings)
