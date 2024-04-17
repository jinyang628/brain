import logging
from typing import Any, Union

from app.config import InferenceConfig
from app.models.conversation import Conversation
from app.process.summariser import Summariser

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


async def generate_summary(
    conversations: Union[dict[str, Any] | list[Conversation]],
    attempt: int = 1,
    max_attempts: int = 9,
    token_sum: int = 0,
) -> tuple[dict[str, str], int]:
    """Returns the summary in topic-content key-value pairs and the total token sum of the conversation for usage tracking in stomach.

    Args:
        conversations (Union[dict[str, Any]  |  list[Conversation]]): The conversation to be summarised. There are two possible types depending on whether it is the first attempt or not.
        attempt (int, optional): The current attempt number which will be incremented with every retry. Defaults to 1.
        max_attempts (int, optional): The attempt number which will cause the inference pipeline to stop when reached. Defaults to 9.
        token_sum (int, optional): The total token sum that is used by the user to generate the notes. Defaults to 0.

    Raises:
        ValueError: _description_

    Returns:
        tuple[dict[str, str], int]: _description_
    """

    config = InferenceConfig()
    summariser = Summariser(config=config)

    conversation_lst: list[Conversation] = None
    if attempt == 1:
        conversation_lst, token_sum = summariser.pre_process(
            conversation_dict=conversations
        )
    else:
        conversation_lst = conversations

    merged_summary: dict[str, str] = {}
    remaining_conversations: list[Conversation] = conversation_lst.copy()

    for conversation in conversation_lst:
        try:
            summary: dict[str, str] = await summariser.summarise(
                conversation=conversation
            )
            merged_summary.update(summary)
            remaining_conversations.remove(conversation)
        except ValueError as e:
            log.error(
                f"Error post-processing summary (attempt {attempt}/{max_attempts}): {e}"
            )

    if remaining_conversations and attempt < max_attempts:
        log.info(
            f"Retrying summary generation for remaining {len(remaining_conversations)} conversations..."
        )
        return await generate_summary(
            conversations=remaining_conversations,
            attempt=attempt + 1,
            max_attempts=max_attempts,
            token_sum=token_sum,
        )
    elif remaining_conversations:
        raise ValueError(
            f"Failed to post-process remaining {len(remaining_conversations)} conversations after {max_attempts} attempts."
        )

    return merged_summary, token_sum
