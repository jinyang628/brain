from abc import ABC, abstractmethod

from pydantic import BaseModel


class LLMConfig(BaseModel):
    temperature: float
    max_tokens: int


class LLMBaseModel(ABC):
    """Base class for all AI models."""

    model_name: str
    model_config: LLMConfig

    def __init__(self, model_name: str, model_config: LLMConfig):
        if not model_name:
            raise ValueError("Model name must be provided.")
        if not model_config:
            raise ValueError("Model config must be provided.")

        self.model_name = model_name
        self.model_config = model_config

    @abstractmethod
    async def send_message(
        self,
        message: str,
    ) -> str:
        """Sends a message to the AI and returns the response."""
        pass
