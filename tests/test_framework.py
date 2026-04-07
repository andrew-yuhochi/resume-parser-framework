from unittest.mock import MagicMock

import pytest

from src.extractors import FieldExtractor
from src.framework import ResumeExtractor, ResumeParserFramework
from src.models import ResumeData


def test_resume_extractor_orchestration() -> None:
    mock_name_ext = MagicMock(spec=FieldExtractor)
    mock_name_ext.extract.return_value = "Jane Doe"
    
    mock_email_ext = MagicMock(spec=FieldExtractor)
    mock_email_ext.extract.return_value = "jane@example.com"
    
    mock_skills_ext = MagicMock(spec=FieldExtractor)
    mock_skills_ext.extract.return_value = ["Python", "AI"]

    extractors = {
        "name": mock_name_ext,
        "email": mock_email_ext,
        "skills": mock_skills_ext
    }
    
    coordinator = ResumeExtractor(extractors)
    result = coordinator.extract_all("Some dummy resume text")
    
    assert isinstance(result, ResumeData)
    assert result.name == "Jane Doe"
    assert result.email == "jane@example.com"
    assert result.skills == ["Python", "AI"]
    
    mock_name_ext.extract.assert_called_once_with("Some dummy resume text")
    mock_email_ext.extract.assert_called_once_with("Some dummy resume text")
    mock_skills_ext.extract.assert_called_once_with("Some dummy resume text")


def test_framework_unsupported_file_format() -> None:
    framework = ResumeParserFramework(extractors={})
    
    with pytest.raises(ValueError, match="Unsupported file format"):
        framework.parse_resume("sample_resumes/jane_doe_resume.txt")


@pytest.mark.parametrize("file_extension, parser_key", [
    (".pdf", ".pdf"),
    (".docx", ".docx")
])
def test_framework_routing(monkeypatch, file_extension: str, parser_key: str) -> None:
    framework = ResumeParserFramework(extractors={})
    
    mock_parse = MagicMock(return_value=f"Mocked {file_extension} Text")
    monkeypatch.setattr(framework.parsers[parser_key], "parse", mock_parse)
    
    mock_extract_all = MagicMock(return_value=ResumeData(name="Test", email="test@test.com", skills=[]))
    framework.resume_extractor.extract_all = mock_extract_all
    
    fake_file = f"fake_file{file_extension}"
    result = framework.parse_resume(fake_file) 
    
    mock_parse.assert_called_once_with(fake_file)
    mock_extract_all.assert_called_once_with(f"Mocked {file_extension} Text")
    assert isinstance(result, ResumeData)