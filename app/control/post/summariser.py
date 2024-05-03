import logging
import re

from app.exceptions.exception import LogicError
from app.llm.model import LLMType

log = logging.getLogger(__name__)


def post_process(topic: str, content: str, llm_type: LLMType) -> dict[str, str]:
    """Processes the output of the summariser and returns a dictionary containing the topic-summary pairs.
    
    Args:
        topic (str): The topic of the summary.
        content (str): The content of the summary.
        llm_type (LLMType): The type of LLM model used to generate the summary. This is important as certain tokens are added to the output by specific LLM models and need to be removed.
    """
    try:
        if not isinstance(topic, str):
            raise TypeError(f"Topic is not a string: {topic}")
        if not isinstance(content, str):
            raise TypeError(f"Content is not a string: {content}")
        # if llm_type == LLMType.CLAUDE_INSTANT_1 or llm_type == LLMType.CLAUDE_3_SONNET:
        #     summary = _remove_output_wrapper(text=summary)
        # removed_header: str = _remove_header(text=summary)
        # topic_content_dict: dict[str, str] = _extract_info(text=removed_header)
        _reject_unlikely_topics(topic=topic)
        return {topic: content}
    except (TypeError, ValueError) as e:
        log.error(f"Logic error while post-processing summary: {e}")
        raise LogicError(message=str(e))
    except Exception as e:
        log.error(f"Unexpected error while post-processing summary: {e}")
        raise e


def _remove_output_wrapper(text: str) -> str:
    """Removes the output wrapper from the text and returns the remaining text.
    
    Args:
        text (str): The text to be processed.
    """
    index = text.find("</output>")
    if index == -1:
        raise ValueError(
            f"The text does not contain the expected index '<output>': {text}"
        )
    return text[:index].strip()


def _reject_unlikely_topics(topic: str):
    """Throws an error if the topic is unlikely to be valid/of good quality.

    The observation is that most valid topics have more than one word. One-word topics generated by LLM tend to be things like "Issue", "Problem", "Solution", etc. that are not what we want.
    
    Args:
        topic (str): the topic-content dictionary to be checked.
    """
    
    if len(topic.split(" ")) <= 1:
        raise ValueError(f"Topic '{topic}' is unlikely to be a valid topic.")


def _remove_header(text: str) -> str:
    """Removes the header from the text and returns the remaining text.
    
    Args:
        text (str): The text to be processed.
    
    Returns:
        str: The text without the header.
    """
    index = text.find("1.")
    if index == -1:
        raise ValueError(f"The text does not contain the expected index '1.': {text}")
    return text[index:].strip()


def _extract_info(text: str) -> dict[str, str]:
    """Extracts the text into topic-summary pairs. Returns a dict containing these pairs.

    Example input:
    1. **Time Complexity of Insertion**: Inserting an element at the beginning of a Python list is a linear-time operation (O(n)), while appending at the end is constant-time (O(1)).

    2. **Prepending Using `insert`**: The `list.insert(0, item)` method can be used to prepend an element, but it's less efficient for large lists.

    Example output:
    {
        'Time Complexity of Insertion': 'Inserting an element at the beginning of a Python list is a linear-time operation (O(n)), while appending at the end is constant-time (O(1)).',
        'Prepending Using `insert`': "The `list.insert(0, item)` method can be used to prepend an element, but it's less efficient for large lists."
    }
    """
    # Regular expression to match **key** and the associated text
    pattern = r"\*\*(.+?)\*\*:\s*(.+?)(?=\n\d\.|\Z)"

    # Find all matches and build the dictionary
    output: dict[str, str] = {
        match.group(1): match.group(2).strip()
        for match in re.finditer(pattern, text, re.DOTALL)
    }

    if len(output) == 0:
        raise ValueError(f"No matches found in the text: {text}")

    return output
