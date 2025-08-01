# app/services/parser.py

import os
import tempfile
import requests
import fitz  # PyMuPDF for PDF parsing
from docx import Document  # For DOCX files
import email
from email import policy

from urllib.parse import urlparse, unquote

def download_file(url: str) -> str:
    """
    Downloads the file from the given URL and returns a clean local filepath.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {url}")

    # Parse the clean path (drop query params like ?sv=...)
    parsed = urlparse(url)
    path = unquote(parsed.path)  # e.g., '/assets/filename.pdf'
    ext = os.path.splitext(path)[1] or ".pdf"  # Get extension only

    # Save to safe tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
        tmp_file.write(response.content)
        return tmp_file.name



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



def extract_text_from_url(url_or_path: str) -> str:
    if os.path.exists(url_or_path):
        local_path = url_or_path
    else:
        local_path = download_file_from_url(url_or_path)

    ext = os.path.splitext(local_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(local_path)
    elif ext in [".docx", ".doc"]:
        return extract_text_from_docx(local_path)
    elif ext == ".eml":
        return extract_text_from_email(local_path)
    else:
        raise Exception(f"Unsupported file type: {ext}")

    # optionally clean up downloaded file here if you want


