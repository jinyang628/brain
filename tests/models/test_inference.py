import pytest
from pydantic import ValidationError

from app.models.inference import InferenceInput
from app.models.task import Task

INFERENCE_INPUT_VALID_DATA = [
    (
        {"title": "Test", "UserMessage1": "Hello", "AssistantMessage1": "Hi"},
        [Task.SUMMARISE, Task.PRACTICE],
    ),
    (
        {"title": "Test", "UserMessage1": "Hello", "AssistantMessage1": "Hi"},
        [Task.SUMMARISE],
    ),
]


@pytest.mark.parametrize("conversation, tasks", INFERENCE_INPUT_VALID_DATA)
def test_inference_input_valid_data(conversation, tasks):
    try:
        input_data = InferenceInput(conversation=conversation, tasks=tasks)
        assert input_data.conversation == conversation
        assert input_data.tasks == tasks
    except ValidationError:
        pytest.fail(
            "Validation error raised unexpectedly for _post_entries_input_valid_data"
        )


INFERENCE_INPUT_INVALID_DATA = [
    ("test_conversation", [Task.SUMMARISE, Task.PRACTICE]),
    (123, [Task.SUMMARISE]),
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
