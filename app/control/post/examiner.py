import logging
import re

log = logging.getLogger(__name__)


def post_process(practice: str) -> tuple[str, str]:
    try:
        _check_to_do_placeholder(text=practice)
        language, question, answer = _extract_code(text=practice)
        return (language, question, answer)
    except ValueError as e:
        log.error(f"Error post-processing practice: {e}")
        raise ValueError(f"Failed to post-process practice: {e}")


def _check_to_do_placeholder(text: str):
    if "# TODO: Add the missing line below." not in text:
        raise ValueError("The placeholder # TODO: for missing code is absent.")


def _extract_code(text: str) -> tuple[str, str, str]:
    """Extracts code enclosed in triple backticks and checks language consistency."""
    pattern = r"```(\w+)\s+(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)

    if len(matches) != 2:
        raise ValueError("The text should contain exactly two code blocks.")

    language_1, question = matches[0]
    language_2, answer = matches[1]

    if language_1 != language_2:
        raise ValueError(
            f"Language mismatch: first block is {language_1}, second block is {language_2}"
        )

    return language_1, question, answer
