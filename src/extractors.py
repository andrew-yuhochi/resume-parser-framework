import json
import re
import time
from abc import ABC, abstractmethod
from typing import Any, List

import spacy

from . import config
from .llm_client import LLMClient


class FieldExtractor(ABC):
    """Abstract base class for field extraction strategies."""

    @abstractmethod
    def extract(self, text: str) -> Any:
        pass


class EmailExtractor(FieldExtractor):
    """Extracts an email address using a regular expression."""

    def __init__(self) -> None:
        self.email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

    def extract(self, text: str) -> str:
        match = re.search(self.email_pattern, text)
        return match.group(0) if match else ""


class NameExtractor(FieldExtractor):
    """Extracts a person's name using a spaCy NER model."""

    def __init__(self) -> None:
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise OSError("spaCy model not found. Run: python -m spacy download en_core_web_sm")

    def extract(self, text: str) -> str:
        lines = text.split('\n')
        first_valid_line = None
        
        for line in lines:
            clean_line = line.strip()
            if not clean_line:
                continue
                
            if first_valid_line is None:
                first_valid_line = clean_line
                
            # Convert ALL CAPS to Title Case for better NER recognition
            eval_line = clean_line.title() if clean_line.isupper() else clean_line
            
            doc = self.nlp(eval_line)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    return ent.text.strip()
                    
        # Fallback to the first non-empty line if NER fails
        return first_valid_line if first_valid_line else ""


class SkillsExtractor(FieldExtractor):
    """Extracts skills using a configured LLM client."""

    def __init__(self, llm_client: LLMClient, prompt_template: str = None) -> None:
        self.llm_client = llm_client
        self.prompt_template = prompt_template or config.DEFAULT_SKILLS_PROMPT
        self.max_retries = config.MAX_RETRIES
        self.retry_delay = config.RETRY_DELAY_SECONDS 

    def extract(self, text: str) -> List[str]:
        prompt = self.prompt_template.format(text=text)
        
        for attempt in range(self.max_retries):
            try:
                response_text = self.llm_client.generate_text(prompt)
                clean_text = response_text.strip().removeprefix("```json").removesuffix("```").strip()
                data = json.loads(clean_text)
                return data.get("skills", [])
                
            except json.JSONDecodeError as e:
                print(f"Attempt {attempt + 1} failed: Malformed JSON. Details: {e}")
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: API Error. Details: {e}")
                
            if attempt < self.max_retries - 1:
                time.sleep(self.retry_delay)
                
        return []