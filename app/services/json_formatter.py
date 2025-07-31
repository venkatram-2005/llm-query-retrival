# app/services/json_formatter.py

from typing import List

def format_answers_only(llm_outputs: List[str]) -> List[str]:
    """
    Returns a list of plain string answers for the API response.

    Args:
        llm_outputs (List[str]): LLM-generated answers for each question.

    Returns:
        List[str]: List of answers
    """
    return [answer.strip() for answer in llm_outputs]
