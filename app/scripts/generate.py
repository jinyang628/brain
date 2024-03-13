from app.config import InferenceConfig
from app.models.conversation import Conversation
import logging

from app.process.summariser import Summarizer 

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)



async def generate(conversation: Conversation) -> str:
    config = InferenceConfig()
    summarizer = Summarizer(config)
    try:
        summary: str = await summarizer.summarize(conversation)
        return summary
    except Exception as e:
        log.error(f"Error generating summary: {e}")
        raise e