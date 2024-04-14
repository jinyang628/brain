import json
import logging
from typing import Any

from transformers import AutoTokenizer

from app.models.conversation import Conversation

logging.basicConfig(level=logging.DEBUG, format="%(filename)s:%(lineno)d - %(message)s")

log = logging.getLogger(__name__)


def pre_process(
    conversation_dict: dict[str, Any], max_input_tokens: int
) -> tuple[list[Conversation], int]:
    """Pre-processes the conversation and returns the list of splitted conversations and the total token sum of the conversation for usage tracking in stomach."""
    try:
        conversation_lst, token_sum = _split_by_token_length(
            conversation_dict=conversation_dict, max_input_tokens=max_input_tokens
        )
        return conversation_lst, token_sum
    except TypeError as e:
        log.error(
            f"Type of conversation_dict is wrong when pre-processing user input: {e}"
        )
        raise e
    except Exception as e:
        log.error(f"Error pre-processing user chatlog input: {e}")
        raise e


def _split_by_token_length(
    conversation_dict: dict[str, Any], max_input_tokens: int
) -> tuple[list[Conversation], int]:
    """Returns the splitted conversation in the form of a list (if the original conversation is too long) and the total token sum of the conversation for usage tracking in stomach. If the conversation doesn't require splitting, the list will contain only one conversation (the original conversation"""

    tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-Instruct-hf")
    title: str = ""
    token_dict: dict[dict[str, Any], int] = {}

    try:
        for key, value in conversation_dict.items():
            if not isinstance(value, str):
                raise TypeError(f"Value for key {key} is not a string.")
            if key == "title":
                title = value
                continue
            token_length: int = len(
                tokenizer(json.dumps(value), add_special_tokens=False)["input_ids"]
            )
            token_dict[key] = token_length
    except TypeError as e:
        log.error(
            f"Type of conversation_dict is wrong when calculating token length: {e}"
        )
        raise e
    except Exception as e:
        log.error(
            f"Error calculating token length for each message in the conversation: {e}"
        )

    total_token_sum: int = 0
    curr_token_sum: int = 0
    conversation_lst: list[Conversation] = []
    splitted_conversation_dict: dict[str, Any] = {"title": title}
    for conversation_dict_key, token_length in token_dict.items():
        total_token_sum += token_length
        curr_token_sum += token_length
        if curr_token_sum > max_input_tokens:
            log.info(
                f"Token length of {curr_token_sum} exceeds the maximum input token length of {max_input_tokens}. Splitting conversation..."
            )
            conversation_lst.append(Conversation(**splitted_conversation_dict))
            curr_token_sum = 0
            splitted_conversation_dict: dict[str, Any] = {"title": title}
        splitted_conversation_dict[conversation_dict_key] = conversation_dict[
            conversation_dict_key
        ]
    conversation_lst.append(Conversation(**splitted_conversation_dict))
    return (conversation_lst, total_token_sum)
