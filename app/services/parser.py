# app/services/parser.py

import os
import tempfile
import requests
import fitz  # PyMuPDF for PDF parsing
from docx import Document  # For DOCX files
import email
from email import policy

def download_file(url: str) -> str:
    """
    Downloads the file from the given URL and returns the local filepath.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {url}")

    # Create a temporary file with the correct extension based on the URL
    file_ext = os.path.splitext(url)[1] or ".tmp"
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
        tmp_file.write(response.content)
        tmp_filepath = tmp_file.name

    return tmp_filepath

def extract_text_from_pdf(filepath: str) -> str:
    """
    Extract text from a PDF file using PyMuPDF.
    """
    text = ""
    doc = fitz.open(filepath)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_text_from_docx(filepath: str) -> str:
    """
    Extract text from a DOCX file using python-docx.
    """
    doc = Document(filepath)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_email(filepath: str) -> str:
    """
    Extract text from an email file (.eml) using Python's email module.
    """
    with open(filepath, "rb") as f:
        msg = email.message_from_binary_file(f, policy=policy.default)
    # Extract plain text parts (optionally, you can add HTML handling)
    text_parts = []
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                text_parts.append(part.get_content())
    else:
        if msg.get_content_type() == "text/plain":
            text_parts.append(msg.get_content())
    return "\n".join(text_parts)

def extract_text_from_url(url: str) -> str:
    """
    Downloads the file from the provided URL and extracts text content.
    Supports PDF, DOCX, and email (.eml) files.
    """
    # Download file and get local path
    local_path = download_file(url)

    # Determine file type based on extension
    ext = os.path.splitext(local_path)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(local_path)
    elif ext in [".docx", ".doc"]:
        text = extract_text_from_docx(local_path)
    elif ext in [".eml"]:
        text = extract_text_from_email(local_path)
    else:
        raise Exception(f"Unsupported file type: {ext}")

    # Optional: Remove temporary file after processing
    os.remove(local_path)

    return text
