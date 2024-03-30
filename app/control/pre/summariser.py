import json
import logging
from typing import Any
from transformers import AutoTokenizer

from app.models.conversation import Conversation

log = logging.getLogger(__name__)

def pre_process(conversation_dict: dict[str, Any], max_input_tokens: int) -> list[Conversation]:
    try:
        conversation_lst: list[Conversation] = _split_by_token_length(
            conversation_dict=conversation_dict,
            max_input_tokens=max_input_tokens
        )
        return conversation_lst
    except Exception as e:
        log.error(f"Error pre-processing user chatlog input: {e}")
        raise e
    
def _split_by_token_length(conversation_dict: dict[str, Any], max_input_tokens: int) -> list[Conversation]:
    tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-Instruct-hf")
    title: str = ""
    token_dict: dict[dict[str, Any], int] = {}
        
    try: 
        for key, value in conversation_dict.items():
            if key == "title":
                title = value
                continue
            token_length: int = len(tokenizer(json.dumps(value), add_special_tokens=False)["input_ids"])
            token_dict[key] = token_length
    except Exception as e:
        log.error(f"Error calculating token length for each message in the conversation: {e}")
    
    token_sum: int = 0
    conversation_lst: list[Conversation] = []   
    splitted_conversation_dict: dict[str, Any] = {"title": title}
    for conversation_dict_key, token_length in token_dict.items():
        token_sum += token_length
        if token_sum > max_input_tokens:
            log.info(f"Token length of {token_sum} exceeds the maximum input token length of {max_input_tokens}. Splitting conversation...")
            conversation_lst.append(Conversation(**splitted_conversation_dict))
            token_sum = 0
            splitted_conversation_dict: dict[str, Any] = {"title": title}
        splitted_conversation_dict[conversation_dict_key] = conversation_dict[conversation_dict_key]
    conversation_lst.append(Conversation(**splitted_conversation_dict))
    return conversation_lst