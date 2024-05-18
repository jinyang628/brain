import json
import logging
from typing import Any
from openai import OpenAI
import os

from app.exceptions.exception import InferenceFailure
from app.llm.base import LLMBaseModel, LLMConfig
from app.prompts.config import PromptMessageConfig
from app.prompts.examiner.functions import PracticeFunctions, get_practice_functions
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
                    goal: str = json_response[SummaryFunctions.GOAL]
                    overview: str = json_response[SummaryFunctions.OVERVIEW]
                    key_concepts_lst: list = []
                    for key_concept in json_response[SummaryFunctions.KEY_CONCEPTS]:
                        key_concepts_lst.append({
                            SummaryFunctions.KEY_CONCEPT_HEADER.value: key_concept[SummaryFunctions.KEY_CONCEPT_HEADER],
                            SummaryFunctions.KEY_CONCEPT_CONTENT.value: key_concept[SummaryFunctions.KEY_CONCEPT_CONTENT],
                            SummaryFunctions.KEY_CONCEPT_CODE_EXAMPLE.value: key_concept.get(SummaryFunctions.KEY_CONCEPT_CODE_EXAMPLE)
                        })
                        
                    
                    log.info(f"Topic: {topic}, Goal: {goal} Overview: {overview}, Key concepts: {key_concepts_lst}")
                    return (topic, goal, overview, key_concepts_lst)
                except Exception as e:
                    log.error(f"Error processing or receiving OpenAI response: {str(e)}")
                    raise InferenceFailure("Error processing OpenAI response")
            case PromptMessageConfig.PRACTICE:
                response = self._client.chat.completions.create(
                    model = self._model_name,
                    messages = [
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message}
                    ],
                    functions=get_practice_functions(),
                    function_call = {"name": PracticeFunctions.GET_PRACTICE}
                )
                try:
                    json_response: dict[str, str] = json.loads(response.choices[0].message.function_call.arguments)
                    log.info(f"Practice: {json_response}")
                    language: str = json_response[PracticeFunctions.LANGUAGE]
                    question: str = json_response[PracticeFunctions.QUESTION]
                    half_completed_code: str = json_response[PracticeFunctions.HALF_COMPLETED_CODE]
                    fully_completed_code: str = json_response[PracticeFunctions.FULLY_COMPLETED_CODE]
                    log.info(f"Language: {language}, Question: {question}, Half-completed-code: {half_completed_code}, Fully-completed-code: {fully_completed_code}")
                    return (language, question, half_completed_code, fully_completed_code)
                except Exception as e:
                    log.error(f"Error processing or receiving OpenAI response: {str(e)}")
                    raise InferenceFailure("Error processing OpenAI response")
            case _:
                raise InferenceFailure("Invalid config type")
            
        
