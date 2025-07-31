# app/services/llm_decider.py

import os
import google.generativeai as genai
from typing import List

# Load Gemini Flash model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

def format_prompt(query: str, top_chunks: List[str]) -> str:
    """
    Prepares the prompt for the Gemini model using context and user query.
    """
    context = "\n\n---\n\n".join(top_chunks)
    prompt = f"""
You are a insurance, legal, HR and compliance domain assistant.

Context:
{context}

Query:
{query}

Based on the context, provide:
1. A concise answer
2. Relevant clauses (quote exact text)
3. Reasoning behind the match
4. Output everything in JSON format like:
{{
  "answer": "...",
  "matched_clauses": ["..."],
  "reasoning": "...",
  "source_chunks": ["..."]
}}
"""
    return prompt.strip()

def answer_with_gemini(query: str, top_chunks: List[str]) -> dict:
    """
    Calls Gemini with formatted prompt and returns structured JSON.
    """
    prompt = format_prompt(query, top_chunks)
    response = model.generate_content(prompt)
    
    # Extract JSON from LLM response
    import json, re
    match = re.search(r'\{.*\}', response.text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return {"error": "LLM returned malformed JSON", "raw": response.text}
    else:
        return {"error": "No JSON found", "raw": response.text}
