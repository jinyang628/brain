import logging
import re

log = logging.getLogger(__name__)

def post_process(practice: str) -> tuple[str, str]:
    try:
        _check_to_do_placeholder(text=practice)
        language, code = _extract_code(text=practice)
        return (language, code)
    except ValueError as e:
        log.error(f"Error post-processing practice: {e}")
        raise ValueError(f"Failed to post-process practice: {e}")

def _check_to_do_placeholder(text: str):
    if "# TODO: Add the missing code below." not in text:
        raise ValueError("The placeholder # TODO: for missing code is absent.")
    
def _extract_code(text: str) -> tuple[str, str]:
    """Extract sthe code enclosed in triple backticks from auxiliary text."""
    # Regular expression to match the pattern
    pattern = r"```(\w+)\s+(.*?)```"

    # Search using the regular expression
    match = re.search(pattern, text, re.DOTALL)
    if match:
        # Extract language and code
        language = match.group(1)
        code = match.group(2)
        return language, code
    else:
        raise ValueError(f"The text does not contain the expected code block and language indicator: {text}")
