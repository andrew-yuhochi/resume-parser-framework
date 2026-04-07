import json
from dataclasses import asdict, dataclass
from typing import List


@dataclass
class ResumeData:
    """Encapsulates the extracted resume fields."""

    name: str
    email: str
    skills: List[str]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=4)