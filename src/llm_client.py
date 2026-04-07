from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Abstract base class for LLM client implementations."""

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        pass