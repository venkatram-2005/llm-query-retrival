# app/services/pipeline.py (or wherever your pipeline lives)

from app.services.parser import extract_text_from_url
from app.services.chunker import chunk_text
from app.services.embedder import embed_chunks, embed_query
from app.services.vector_store import build_faiss_index, search_faiss_index
from app.services.llm_decider import answer_with_gemini
from app.services.json_formatter import format_answers_only

import os

def process_query_pipeline(document_url: str, questions: list[str]) -> list[str]:
    # Step 1: Download file locally (returns clean local path)
    local_path = download_file_from_url(document_url)

    try:
        # Step 2: Extract text from the local file path
        raw_text = extract_text_from_url(local_path)

        # Step 3: Continue with processing
        chunks = chunk_text(raw_text)
        chunk_embeddings = embed_chunks(chunks)
        index = build_faiss_index(chunk_embeddings)

        llm_outputs = []

        for question in questions:
            query_embedding = embed_query(question)
            top_chunks_with_scores = search_faiss_index(index, query_embedding, chunks, top_k=5)
            matched_chunks = [item["chunk"] for item in top_chunks_with_scores]
            llm_result = answer_with_gemini(question, matched_chunks)
            print("Gemini response:", llm_result)
            llm_output = llm_result.get("answer", "") if isinstance(llm_result, dict) else llm_result
            llm_outputs.append(llm_output)

        return format_answers_only(llm_outputs)

    finally:
        # Step 4: Cleanup temp file
        try:
            os.remove(local_path)
        except Exception as e:
            print(f"Warning: Could not delete temp file: {e}")


# Your existing download function with safe filename extraction
import tempfile
import requests
from urllib.parse import urlparse, unquote
import os

def download_file_from_url(url: str) -> str:
    response = requests.get(url, verify=True)
    if response.status_code != 200:
        raise Exception(f"Failed to download file from {url}")

    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)  # decode %20 etc

    file_ext = os.path.splitext(path)[1] or ".tmp"

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
        tmp_file.write(response.content)
        print(f"Saved file to temporary path: {tmp_file.name}")  # Debug info
        return tmp_file.name


import os
from urllib.parse import urlparse
from app.utils.downloader import download_file_from_url  # assuming this is in a separate module
from app.services.parser import extract_text_from_pdf  # whatever you use to parse PDF text

def extract_text_from_url(url_or_path: str) -> str:
    """
    Extracts text from a given URL or local file path.
    If the input is a URL, downloads the file and processes it.
    """
    print(f"[extract_text_from_url] Input: {url_or_path}")

    # Check if it's a URL
    parsed = urlparse(url_or_path)
    if parsed.scheme in ["http", "https"]:
        print("[extract_text_from_url] Detected URL, downloading...")
        local_path = download_file_from_url(url_or_path)

        try:
            print(f"[extract_text_from_url] Extracting from downloaded file: {local_path}")
            return extract_text_from_pdf(local_path)
        finally:
            # Clean up downloaded file
            try:
                os.remove(local_path)
                print(f"[extract_text_from_url] Temporary file deleted: {local_path}")
            except Exception as e:
                print(f"[extract_text_from_url] Failed to delete temp file: {e}")
    else:
        # Local file path
        if not os.path.exists(url_or_path):
            raise FileNotFoundError(f"File does not exist: {url_or_path}")

        print(f"[extract_text_from_url] Detected local path, extracting: {url_or_path}")
        return extract_text_from_pdf(url_or_path)
