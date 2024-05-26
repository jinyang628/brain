import pytest

from app.config import InferenceConfig
from app.llm.model import LLMType

@pytest.fixture
def config():
    return InferenceConfig()

def test_inference_config_initialization(config):
    """Test the default initialization of InferenceConfig."""
    assert config.llm_type == LLMType.OPENAI_GPT4