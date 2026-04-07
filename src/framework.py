import os
from typing import Dict

from .extractors import FieldExtractor
from .models import ResumeData
from .parsers import FileParser, PDFParser, WordParser


class ResumeExtractor:
    """Orchestrates extraction across multiple fields to build a ResumeData object."""

    def __init__(self, extractors: Dict[str, FieldExtractor]) -> None:
        self.extractors = extractors

    def extract_all(self, text: str) -> ResumeData:
        name = self.extractors["name"].extract(text) if "name" in self.extractors else ""
        email = self.extractors["email"].extract(text) if "email" in self.extractors else ""
        skills = self.extractors["skills"].extract(text) if "skills" in self.extractors else []

        return ResumeData(name=name, email=email, skills=skills)


class ResumeParserFramework:
    """Provides a unified interface for parsing resume files into structured data."""

    def __init__(self, extractors: Dict[str, FieldExtractor]) -> None:
        self.resume_extractor = ResumeExtractor(extractors)
        
        self.parsers: Dict[str, FileParser] = {
            ".pdf": PDFParser(),
            ".docx": WordParser()
        }

    def parse_resume(self, file_path: str) -> ResumeData:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext not in self.parsers:
            supported = list(self.parsers.keys())
            raise ValueError(f"Unsupported file format: '{ext}'. Supported formats: {supported}")

        parser = self.parsers[ext]
        text = parser.parse(file_path)

        return self.resume_extractor.extract_all(text)