import logging
import os

import cohere
from dotenv import load_dotenv

from app.llm.base import LLMBaseModel, LLMConfig

load_dotenv()

log = logging.getLogger(__name__)

COHERE_API_KEY = os.environ.get("COHERE_API_KEY")


class Cohere(LLMBaseModel):
    """This class handles the interaction with Cohere API."""

    def __init__(self, model_name: str, model_config: LLMConfig):
        super().__init__(model_name=model_name, model_config=model_config)
        self._co = cohere.Client(COHERE_API_KEY)

    async def send_message(self, system_message: str, user_message: str) -> str:
        """Sends a message to Cohere and returns the response."""
        messages = [
            {"role": "SYSTEM", "message": system_message},
        ]

        log.info(f"Sending messages to Cohere")
        response = self._co.chat(
            chat_history=messages,
            message=user_message,
            max_tokens=self._model_config.max_tokens,
            temperature=self._model_config.temperature,
        )
        return response.text
