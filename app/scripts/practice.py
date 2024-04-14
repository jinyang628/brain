import logging

from app.config import InferenceConfig
from app.process.examiner import Examiner

log = logging.getLogger(__name__)


async def generate_practice(
    topic: str, summary_chunk: str, attempt=1, max_attempts=9
) -> tuple[str, str, str]:
    config = InferenceConfig()
    examiner = Examiner(config=config)
    try:
        language, question, answer = await examiner.examine(
            topic=topic, summary_chunk=summary_chunk
        )
        log.info(f"Language: {language}")
        log.info(f"Question: {question}")
        log.info(f"Answer: {answer}")
        return language, question, answer
    except ValueError as e:
        log.error(
            f"Error post-processing practice (attempt {attempt}/{max_attempts}): {e}"
        )

    if attempt < max_attempts:
        log.info(f"Retrying practice generation for topic: {topic}...")
        return await generate_practice(
            topic=topic,
            summary_chunk=summary_chunk,
            attempt=attempt + 1,
            max_attempts=max_attempts,
        )
    else:
        raise ValueError(
            f"Failed to post-process practice for topic: {topic} after {max_attempts} attempts."
        )
