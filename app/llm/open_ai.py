import json
import logging
from typing import Any, Optional
from openai import OpenAI
import os

from app.exceptions.exception import InferenceFailure
from app.llm.base import LLMBaseModel, LLMConfig
from app.models.content import Content
from app.prompts.config import PromptMessageConfig
from app.prompts.generator.functions import get_notes_functions, NotesFunctions

log = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

class OpenAi(LLMBaseModel):
    """This class handles the interaction with OpenAI API."""


    def __init__(self, model_name: str, model_config: LLMConfig):
        super().__init__(model_name=model_name, model_config=model_config)
        self._client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

    async def send_message(self, system_message: str, user_message: str, content_lst: list[Content]) -> Any:
        """Sends a message to OpenAI and returns the response."""
        
        log.info(f"Sending messages to OpenAI")
        try:
            response = self._client.chat.completions.create(
                model = self._model_name,
                messages = [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                functions=get_notes_functions(
                    contains_mcq_practice=bool(Content.MCQ in content_lst),
                    contains_code_practice=bool(Content.CODE in content_lst)
                ),
                function_call = {"name": NotesFunctions.GET_NOTES}
            )
            try:
                json_response: dict[str, str] = json.loads(response.choices[0].message.function_call.arguments)
                print("~~~LLM RESPONSE~~~")
                print(json_response)
                topic: str = json_response[NotesFunctions.TOPIC]
                goal: str = json_response[NotesFunctions.GOAL]
                context: str = json_response[NotesFunctions.CONTEXT]
                overview: str = json_response[NotesFunctions.OVERVIEW]
                
                key_concepts_lst: list = []
                for key_concept in json_response[NotesFunctions.KEY_CONCEPTS]:
                    code_example: Optional[dict[str, str]] = key_concept.get(NotesFunctions.KEY_CONCEPT_CODE_EXAMPLE)
                    if code_example:
                        key_concepts_lst.append({
                            NotesFunctions.KEY_CONCEPT_TITLE.value: key_concept[NotesFunctions.KEY_CONCEPT_TITLE],
                            NotesFunctions.KEY_CONCEPT_EXPLANATION.value: key_concept[NotesFunctions.KEY_CONCEPT_EXPLANATION],
                            NotesFunctions.KEY_CONCEPT_CODE_EXAMPLE.value: {
                                NotesFunctions.KEY_CONCEPT_CODE.value: code_example[NotesFunctions.KEY_CONCEPT_CODE],
                                NotesFunctions.KEY_CONCEPT_LANGUAGE.value: code_example[NotesFunctions.KEY_CONCEPT_LANGUAGE]
                            }
                        })
                    else:
                        key_concepts_lst.append({
                            NotesFunctions.KEY_CONCEPT_TITLE.value: key_concept[NotesFunctions.KEY_CONCEPT_TITLE],
                            NotesFunctions.KEY_CONCEPT_EXPLANATION.value: key_concept[NotesFunctions.KEY_CONCEPT_EXPLANATION],
                        })
                        
                tips_lst: list = []
                tips: Optional[list[dict[str, str]]] = json_response.get(NotesFunctions.TIPS)
                if tips:
                    for tip in tips:
                        tips_lst.append({
                            NotesFunctions.TIP_TITLE.value: tip[NotesFunctions.TIP_TITLE],
                            NotesFunctions.TIP_EXPLANATION.value: tip[NotesFunctions.TIP_EXPLANATION]
                        })     
                        
                mcq_practice: Optional[dict[str, str]] = json_response.get(NotesFunctions.MCQ_PRACTICE)
                if mcq_practice:
                    mcq_practice = {
                        NotesFunctions.MCQ_PRACTICE_TITLE.value: mcq_practice[NotesFunctions.MCQ_PRACTICE_TITLE],
                        NotesFunctions.MCQ_PRACTICE_QUESTION.value: mcq_practice[NotesFunctions.MCQ_PRACTICE_QUESTION],
                        NotesFunctions.MCQ_PRACTICE_WRONG_OPTIONS.value: mcq_practice[NotesFunctions.MCQ_PRACTICE_WRONG_OPTIONS],
                        NotesFunctions.MCQ_PRACTICE_CORRECT_OPTION.value: mcq_practice[NotesFunctions.MCQ_PRACTICE_CORRECT_OPTION]
                    }     
                
                code_practice: Optional[dict[str, str]] = json_response.get(NotesFunctions.CODE_PRACTICE)
                if code_practice:
                    code_practice = {
                        NotesFunctions.CODE_PRACTICE_TITLE.value: code_practice[NotesFunctions.CODE_PRACTICE_TITLE],
                        NotesFunctions.CODE_PRACTICE_QUESTION.value: code_practice[NotesFunctions.CODE_PRACTICE_QUESTION],
                        NotesFunctions.CODE_PRACTICE_HALF_COMPLETED_CODE.value: code_practice[NotesFunctions.CODE_PRACTICE_HALF_COMPLETED_CODE],
                        NotesFunctions.CODE_PRACTICE_FULLY_COMPLETED_CODE.value: code_practice[NotesFunctions.CODE_PRACTICE_FULLY_COMPLETED_CODE],
                        NotesFunctions.CODE_PRACTICE_LANGUAGE.value: code_practice[NotesFunctions.CODE_PRACTICE_LANGUAGE]
                    }
                
                log.info(f"Topic: {topic}, Goal: {goal}, Context: {context}, Overview: {overview}, Key concepts: {key_concepts_lst}, Tips: {tips_lst}, MCQ Practice: {mcq_practice}, Code Practice: {code_practice}")
                return (topic, goal, context, overview, key_concepts_lst, tips_lst, mcq_practice, code_practice)
            except Exception as e:
                log.error(f"Error processing or receiving OpenAI response: {str(e)}")
                raise InferenceFailure("Error processing OpenAI response")
        except Exception as e:
            log.error(f"Error sending message to OpenAI: {str(e)}")
            raise InferenceFailure("Error sending message to OpenAI")
            
        
