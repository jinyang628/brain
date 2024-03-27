import logging

from app.config import InferenceConfig
from app.control.summariser import post_process
from app.models.conversation import Conversation
from app.process.summariser import Summariser
import asyncio

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


async def generate_summary(
    conversation: Conversation,
    attempt=1,
    max_attempts=9
) -> dict[str, str]:
    config = InferenceConfig()
    summariser = Summariser(config=config)
    try:
        summary: str = await summariser.summarise(conversation=conversation)
        try:
            processed_summary: dict[str, str] = post_process(summary=summary)
            log.info(f"Processed Summary: {processed_summary}")
            return processed_summary
        except ValueError as e:
            log.error(f"Error post-processing summary (attempt {attempt}/{max_attempts}): {e}")
            if attempt < max_attempts:
                log.info("Retrying summary generation...")
                return await generate_summary(conversation, attempt + 1, max_attempts)
            else:
                raise ValueError(f"Failed to post-process summary after {max_attempts} attempts.")
    except Exception as e:
        log.error(f"Error generating summary: {e}")
        raise e
