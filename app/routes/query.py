# app/routes/query.py

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import List, Dict
from app.services.pipeline import process_query_pipeline
from app.utils.logger import get_logger
from app.config import API_KEY  # ✅ Load from config.py

router = APIRouter()
logger = get_logger(__name__)

# Input schema
class QueryRequest(BaseModel):
    documents: str                     # Blob URL or doc link
    questions: List[str]              # List of natural language queries

@router.post("/hackrx/run", response_model=Dict[str, List[str]])
async def run_query(request: QueryRequest, Authorization: str = Header(...)):
    if Authorization != f"Bearer {API_KEY}":
        logger.warning("Unauthorized access attempt.")
        raise HTTPException(status_code=401, detail="Invalid API token")

    try:
        logger.info(f"Processing query for document: {request.documents}")
        answers = process_query_pipeline(request.documents, request.questions)
        return {"answers": answers}  # ✅ Wrap in dict
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
