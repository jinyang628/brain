from unittest.mock import MagicMock, patch

import pytest

from app.control.pre.summariser import _split_by_token_length, pre_process
from app.models.conversation import Conversation


@pytest.fixture
def mock_tokenizer():
    mock = MagicMock()
    # Set a higher token count for each element
    mock.return_value.__getitem__.return_value = {"input_ids": [0] * 60}
    return mock


# This must match the number of XMessage in the fixture below
MOCK_TOKENIZER_CALL_COUNT = 3
# This must match the token length of the content in the fixture below
TOKEN_SPLIT_VALID_DATA = [
    (150, 1),
    (2, 2),
]


@pytest.fixture
def valid_conversation_dict():
    return {
        "title": "Test Conversation",
        "UserMessage1": "Hello",
        "AssistantMessage1": "Hi, how can I help?",
        "UserMessage2": "I need assistance with my account.",
    }


@pytest.fixture
def invalid_conversation_dict():
    return {"title": "Test Conversation", "UserMessage1": []}


@pytest.mark.parametrize(
    "max_input_tokens, expected_number_of_splits", TOKEN_SPLIT_VALID_DATA
)
def test_pre_process(
    max_input_tokens, expected_number_of_splits, mock_tokenizer, valid_conversation_dict
):
    with patch(
        "app.control.pre.summariser.AutoTokenizer.from_pretrained",
        return_value=mock_tokenizer,
    ):
        result = pre_process(
            conversation_dict=valid_conversation_dict, max_input_tokens=max_input_tokens
        )
        assert mock_tokenizer.call_count == MOCK_TOKENIZER_CALL_COUNT
        assert len(result) == expected_number_of_splits
        for conversation in result:
            assert isinstance(conversation, Conversation)


def test_pre_process_with_invalid_input(invalid_conversation_dict):
    with pytest.raises(TypeError):
        pre_process(conversation_dict=invalid_conversation_dict, max_input_tokens=100)


@pytest.mark.parametrize(
    "max_input_tokens, expected_number_of_splits", TOKEN_SPLIT_VALID_DATA
)
def test_split_by_token_length(
    max_input_tokens, expected_number_of_splits, mock_tokenizer, valid_conversation_dict
):
    with patch(
        "app.control.pre.summariser.AutoTokenizer.from_pretrained",
        return_value=mock_tokenizer,
    ):
        result = _split_by_token_length(valid_conversation_dict, max_input_tokens)
        assert mock_tokenizer.call_count == MOCK_TOKENIZER_CALL_COUNT
        assert len(result) == expected_number_of_splits
        for conversation in result:
            assert isinstance(conversation, Conversation)
