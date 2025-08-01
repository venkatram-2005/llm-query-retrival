# app/utils/downloader.py

import os
import requests
import mimetypes
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse

SUPPORTED_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "message/rfc822": ".eml"
}

def download_file(url: str) -> str:
    """
    Downloads a file from a blob/document URL and saves it locally.
    
    Args:
        url (str): The document blob or HTTP URL.
    
    Returns:
        str: Path to the downloaded file.
    
    Raises:
        ValueError: If the file type is not supported or download fails.
    """
    try:
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type")
        extension = SUPPORTED_TYPES.get(content_type)

        if not extension:
            raise ValueError(f"Unsupported file type: {content_type}")

        with NamedTemporaryFile(delete=False, suffix=extension, mode='wb') as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
            return temp_file.name

    except requests.RequestException as e:
        raise RuntimeError(f"Download failed: {e}")

import os
import tempfile
import requests
from urllib.parse import urlparse, unquote

def download_file_from_url(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()

    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    file_ext = os.path.splitext(path)[1] or ".tmp"

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
        tmp_file.write(response.content)
        print(f"[download_file_from_url] Saved to temp path: {tmp_file.name}")
        return tmp_file.name
