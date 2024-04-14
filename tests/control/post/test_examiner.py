import pytest

from app.control.post.examiner import (_determine_question_and_answer,
                                       _extract_code, post_process)
from app.control.post.summariser import _remove_output_wrapper
from app.llm.model import LLMType

EXTRACT_CODE_VALID_DATA = [
    (
        "```python\nprint('Hello')```\n```python\n# TODO: Add the missing line(s) below.```",
        ("python", "print('Hello')", "# TODO: Add the missing line(s) below."),
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
        "def test(): # TODO: Add the missing line(s) below.",
        (
            "def test(): # TODO: Add the missing line(s) below.",
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
        "```python\ndef test(): print('Hello')```\n```python\ndef love_coding(): # TODO: Add the missing line(s) below.```",
        LLMType.GEMINI_PRO,
        (
            "python",
            "def love_coding(): # TODO: Add the missing line(s) below.",
            "def test(): print('Hello')",
        ),
    ),
    (
        "```python\ndef test(): print('Hello')```\n```python\ndef love_coding(): # TODO: Add the missing line(s) below.```</output>",
        LLMType.CLAUDE_3_SONNET,
        (
            "python",
            "def love_coding(): # TODO: Add the missing line(s) below.",
            "def test(): print('Hello')",
        ),
    ),
    (
        "```python\ndef test(): print('Hello')```\n```python\ndef love_coding(): # TODO: Add the missing line(s) below.```</output>",
        LLMType.CLAUDE_INSTANT_1,
        (
            "python",
            "def love_coding(): # TODO: Add the missing line(s) below.",
            "def test(): print('Hello')",
        ),
    ),
]


@pytest.mark.parametrize("practice, llm_type, expected", POST_PROCESS_VALID_DATA)
def test_valid_post_process(practice, llm_type, expected):
    language, question, answer = post_process(practice=practice, llm_type=llm_type)
    assert (language, question, answer) == expected


POST_PROCESS_INVALID_DATA = [
    (
        "Some random text",
        LLMType.GEMINI_PRO,
    ),
    (
        "Some random text",
        LLMType.CLAUDE_3_SONNET,
    ),
]


@pytest.mark.parametrize("practice, llm_type", POST_PROCESS_INVALID_DATA)
def test_invalid_post_process(practice, llm_type):
    with pytest.raises(ValueError):
        post_process(practice=practice, llm_type=llm_type)


REMOVE_OUTPUT_WRAPPER_DATA = [
    ("This is the output. </output>", "This is the output."),
    ("This is the output. </output>\nProbably rubbish", "This is the output."),
    ("This is the output. </output>testetstest", "This is the output."),
]


@pytest.mark.parametrize("input_str, expected", REMOVE_OUTPUT_WRAPPER_DATA)
def test_remove_output_wrapper(input_str, expected):
    assert _remove_output_wrapper(input_str) == expected
