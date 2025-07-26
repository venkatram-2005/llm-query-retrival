# tests/test_endpoints.py

import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Set the API key in environment to match what is used in the test
os.environ["API_KEY"] = "test_api_key"

client = TestClient(app)

def test_run_query_success(monkeypatch):
    # Mocking process_query_pipeline
    def mock_pipeline(doc_url, questions):
        return [{"question": q, "answer": "Mocked answer"} for q in questions]

    from app.services import pipeline
    monkeypatch.setattr(pipeline, "process_query_pipeline", mock_pipeline)

    payload = {
        "documents": "https://example.com/sample.pdf",
        "questions": ["What is the policy term?", "Who is covered?"]
    }

    headers = {
        "Authorization": "Bearer test_api_key"
    }

    response = client.post("/hackrx/run", json=payload, headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all("question" in ans and "answer" in ans for ans in response.json())

def test_run_query_unauthorized():
    payload = {
        "documents": "https://example.com/sample.pdf",
        "questions": ["What is the premium?"]
    }

    headers = {
        "Authorization": "Bearer wrong_key"
    }

    response = client.post("/hackrx/run", json=payload, headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API token"

def test_run_query_invalid_payload():
    # Missing 'documents' key
    payload = {
        "wrong_field": "https://example.com/sample.pdf",
        "questions": ["Sample?"]
    }

    headers = {
        "Authorization": "Bearer test_api_key"
    }

    response = client.post("/hackrx/run", json=payload, headers=headers)

    assert response.status_code == 422  # Unprocessable Entity (validation error)
