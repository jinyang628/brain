import logging

from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.llm.base import LLMBaseModel, LLMConfig

log = logging.getLogger(__name__)


class OpenAI(LLMBaseModel):
    """This class handles the interaction with OpenAI API."""

    def __init__(self, model_name: str, model_config: LLMConfig):
        super().__init__(model_name=model_name, model_config=model_config)
        self._model = ChatOpenAI(
            model_name=model_name,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
        )

    async def send_message(self, system_message: str, user_message: str) -> str:
        """Sends a message to OpenAI and returns the response."""
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_message),
        ]
        log.info(f"Sending messages to OpenAI")
        response = (await self._model.ainvoke(messages)).content
        return response
