import logging

from app.config import InferenceConfig
from app.llm.base import LLMBaseModel
from app.llm.model import LLM, LLMType
from app.models.conversation import Conversation
from app.prompts.summariser.google_ai import (
    generate_google_ai_summariser_system_message,
    generate_google_ai_summariser_user_message,
)

log = logging.getLogger(__name__)


class Summarizer:

    _llm_type: LLMType
    _model: LLMBaseModel

    def __init__(self, config: InferenceConfig):
        self._llm_type = config.llm_type
        self._model = LLM(model_type=self._llm_type).model

    def generate_system_message(self) -> str:
        match self._llm_type:
            case LLMType.OPENAI_GPT4:
                # TODO
                pass
            case LLMType.OPENAI_GPT3_5:
                # TODO
                pass
            case LLMType.GEMINI_PRO:
                return generate_google_ai_summariser_system_message()
            case LLMType.AWS_BEDROCK_CLAUDE_3_SONNET:
                # TODO
                pass

    def generate_user_message(self, conversation: Conversation) -> str:
        match self._llm_type:
            case LLMType.OPENAI_GPT4:
                # TODO
                pass
            case LLMType.OPENAI_GPT3_5:
                # TODO
                pass
            case LLMType.GEMINI_PRO:
                return generate_google_ai_summariser_user_message(
                    conversation=conversation
                )
            case LLMType.AWS_BEDROCK_CLAUDE_3_SONNET:
                # TODO
                pass

    async def summarize(self, conversation: Conversation) -> str:
        system_message: str = self.generate_system_message()
        user_message: str = self.generate_user_message(conversation=conversation)

        try:
            response: str = await self._model.send_message(
                system_message=system_message, user_message=user_message
            )

            return response

        except Exception as e:
            log.error(f"Error occurred while summarizing conversation: {e}")
            raise e
