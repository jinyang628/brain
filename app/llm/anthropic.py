import logging
import os

import anthropic

from app.llm.base import LLMBaseModel, LLMConfig

log = logging.getLogger(__name__)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")


class Anthropic(LLMBaseModel):
    """This class handles the interaction with Anthropic API."""

    def __init__(self, model_name: str, model_config: LLMConfig):
        super().__init__(model_name=model_name, model_config=model_config)
        self._client = anthropic.Anthropic(
            api_key=ANTHROPIC_API_KEY,
        )

    async def send_message(self, system_message: str, user_message: str) -> str:
        """Sends a message to Anthropic and returns the response."""
        messages = [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": "<output>"},
        ]

        log.info(f"Sending messages to Anthropic with messages: {messages}")
        response = self._client.messages.create(
            model=self._model_name,
            max_tokens=self._model_config.max_tokens,
            temperature=self._model_config.temperature,
            system=system_message,
            messages=messages,
        )

        if len(response.content) > 1:
            log.error(
                f"Received more than one response from Anthropic: {response.content}. Please verify"
            )
            log.error(response.content)
            raise TypeError("Received more than one response from Anthropic.")
        return response.content[0].text
