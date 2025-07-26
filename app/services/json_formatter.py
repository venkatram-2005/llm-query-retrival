# app/services/json_formatter.py

from typing import List
from app.models import QueryResponse, DecisionRationale, ClauseMatch

def format_answers(query: str, llm_output: str, matched_chunks: List[str], scores: List[float]) -> QueryResponse:
    """
    Formats the final output as a structured QueryResponse.
    
    Args:
        query (str): User's natural language question.
        llm_output (str): LLM's explanation/answer.
        matched_chunks (List[str]): Chunks matched via semantic similarity.
        scores (List[float]): Corresponding similarity scores.
    
    Returns:
        QueryResponse: Structured response for API.
    """

    # Zip matched clauses with scores
    clause_matches = [
        ClauseMatch(chunk=chunk, similarity_score=round(score, 4))
        for chunk, score in zip(matched_chunks, scores)
    ]

    # Package rationale
    rationale = DecisionRationale(
        explanation=llm_output.strip(),
        matched_clauses=clause_matches
    )

    # Final structured response
    return QueryResponse(
        query=query,
        result=llm_output.strip(),
        rationale=rationale,
        source_chunks=matched_chunks
    )
