import pytest

from app.control.post.examiner import (_determine_question_and_answer,
                                       _extract_code, post_process)

EXTRACT_CODE_VALID_DATA = [
    (
        "```python\nprint('Hello')```\n```python\n# TODO: Add the missing line below.```",
        ("python", "print('Hello')", "# TODO: Add the missing line below."),
    ),
]


@pytest.mark.parametrize("text, expected", EXTRACT_CODE_VALID_DATA)
def test_valid_extract_code(text, expected):
    language, block_1, block_2 = _extract_code(text)
    assert (language, block_1, block_2) == expected


EXTRACT_CODE_INVALID_DATA = [
    ("Some random text"),
]


@pytest.mark.parametrize("text", EXTRACT_CODE_INVALID_DATA)
def test_invalid_extract_code(text):
    with pytest.raises(ValueError):
        _extract_code(text)


# Define test data for _determine_question_and_answer
DETERMINE_QUESTION_AND_ANSWER_VALID_DATA = [
    (
        "def function(): print('Hello')",
        "def test(): # TODO: Add the missing line below.",
        (
            "def test(): # TODO: Add the missing line below.",
            "def function(): print('Hello')",
        ),
    ),
]


@pytest.mark.parametrize(
    "block_1, block_2, expected", DETERMINE_QUESTION_AND_ANSWER_VALID_DATA
)
def test_valid_determine_question_and_answer(block_1, block_2, expected):
    question, answer = _determine_question_and_answer(block_1, block_2)
    assert (question, answer) == expected


DETERMINE_QUESTION_AND_ANSWER_INVALID_DATA = [
    ("def function(): print('Hello')", "def test(): print('World')"),
    ("print('Hello') # TODO: Add the missing line", "print('World')"),
]


@pytest.mark.parametrize("block_1, block_2", DETERMINE_QUESTION_AND_ANSWER_INVALID_DATA)
def test_invalid_determine_question_and_answer(block_1, block_2):
    with pytest.raises(ValueError):
        _determine_question_and_answer(block_1, block_2)


POST_PROCESS_VALID_DATA = [
    (
        "```python\ndef test(): print('Hello')```\n```python\ndef love_coding(): # TODO: Add the missing line below.```",
        (
            "python",
            "def love_coding(): # TODO: Add the missing line below.",
            "def test(): print('Hello')",
        ),
    ),
]


@pytest.mark.parametrize("practice, expected", POST_PROCESS_VALID_DATA)
def test_valid_post_process(practice, expected):
    language, question, answer = post_process(practice)
    assert (language, question, answer) == expected


POST_PROCESS_INVALID_DATA = [
    ("Some random text"),
]


@pytest.mark.parametrize("practice", POST_PROCESS_INVALID_DATA)
def test_invalid_post_process(practice):
    with pytest.raises(ValueError):
        post_process(practice)
