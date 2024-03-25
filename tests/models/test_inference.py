import uuid

import pytest
from pydantic import ValidationError

from app.models.inference import InferenceInput

ID_DATA = [
    (
        {"_id": "12345", "user_id": str(uuid.uuid4()), "messages": {"msg1": "Hello"}},
        True,
    ),
    ({"user_id": str(uuid.uuid4()), "messages": {"msg1": "Hello"}}, False),
]


@pytest.mark.parametrize("input_data, expected", ID_DATA)
def test_id_field_with_alias(input_data, expected):
    if expected:
        try:
            InferenceInput(**input_data)
        except ValidationError:
            pytest.fail("Unexpected ValidationError raised")
    else:
        with pytest.raises(ValidationError):
            InferenceInput(**input_data)


USER_ID_DATA = [
    (
        {"_id": "12345", "user_id": str(uuid.uuid4()), "messages": {"msg1": "Hello"}},
        True,
    ),
    (
        {"_id": "12345", "user_id": "not-a-uuid", "messages": {"msg1": "Hello"}},
        False,  # Non-uuid value
    ),
]


@pytest.mark.parametrize("input_data, expected", USER_ID_DATA)
def test_user_id_field(input_data, expected):
    if expected:
        try:
            InferenceInput(**input_data)
        except ValidationError:
            pytest.fail("Unexpected ValidationError raised")
    else:
        with pytest.raises(ValidationError):
            InferenceInput(**input_data)


MESSAGES_DATA = [
    (
        {"_id": "12345", "user_id": str(uuid.uuid4()), "messages": {"msg1": "Hello"}},
        True,
    ),
    (
        {"_id": "12345", "user_id": str(uuid.uuid4()), "messages": {"msg1": 123}},
        False,  # Non-string value
    ),
]


@pytest.mark.parametrize("input_data, expected", MESSAGES_DATA)
def test_messages_field(input_data, expected):
    if expected:
        try:
            InferenceInput(**input_data)
        except ValidationError:
            pytest.fail("Unexpected ValidationError raised")
    else:
        with pytest.raises(ValidationError):
            InferenceInput(**input_data)



   
# INFERENCE_INPUT_VALID_DATA = [
#     (
#         {
#             "title": "test_title",
#             "UserMessage1": "First message",
#             "AssistantMessage1": "Second message",
#         },
#         [Task.SUMMARISE]
#     ),
#     (
#         {
#             "title": "test_title",
#             "UserMessage1": "First message",
#             "AssistantMessage1": "Second message",
#         },
#         [Task.SUMMARISE, Task.PRACTICE]
#     )
# ]

# @pytest.mark.parametrize("conversation, tasks", INFERENCE_INPUT_VALID_DATA)
# def test_inference_input_valid_data(conversation, tasks):
#     try:
#         input_data = InferenceInput(conversation=conversation, tasks=tasks)
#         assert input_data.conversation == conversation
#         assert input_data.tasks == tasks
#     except ValidationError:
#         pytest.fail("Validation error raised unexpectedly for _post_entries_input_valid_data")
    
# INFERENCE_INPUT_INVALID_DATA = [
#     (
#         "test_conversation", 
#         [Task.SUMMARISE, Task.PRACTICE]
#     ),
#     (
#         123, 
#         [Task.SUMMARISE]
#     ),
#     (
#         {
#             "title": "test_title",
#             "UserMessage1": "First message",
#             "AssistantMessage1": "Second message",
#         },
#         "task_summarise"
#     )
# ]

# @pytest.mark.parametrize("conversation, tasks", INFERENCE_INPUT_INVALID_DATA)
# def test_inference_input_invalid_data(conversation, tasks):
#     with pytest.raises(ValidationError):
#         InferenceInput(conversation=conversation, tasks=tasks)
        
       