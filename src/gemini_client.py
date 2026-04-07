import warnings
from typing import Optional

from google import genai
from google.genai import types

from . import config
from .llm_client import LLMClient


class GeminiClient(LLMClient):
    """Google Gemini implementation of the LLM client."""

    def __init__(self, model_name: Optional[str] = None) -> None:
        if not config.LLM_API_KEY:
            raise ValueError("LLM_API_KEY environment variable is not set.")
        
        self.client = genai.Client(api_key=config.LLM_API_KEY)
        self.model_name = model_name or config.LLM_MODEL_NAME

        warnings.filterwarnings("ignore", message=".*non-text parts in the response.*")

    def generate_text(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=config.LLM_TEMPERATURE,
            )
        )
        return response.text