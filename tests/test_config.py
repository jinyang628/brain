from marshmallow import ValidationError
import pytest

from app.config import InferenceConfig
from app.llm.model import LLMType
from app.models.task import Task

@pytest.fixture
def config():
    return InferenceConfig()

def test_inference_config_initialization(config):
    """Test the default initialization of InferenceConfig."""
    assert Task.SUMMARISE in config.llm_type
    assert Task.PRACTICE in config.llm_type
    assert config.llm_type[Task.SUMMARISE] == LLMType.GEMINI_PRO
    assert config.llm_type[Task.PRACTICE] == LLMType.OPENAI_GPT3_5