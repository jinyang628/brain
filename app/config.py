from pydantic import BaseModel

from app.llm.model import LLMType
from app.models.task import Task


class InferenceConfig(BaseModel):
    """The main class describing the inference configuration."""

    llm_type: dict[Task, LLMType] = {    
        # Task.SUMMARISE: LLMType.GEMINI_PRO,  
        Task.SUMMARISE: LLMType.OPENAI_GPT3_5,
        # Task.PRACTICE: LLMType.OPENAI_GPT4_TURBO
        # Task.PRACTICE: LLMType.COHERE_COMMAND_R_PLUS
        Task.PRACTICE: LLMType.OPENAI_GPT3_5
        # Task.PRACTICE: LLMType.GEMINI_PRO
    }
