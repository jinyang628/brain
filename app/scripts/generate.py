import logging
from typing import Any, Union
import asyncio 

from app.config import InferenceConfig
from app.exceptions.exception import InferenceFailure, LogicError
from app.models.conversation import Conversation
from app.models.content import Content
from app.process.generator import Generator

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

async def generate(
    conversation: Union[dict[str, Any] | list[Conversation]],
    content_lst: list[Content],
    attempt: int = 1,
    max_attempts: int = 5,
    token_sum: int = 0,
) -> tuple[list[dict[str, Any]], int]:
    """Returns the gemerated notes and the total token sum of the conversation for usage tracking in stomach.

    Args:
        conversations (Union[dict[str, Any]  |  list[Conversation]]): The conversation to be summarised. There are two possible types depending on whether it is the first attempt or not.
        content_lst (list[Content]): The content types that the user wants to generate notes for.
        attempt (int, optional): The current attempt number which will be incremented with every retry. Defaults to 1.
        max_attempts (int, optional): The attempt number which will cause the inference pipeline to stop when reached. Defaults to 9.
        token_sum (int, optional): The total token sum that is used by the user to generate the notes. Defaults to 0.

    Returns:
        tuple[dict[str, str], int]: The summary in topic-content key-value pairs and the total token sum of the conversation
    """

    config = InferenceConfig()
    generator = Generator(config=config)

    conversation_lst: list[Conversation] = None
    if attempt == 1:
        try:
            conversation_lst, token_sum = generator.pre_process(
                conversation=conversation
            )
        except LogicError as e:
            log.error(f"Logic error while trying to pre-process conversation: {str(e)}")
            raise e
    else:
        conversation_lst = conversation 

    notes: list[dict[str, Any]] = []
    remaining_conversations: list[Conversation] = []
    generate_tasks = [
        generator.generate(conversation=conversation, content_lst=content_lst) for conversation in conversation_lst
    ]
    results = await asyncio.gather(*generate_tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            # TODO: Handle exceptions individually
            log.error(
                f"Error processing conversation {i+1} (attempt {attempt}/{max_attempts}): {result}"
            )
            remaining_conversations.append(conversation_lst[i])
        else:
            notes.append(result)

    if remaining_conversations and attempt < max_attempts:
        log.info(
            f"Retrying summary generation for remaining {len(remaining_conversations)} conversations..."
        )
        return await generate(
            conversation=remaining_conversations,
            content_lst=content_lst,
            attempt=attempt + 1,
            max_attempts=max_attempts,
            token_sum=token_sum,
        )
    elif remaining_conversations:
        raise InferenceFailure(
            f"Failed to post-process remaining {len(remaining_conversations)} conversations after {max_attempts} attempts."
        )

    return notes, token_sum
