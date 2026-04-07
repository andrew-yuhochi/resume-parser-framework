import json

from src.models import ResumeData


def test_resume_data_schema_and_serialization() -> None:
    data = ResumeData(
        name="Test Name",
        email="test@email.com",
        skills=["Skill 1", "Skill 2"]
    )
    
    json_output = data.to_json()
    parsed_json = json.loads(json_output)
    
    assert hasattr(data, "name")
    assert hasattr(data, "email")
    assert hasattr(data, "skills")
    assert isinstance(data.skills, list)
    
    expected_keys = {"name", "email", "skills"}
    assert set(parsed_json.keys()) == expected_keys
    
    assert isinstance(parsed_json["name"], str)
    assert isinstance(parsed_json["email"], str)
    assert isinstance(parsed_json["skills"], list)