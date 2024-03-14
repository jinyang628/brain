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
