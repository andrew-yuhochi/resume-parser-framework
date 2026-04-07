from unittest.mock import MagicMock

from src.extractors import SkillsExtractor
from src.llm_client import LLMClient


def test_skills_extractor_happy_path() -> None:
    mock_client = MagicMock(spec=LLMClient)
    mock_client.generate_text.return_value = '{"skills": ["Python", "SQL"]}'
    
    extractor = SkillsExtractor(llm_client=mock_client)
    skills = extractor.extract("Resume text")
    
    assert skills == ["Python", "SQL"]
    assert mock_client.generate_text.call_count == 1


def test_skills_extractor_retry_success() -> None:
    mock_client = MagicMock(spec=LLMClient)
    mock_client.generate_text.side_effect = [
        "Garbage response 1", 
        "Garbage response 2", 
        '{"skills": ["Python", "SQL"]}'
    ]
    
    extractor = SkillsExtractor(llm_client=mock_client)
    extractor.retry_delay = 0  
    skills = extractor.extract("Resume text")
    
    assert skills == ["Python", "SQL"]
    assert mock_client.generate_text.call_count == 3


def test_skills_extractor_total_failure() -> None:
    mock_client = MagicMock(spec=LLMClient)
    mock_client.generate_text.side_effect = Exception("API Timeout")
    
    extractor = SkillsExtractor(llm_client=mock_client)
    extractor.retry_delay = 0  
    skills = extractor.extract("Resume text")
    
    assert skills == []
    assert mock_client.generate_text.call_count == 3