import logging

from app.config import InferenceConfig
from app.control.post.examiner import post_process
from app.llm.base import LLMBaseModel
from app.llm.model import LLM, LLMType
from app.models.task import Task
from app.prompts.examiner.anthropic import (
    generate_anthropic_examiner_system_message,
    generate_anthropic_examiner_user_message)
from app.prompts.examiner.cohere import (
    generate_cohere_examiner_system_message,
    generate_cohere_examiner_user_message)
from app.prompts.examiner.google_ai import (
    generate_google_ai_examiner_system_message,
    generate_google_ai_examiner_user_message)
from app.prompts.examiner.open_ai import (
    generate_open_ai_examiner_system_message,
    generate_open_ai_examiner_user_message)

log = logging.getLogger(__name__)


class Examiner:

    task = Task.PRACTICE
    _llm_type: LLMType
    _model: LLMBaseModel

    def __init__(self, config: InferenceConfig):
        self._llm_type = config.llm_type.get(self.task)
        self._model = LLM(model_type=self._llm_type).model

    def generate_system_message(self) -> str:
        match self._llm_type:
            case LLMType.OPENAI_GPT4:
                return generate_open_ai_examiner_system_message()
            case LLMType.OPENAI_GPT3_5:
                return generate_open_ai_examiner_system_message()
            case LLMType.GEMINI_PRO:
                return generate_google_ai_examiner_system_message()
            case LLMType.CLAUDE_3_SONNET:
                return generate_anthropic_examiner_system_message()
            case LLMType.CLAUDE_INSTANT_1:
                return generate_anthropic_examiner_system_message()
            case LLMType.COHERE:
                return generate_cohere_examiner_system_message()

    def generate_user_message(self, topic: str, summary_chunk: str) -> str:
        match self._llm_type:
            case LLMType.OPENAI_GPT4:
                return generate_open_ai_examiner_user_message(
                    topic=topic, summary_chunk=summary_chunk
                )
            case LLMType.OPENAI_GPT3_5:
                return generate_open_ai_examiner_user_message(
                    topic=topic, summary_chunk=summary_chunk
                )
            case LLMType.GEMINI_PRO:
                return generate_google_ai_examiner_user_message(
                    topic=topic, summary_chunk=summary_chunk
                )
            case LLMType.CLAUDE_3_SONNET:
                return generate_anthropic_examiner_user_message(
                    topic=topic, summary_chunk=summary_chunk
                )
            case LLMType.CLAUDE_INSTANT_1:
                return generate_anthropic_examiner_user_message(
                    topic=topic, summary_chunk=summary_chunk
                )
            case LLMType.COHERE:
                return generate_cohere_examiner_user_message(
                    topic=topic, summary_chunk=summary_chunk
                )

    async def examine(self, topic: str, summary_chunk: str) -> tuple[str, str, str]:
        system_message: str = self.generate_system_message()
        user_message: str = self.generate_user_message(
            topic=topic, summary_chunk=summary_chunk
        )

        try:
            response: str = await self._model.send_message(
                system_message=system_message, user_message=user_message
            )
            try:
                language, question, answer = post_process(
                    practice=response, llm_type=self._llm_type
                )
                return language, question, answer
            except ValueError as e:
                log.error(f"Error post-processing practice: {e}")
                raise e
        except Exception as e:
            log.error(f"Error occurred while generating practices off the summary: {e}")
            raise e
