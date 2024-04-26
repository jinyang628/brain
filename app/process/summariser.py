import logging
from typing import Any

from app.config import InferenceConfig
from app.control.post.summariser import post_process
from app.control.pre.summariser import pre_process
from app.exceptions.exception import LogicError
from app.llm.base import LLMBaseModel
from app.llm.model import LLM, LLMType
from app.models.conversation import Conversation
from app.models.task import Task
from app.prompts.summariser.anthropic import (
    generate_anthropic_summariser_system_message,
    generate_anthropic_summariser_user_message)
from app.prompts.summariser.cohere import (
    generate_cohere_summariser_system_message,
    generate_cohere_summariser_user_message)
from app.prompts.summariser.google_ai import (
    generate_google_ai_summariser_system_message,
    generate_google_ai_summariser_user_message)
from app.prompts.summariser.llama3 import generate_llama3_summariser_system_message, generate_llama3_summariser_user_message
from app.prompts.summariser.open_ai import (
    generate_open_ai_summariser_system_message,
    generate_open_ai_summariser_user_message)

log = logging.getLogger(__name__)


class Summariser:

    TASK = Task.SUMMARISE
    
    _llm_type: LLMType
    _model: LLMBaseModel
    _max_tokens: int

    def __init__(self, config: InferenceConfig):
        self._llm_type = config.llm_type.get(self.TASK)
        self._model = LLM(model_type=self._llm_type).model
        self._max_tokens = self._model.model_config.max_tokens

    def generate_system_message(self) -> str:
        match self._llm_type:
            case LLMType.OPENAI_GPT4_TURBO:
                return generate_open_ai_summariser_system_message()
            case LLMType.OPENAI_GPT3_5:
                return generate_open_ai_summariser_system_message()
            case LLMType.GEMINI_PRO:
                return generate_google_ai_summariser_system_message()
            case LLMType.CLAUDE_3_SONNET:
                return generate_anthropic_summariser_system_message()
            case LLMType.CLAUDE_INSTANT_1:
                return generate_anthropic_summariser_system_message()
            case LLMType.COHERE_COMMAND_R:
                return generate_cohere_summariser_system_message()
            case LLMType.COHERE_COMMAND_R_PLUS:
                return generate_cohere_summariser_system_message()
            case LLMType.LLAMA3:
                return generate_llama3_summariser_system_message()

    def generate_user_message(self, conversation: Conversation) -> str:
        match self._llm_type:
            case LLMType.OPENAI_GPT4_TURBO:
                return generate_open_ai_summariser_user_message(
                    conversation=conversation
                )
            case LLMType.OPENAI_GPT3_5:
                return generate_open_ai_summariser_user_message(
                    conversation=conversation
                )
            case LLMType.GEMINI_PRO:
                return generate_google_ai_summariser_user_message(
                    conversation=conversation
                )
            case LLMType.CLAUDE_3_SONNET:
                return generate_anthropic_summariser_user_message(
                    conversation=conversation
                )
            case LLMType.CLAUDE_INSTANT_1:
                return generate_anthropic_summariser_user_message(
                    conversation=conversation
                )
            case LLMType.COHERE_COMMAND_R:
                return generate_cohere_summariser_user_message(
                    conversation=conversation
                )
            case LLMType.COHERE_COMMAND_R_PLUS:
                return generate_cohere_summariser_user_message(
                    conversation=conversation
                )
            case LLMType.LLAMA3:
                return generate_llama3_summariser_user_message(
                    conversation=conversation
                )

    def pre_process(
        self, conversation_dict: dict[str, Any]
    ) -> tuple[list[Conversation], int]:
        """Pre-processes the conversation given the summarisation model's max tokens limit. 
        
        The conversation will be split up into multiple conversation chunks if it exceeds the max tokens limit.

        Args:
            conversation_dict (dict[str, Any]): The user's conversation chatlog.

        Returns:
            tuple[list[Conversation], int]: The list of conversation chunks and the total token sum of the conversation.
        """
        conversation_lst, token_sum = pre_process(
            conversation_dict=conversation_dict, max_input_tokens=self._max_tokens
        )
        log.info(f"Length of conversation list: {len(conversation_lst)} post split")
        log.info(f"Token sum of conversation: {token_sum}")
        return conversation_lst, token_sum

    async def summarise(self, conversation: Conversation) -> str:
        """Invokes the LLM to generate a summary of the conversation.

        Args:
            conversation (Conversation): The conversation to be summarised.
            
        Returns:
            str: A string containing the summary of the conversation.
        """
        system_message: str = self.generate_system_message()
        user_message: str = self.generate_user_message(conversation=conversation)

        try:
            response: str = await self._model.send_message(
                system_message=system_message, user_message=user_message
            )
            processed_summary: dict[str, str] = post_process(
                summary=response, llm_type=self._llm_type
            )
            log.info(f"Processed Summary: {processed_summary}")
            return processed_summary
        except LogicError as e:
            log.error(f"Logic error occurred while summarizing conversation: {e}")
            raise e
        except Exception as e:
            log.error(f"Error occurred while summarizing conversation: {e}")
            raise e
