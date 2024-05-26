import pytest
from pydantic import ValidationError

from app.models.inference import InferenceInput
from app.models.content import Content

INFERENCE_INPUT_VALID_DATA = [
    (
        {"title": "Test", "UserMessage1": "Hello", "AssistantMessage1": "Hi"},
        [Content.MCQ, Content.CODE],
    ),
    (
        {"title": "Test", "UserMessage1": "Hello", "AssistantMessage1": "Hi"},
        [Content.CODE],
    ),
]


@pytest.mark.parametrize("conversation, content", INFERENCE_INPUT_VALID_DATA)
def test_inference_input_valid_data(conversation, content):
    try:
        input_data = InferenceInput(conversation=conversation, content=content)
        assert input_data.conversation == conversation
        assert input_data.content == content
    except ValidationError:
        pytest.fail(
            "Validation error raised unexpectedly for _post_entries_input_valid_data"
        )


INFERENCE_INPUT_INVALID_DATA = [
    ("test_conversation", [Content.MCQ, Content.CODE]),
    (123, [Content.CODE]),
    (
        {
            "title": "test_title",
            "UserMessage1": "First message",
            "AssistantMessage1": "Second message",
        },
        "task_summarise",
    ),
]


@pytest.mark.parametrize("conversation, tasks", INFERENCE_INPUT_INVALID_DATA)
def test_inference_input_invalid_data(conversation, tasks):
    with pytest.raises(ValidationError):
        InferenceInput(conversation=conversation, tasks=tasks)
