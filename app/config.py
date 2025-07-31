# app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.0-flash")  # default to flash

# Embedding Model
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "hkunlp/instructor-xl")

# Chunking Config
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 512))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))

# Retrieval Config
TOP_K = int(os.getenv("TOP_K", 5))

# API Key for the application
API_KEY = os.getenv("API_KEY")
