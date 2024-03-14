import pytest

from app.models.conversation import Conversation

VALID_KEYS_DATA = [
    ({"title": "Test", "UserMessage1": "Hello", "AssistantMessage1": "Hi"}, True),
    ({"title": "Another Test", "UserMessage1": "What's up?"}, True),
]


@pytest.mark.parametrize("input_data, expected", VALID_KEYS_DATA)
def test_root_validator_valid(input_data, expected):
    try:
        Conversation(**input_data)
    except ValueError:
        assert not expected
    else:
        assert expected


INVALID_KEYS_DATA = [
    ({"title": "Test", "InvalidKey": "This should fail"}),
    ({"TITLE": "Test", "UserMessage1": "This should fail"}),
]


@pytest.mark.parametrize("input_data", INVALID_KEYS_DATA)
def test_root_validator_invalid(input_data):
    with pytest.raises(ValueError):
        Conversation(**input_data)
