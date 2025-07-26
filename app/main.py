# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.query import router as query_router

app = FastAPI(
    title="LLM-Powered Query Retrieval System",
    version="1.0",
    description="Handles PDF, DOCX, and email-based queries using Gemini + FAISS"
)

# CORS (Optional: allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route
app.include_router(query_router)
