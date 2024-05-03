import json
import logging
from typing import Any
from openai import OpenAI
import os

from app.exceptions.exception import InferenceFailure
from app.llm.base import LLMBaseModel, LLMConfig
from app.prompts.config import PromptMessageConfig
from app.prompts.summariser.functions import get_summary_functions, SummaryFunctions

log = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

class OpenAi(LLMBaseModel):
    """This class handles the interaction with OpenAI API."""


    def __init__(self, model_name: str, model_config: LLMConfig):
        super().__init__(model_name=model_name, model_config=model_config)
        self._client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

    async def send_message(self, system_message: str, user_message: str, config: PromptMessageConfig) -> Any:
        """Sends a message to OpenAI and returns the response."""
        
        log.info(f"Sending messages to OpenAI")
        match config:
            case PromptMessageConfig.SUMMARY:
                response = self._client.chat.completions.create(
                    model = self._model_name,
                    messages = [
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message}
                    ],
                    functions=get_summary_functions(),
                    function_call = {"name": SummaryFunctions.GET_SUMMARY}
                )
                try:
                    json_response: dict[str, str] = json.loads(response.choices[0].message.function_call.arguments)
                    topic: str = json_response[SummaryFunctions.TOPIC]
                    content: str = json_response[SummaryFunctions.CONTENT]
                    log.info(f"Topic: {topic}, Content: {content}")
                    return (topic, content)
                except Exception as e:
                    log.error(f"Error processing or receiving OpenAI response: {str(e)}")
                    raise InferenceFailure("Error processing OpenAI response")
            case PromptMessageConfig.PRACTICE:
                pass
            case _:
                raise InferenceFailure("Invalid config type")
            
        
