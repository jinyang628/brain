from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

from app.llm.anthropic import AWSBedrock
from app.llm.base import LLMBaseModel, LLMConfig
from app.llm.google_ai import GoogleAI
from app.llm.open_ai import OpenAI


class LLMType(StrEnum):
    OPENAI_GPT4 = "gpt-4-0125-preview"
    OPENAI_GPT3_5 = "gpt-3.5-turbo-0125"
    GEMINI_PRO = "gemini-pro"
    # AWS_BEDROCK_CLAUDE_3_SONNET = "anthropic.claude-3-sonnet-20240229-v1:0"
    CLAUDE_3_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_INSTANT_1 = "claude-instant-1.2"

    def default_config(self) -> LLMConfig:
        if self == LLMType.OPENAI_GPT4:
            return LLMConfig(
                temperature=0.7,
                max_tokens=100,
            )
        elif self == LLMType.OPENAI_GPT3_5:
            return LLMConfig(
                temperature=0.7,
                max_tokens=100,
            )
        elif self == LLMType.GEMINI_PRO:
            return LLMConfig(
                temperature=1,
                max_tokens=10000,
            )
        elif self == LLMType.CLAUDE_3_SONNET:
            return LLMConfig(
                temperature=1,
                max_tokens=4096,
            )
        elif self == LLMType.CLAUDE_INSTANT_1:
            return LLMConfig(
                temperature=1,
                max_tokens=4096,
            )
        raise ValueError(f"Unsupported LLM type: {self}")


@dataclass
class LLM:
    """Wrapper class for the LLM models."""

    _model: LLMBaseModel

    def __init__(
        self,
        model_type: LLMType,
        model_config: Optional[LLMConfig] = None,
    ):
        model_config: LLMConfig = model_config or model_type.default_config()
        match model_type:
            case LLMType.OPENAI_GPT4:
                self._model = OpenAI(
                    model_name=model_type.value, model_config=model_config
                )
            case LLMType.OPENAI_GPT3_5:
                self._model = OpenAI(
                    model_name=model_type.value, model_config=model_config
                )
            case LLMType.GEMINI_PRO:
                self._model = GoogleAI(
                    model_name=model_type.value, model_config=model_config
                )
            case LLMType.CLAUDE_3_SONNET:
                self._model = AWSBedrock(
                    model_name=model_type.value, model_config=model_config
                )
            case LLMType.CLAUDE_INSTANT_1:
                self._model = AWSBedrock(
                    model_name=model_type.value, model_config=model_config
                )

    @property
    def model(self) -> LLMBaseModel:
        return self._model
