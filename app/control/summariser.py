import re
import logging

log = logging.getLogger(__name__)

def post_process(summary: str) -> dict[str, str]:
    """Processes the output of the summariser and returns a dictionary containing the topic-summary pairs."""
    try:
        removed_header: str = _remove_header(text=summary)
        topic_content_dict: dict[str, str] = _extract_info(text=removed_header)
        return topic_content_dict
    except ValueError as e:
        log.error(f"Error post-processing summary: {e}")
        raise ValueError(f"Error post-processing summary: {e}")

def _remove_header(text: str) -> str:
    """Removes the header from the text and returns the remaining text."""
    index = text.find("1.")
    if index == -1:
        raise ValueError(f"The text does not contain the expected index '1.': {text}")
    # index = text.find("-")
    # if index == -1:
    #     raise ValueError(f"The text does not contain the expected demarker '-': {text}")
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
    pattern = r'\*\*(.+?)\*\*:\s*(.+?)(?=\n\d\.|\Z)'

    # Find all matches and build the dictionary
    output: dict[str, str] = {match.group(1): match.group(2).strip() for match in re.finditer(pattern, text, re.DOTALL)}
    
    if len(output) == 0:
        raise ValueError(f"No matches found in the text: {text}")
    
    return output