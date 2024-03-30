import logging
from typing import Any

from app.config import InferenceConfig
from app.control.post.summariser import post_process
from app.process.summariser import Summariser

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


async def generate_summary(
    conversation_dict: dict[str, Any],
    attempt=1,
    max_attempts=9
) -> dict[str, str]:
    config = InferenceConfig()
    summariser = Summariser(config=config)
    
    try:
        summary: str = await summariser.summarise(conversation_dict=conversation_dict)
        return summary
    except ValueError as e:
        log.error(f"Error post-processing summary (attempt {attempt}/{max_attempts}): {e}")
        if attempt < max_attempts:
            log.info("Retrying summary generation...")
            return await generate_summary(
                conversation_dict=conversation_dict, 
                attempt=attempt + 1, 
                max_attempts=max_attempts
            )
        else:
            raise ValueError(f"Failed to post-process summary after {max_attempts} attempts.")
