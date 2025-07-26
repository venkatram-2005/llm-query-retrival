# tests/test_parser.py

import pytest
from unittest.mock import patch
from app.services import parser

def test_parse_pdf_text_success():
    dummy_pdf_text = "This is a sample PDF content."

    with patch("app.services.parser.extract_text_from_pdf") as mock_extract:
        mock_extract.return_value = dummy_pdf_text

        result = parser.parse_document("https://example.com/sample.pdf")
        assert dummy_pdf_text in result

def test_parse_docx_text_success():
    dummy_docx_text = "This is a sample DOCX content."

    with patch("app.services.parser.extract_text_from_docx") as mock_extract:
        mock_extract.return_value = dummy_docx_text

        result = parser.parse_document("https://example.com/sample.docx")
        assert dummy_docx_text in result

def test_parse_email_text_success():
    dummy_email_text = "Subject: Hello\nThis is a test email."

    with patch("app.services.parser.extract_text_from_email") as mock_extract:
        mock_extract.return_value = dummy_email_text

        result = parser.parse_document("https://example.com/sample.eml")
        assert dummy_email_text in result

def test_parse_unknown_format():
    with pytest.raises(ValueError) as exc_info:
        parser.parse_document("https://example.com/unknown.xyz")
    assert "Unsupported document format" in str(exc_info.value)
