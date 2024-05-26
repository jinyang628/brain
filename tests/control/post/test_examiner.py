# import pytest

# from app.control.post.examiner import (_determine_question_and_answer,
#                                        _extract_code, post_process)
# from app.exceptions.exception import LogicError
# from app.llm.model import LLMType

# EXTRACT_CODE_VALID_DATA = [
#     (
#         "```python\nprint('Hello')```\n```python\n# TODO: Add the missing line(s) below.```",
#         ("python", "print('Hello')", "# TODO: Add the missing line(s) below."),
#     ),
# ]


# @pytest.mark.parametrize("text, expected", EXTRACT_CODE_VALID_DATA)
# def test_valid_extract_code(text, expected):
#     language, block_1, block_2 = _extract_code(text)
#     assert (language, block_1, block_2) == expected


# EXTRACT_CODE_INVALID_DATA = [
#     ("Some random text"),
# ]


# @pytest.mark.parametrize("text", EXTRACT_CODE_INVALID_DATA)
# def test_invalid_extract_code(text):
#     with pytest.raises(ValueError):
#         _extract_code(text)


# # Define test data for _determine_question_and_answer
# DETERMINE_QUESTION_AND_ANSWER_VALID_DATA = [
#     (
#         "def function(): print('Hello')",
#         "def test(): # TODO: Add the missing line(s) below.",
#         (
#             "def test(): # TODO: Add the missing line(s) below.",
#             "def function(): print('Hello')",
#         ),
#     ),
# ]


# @pytest.mark.parametrize(
#     "block_1, block_2, expected", DETERMINE_QUESTION_AND_ANSWER_VALID_DATA
# )
# def test_valid_determine_question_and_answer(block_1, block_2, expected):
#     question, answer = _determine_question_and_answer(block_1, block_2)
#     assert (question, answer) == expected


# DETERMINE_QUESTION_AND_ANSWER_INVALID_DATA = [
#     ("def function(): print('Hello')", "def test(): print('World')"),
#     ("print('Hello') # TODO: Add the missing line", "print('World')"),
# ]


# @pytest.mark.parametrize("block_1, block_2", DETERMINE_QUESTION_AND_ANSWER_INVALID_DATA)
# def test_invalid_determine_question_and_answer(block_1, block_2):
#     with pytest.raises(ValueError):
#         _determine_question_and_answer(block_1, block_2)


# POST_PROCESS_VALID_DATA = [
#     (
#         "python",
#         "Print hello",
#         "def test():\nprint('Hello')```\n```python\ndef test():\n# TODO: Add the missing line(s) below.",
#         "def test():\nprint('Hello')```\n```python\ndef test():\nprint('Hello')",
#         (
#             "python",
#             "Print hello",
#             "def test():\nprint('Hello')```\n```python\ndef test():\n# TODO: Add the missing line(s) below.",
#             "def test():\nprint('Hello')```\n```python\ndef test():\nprint('Hello')"
#         )
#     ),
#     (
#         "javascript",
#         "Print hello",
#         "function test():\nprint('Hello')```\n```python\ndef test():\n// TODO: Add the missing line(s) below.",
#         "function test():\nprint('Hello')```\n```python\ndef test():\nprint('Hello')",
#         (
#             "javascript",
#             "Print hello",
#             "function test():\nprint('Hello')```\n```python\ndef test():\n// TODO: Add the missing line(s) below.",
#             "function test():\nprint('Hello')```\n```python\ndef test():\nprint('Hello')"
#         )
#     )
# ]


# @pytest.mark.parametrize("language, question, half_completed_code, fully_completed_code, expected", POST_PROCESS_VALID_DATA)
# def test_valid_post_process(language, question, half_completed_code, fully_completed_code, expected):
#     language, question, half_completed_code, fully_completed_code = post_process(language=language, question=question, half_completed_code=half_completed_code, fully_completed_code=fully_completed_code)
#     assert (language, question, half_completed_code, fully_completed_code) == expected


# POST_PROCESS_INVALID_DATA = [
#     (
#         True,
#         "Print hello",
#         "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\n# TODO: Add the missing line(s) below.```",
#         "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\nprint('Hello')```",
#     ),
#     (
#         "python",
#         123,
#         "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\n# TODO: Add the missing line(s) below.```",
#         "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\nprint('Hello')```",
#     ),
#     (
#         "python",
#         123,
#         "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\n```",
#         "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\nprint('Hello')```",
#     ),
#     (
#         "python",
#         "Print hello",
#         "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\n# TODO: Add the missing line(s) below.```",
#         "```python\ndef test():\nprint('Hello')```\n```python\ndef testing():\nprint('Hello')```",
#     )
# ]


# @pytest.mark.parametrize("language, question, half_completed_code, fully_completed_code", POST_PROCESS_INVALID_DATA)
# def test_invalid_post_process(language, question, half_completed_code, fully_completed_code):
#     with pytest.raises(LogicError):
#         post_process(language=language, question=question, half_completed_code=half_completed_code, fully_completed_code=fully_completed_code)