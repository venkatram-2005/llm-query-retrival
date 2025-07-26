# app/models.py

from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict

class QueryRequest(BaseModel):
    query: str = Field(..., example="What are the termination clauses in this contract?")
    document_url: HttpUrl = Field(..., example="https://example.com/sample.pdf")

class ClauseMatch(BaseModel):
    chunk: str
    similarity_score: float

class DecisionRationale(BaseModel):
    explanation: str
    matched_clauses: List[ClauseMatch]

class QueryResponse(BaseModel):
    query: str
    result: str
    rationale: DecisionRationale
    source_chunks: List[str]
