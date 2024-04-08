import pytest
from app.models.task import Task


def test_enum_values():
    assert Task.SUMMARISE == "summarise"
    assert Task.PRACTICE == "practice"


VALIDATE_VALID_DATA = [
    (["summarise"], [Task.SUMMARISE]),
    (["practice"], [Task.PRACTICE]),
    (["summarise", "practice"], [Task.SUMMARISE, Task.PRACTICE]),
]


@pytest.mark.parametrize("input, expected", VALIDATE_VALID_DATA)
def test_validate_valid(input, expected):
    assert Task.validate(input) == expected


VALIDATE_INVALID_DATA = [
    ["unknown"],
    ["summarise", "unknown"],
]


# Test for invalid input
@pytest.mark.parametrize("invalid_input", VALIDATE_INVALID_DATA)
def test_validate_invalid(invalid_input):
    with pytest.raises(ValueError):
        Task.validate(invalid_input)
