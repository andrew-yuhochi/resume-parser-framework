import pytest

from src.parsers import PDFParser, WordParser


def test_word_parser_extraction() -> None:
    parser = WordParser()
    try:
        text = parser.parse("sample_resumes/jane_doe_resume.docx")
        assert "Jane Doe" in text
        assert "jane.doe@gmail.com" in text
    except FileNotFoundError:
        pytest.skip("Sample Word file not found. Skipping extraction test.")


def test_pdf_parser_extraction() -> None:
    parser = PDFParser()
    try:
        text = parser.parse("sample_resumes/john_smith_resume.pdf")
        assert "SMITH" in text
        assert "JOHN.SMITH@EXAMPLE.COM" in text
    except FileNotFoundError:
        pytest.skip("Sample PDF file not found. Skipping extraction test.")