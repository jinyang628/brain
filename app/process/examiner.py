import logging

from app.config import InferenceConfig
from app.control.post.examiner import post_process
from app.llm.base import LLMBaseModel
from app.llm.model import LLM, LLMType
from app.prompts.examiner.google_ai import generate_google_ai_examiner_system_message, generate_google_ai_examiner_user_message

log = logging.getLogger(__name__)

class Examiner:

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
                return generate_google_ai_examiner_system_message()
            case LLMType.AWS_BEDROCK_CLAUDE_3_SONNET:
                # TODO
                pass    
            
    def generate_user_message(self, topic: str, content: str) -> str:
        match self._llm_type:
            case LLMType.OPENAI_GPT4:
                # TODO
                pass
            case LLMType.OPENAI_GPT3_5:
                # TODO
                pass
            case LLMType.GEMINI_PRO:
                return generate_google_ai_examiner_user_message(
                    topic=topic,
                    content=content
                )
            case LLMType.AWS_BEDROCK_CLAUDE_3_SONNET:
                # TODO
                pass
    
    async def examine(self, topic: str, content: str) -> tuple[str, str, str]:    
        system_message: str = self.generate_system_message()
        user_message: str = self.generate_user_message(
            topic=topic, 
            content=content
        )
        
        try:
            response: str = await self._model.send_message(
                system_message=system_message, 
                user_message=user_message
            )
            try:
                language, question, answer = post_process(practice=response)
                return language, question, answer 
            except ValueError as e:
                log.error(f"Error post-processing practice: {e}")
                raise e
        except Exception as e:
            log.error(f"Error occurred while generating practices off the summary: {e}")
            raise e