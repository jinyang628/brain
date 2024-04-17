import logging
import re

from app.llm.model import LLMType
from app.process.types import TODO_MARKER

log = logging.getLogger(__name__)


def post_process(practice: str, llm_type: LLMType) -> tuple[str, str]:
    """Main post-processing function for the examiner task. Extracts the language, question, and answer from the LLM response."""
    try:
        if not isinstance(practice, str):
            raise TypeError(f"Input is not a string: {practice}")
        if llm_type == LLMType.CLAUDE_INSTANT_1 or llm_type == LLMType.CLAUDE_3_SONNET:
            practice = _remove_output_wrapper(text=practice)
        language, block_1, block_2 = _extract_code(text=practice)
        question, answer = _determine_question_and_answer(block_1=block_1, block_2=block_2)
        question, answer = _verify_expected_similarity_and_difference(question=question, answer=answer)
        return (language, question, answer)
    except ValueError as e:
        log.error(f"Error post-processing practice: {e}")
        raise ValueError(f"Failed to post-process practice: {e}")

def _verify_expected_similarity_and_difference(question: str, answer: str):
    question_lines = question.strip().split("\n")
    answer_lines = answer.strip().split("\n")
    todo_marker_found = False

    q_index = 0
    a_index = 0

    # Loop through each line until we run out of lines in question
    while q_index < len(question_lines):
        if "TODO" in question_lines[q_index]:
            todo_marker_found = True
            q_index += 1
            continue  # Skip TODO marker line and proceed to enforce matching on subsequent lines

        if todo_marker_found:
            # Ensure there are enough lines left in the answer to match the remaining question lines
            if a_index >= len(answer_lines):
                raise ValueError("The answer does not cover all lines in the question after the TODO marker.")

            # Check for matching lines strictly after TODO
            while a_index < len(answer_lines) and question_lines[q_index] != answer_lines[a_index]:
                a_index += 1  # Skip non-matching lines in the answer until a match is found

            if a_index < len(answer_lines) and question_lines[q_index] == answer_lines[a_index]:
                q_index += 1
                a_index += 1  # Increment both to continue matching
            else:
                raise ValueError("The question and answer blocks differ after the TODO marker.")
        else:
            # Match lines one-to-one before the TODO marker
            if question_lines[q_index] != answer_lines[a_index]:
                raise ValueError("The question and answer blocks differ before the TODO marker.")
            q_index += 1
            a_index += 1

    return question, answer


def _remove_output_wrapper(text: str) -> str:
    """Removes the output wrapper from the text and returns the remaining text."""
    index = text.find("</output>")
    if index == -1:
        raise ValueError(
            f"The text does not contain the expected index '<output>': {text}"
        )
    return text[:index].strip()


def _determine_question_and_answer(block_1: str, block_2: str) -> tuple[str, str]:
    """Determines which is the question and answer block by checking which block contains the {TODO_MARKER}. Returns the question and answer in order.

    Raises:
        ValueError: if neither block contains the {TODO_MARKER}, indicating that the LLM response is of invalid shape

    Returns:
        tuple[str, str]: the question and answer strings respectively.
    """
    if TODO_MARKER not in block_1:
        if TODO_MARKER not in block_2:
            log.error("Neither block contains the placeholder for missing code.")
            raise ValueError(
                f"The placeholder {TODO_MARKER} for missing code is absent."
            )
        # question is block_2, answer is block_1
        return block_2, block_1
    elif TODO_MARKER not in block_2:
        # question is block_1, answer is block_2
        return block_1, block_2
    else:
        log.error("Both blocks contain the placeholder for missing code.")
        raise ValueError(f"Both blocks contain the placeholder {TODO_MARKER}.")


def _extract_code(text: str) -> tuple[str, str, str]:
    """Extracts code enclosed in triple backticks and checks language consistency."""
    pattern = r"```(\w+)\s+(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)

    if len(matches) != 2:
        raise ValueError("The text should contain exactly two code blocks.")

    language_1, block_1 = matches[0]
    language_2, block_2 = matches[1]

    if language_1 != language_2:
        raise ValueError(
            f"Language mismatch: first block is {language_1}, second block is {language_2}"
        )

    return language_1, block_1, block_2
