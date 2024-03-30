import logging
from typing import Any, Union

from app.config import InferenceConfig
from app.models.conversation import Conversation
from app.process.summariser import Summariser

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


async def generate_summary(
    conversations: Union[dict[str, Any] | list[Conversation]],
    attempt=1,
    max_attempts=9
) -> dict[str, str]:
    config = InferenceConfig()
    summariser = Summariser(config=config)
    
    conversation_lst: list[Conversation] = None
    if attempt == 1:
        conversation_lst = summariser.pre_process(
            conversation_dict=conversations
        ) 
    else:
        conversation_lst = conversations
        
    merged_summary: dict[str, str] = {}
    remaining_conversations: list[Conversation] = conversation_lst.copy()

    for conversation in conversation_lst:
        try:
            summary: dict[str, str] = await summariser.summarise(conversation=conversation)
            merged_summary.update(summary)
            remaining_conversations.remove(conversation)
        except ValueError as e:
            log.error(f"Error post-processing summary (attempt {attempt}/{max_attempts}): {e}")
            
    if remaining_conversations and attempt < max_attempts:
        log.info(f"Retrying summary generation for remaining {len(remaining_conversations)} conversations...")
        return await generate_summary(
            conversations=remaining_conversations, 
            attempt=attempt + 1, 
            max_attempts=max_attempts
        )
    elif remaining_conversations:
        raise ValueError(f"Failed to post-process remaining {len(remaining_conversations)} conversations after {max_attempts} attempts.")

    return merged_summary
        