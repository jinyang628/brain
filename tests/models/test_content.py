import pytest

from app.models.content import Content


def test_enum_values():
    assert Content.MCQ == "mcq"
    assert Content.CODE == "code"


VALIDATE_VALID_DATA = [
    (["mcq"], [Content.MCQ]),
    (["code"], [Content.CODE]),
    (["mcq", "code"], [Content.MCQ, Content.CODE]),
]


@pytest.mark.parametrize("input, expected", VALIDATE_VALID_DATA)
def test_validate_valid(input, expected):
    assert Content.validate(input) == expected


VALIDATE_INVALID_DATA = [
    ["unknown"],
    ["mcq", "unknown"],
]


# Test for invalid input
@pytest.mark.parametrize("invalid_input", VALIDATE_INVALID_DATA)
def test_validate_invalid(invalid_input):
    with pytest.raises(ValueError):
        Content.validate(invalid_input)
