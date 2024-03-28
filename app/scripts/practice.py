from app.config import InferenceConfig
from app.control.examiner import post_process
from app.process.examiner import Examiner
import logging

log = logging.getLogger(__name__) 

async def generate_practice(
    topic: str,
    content: str,
    attempt=1,
    max_attempts=9
) -> tuple[str, str]:
    config = InferenceConfig()
    examiner = Examiner(config=config)
    try:
        practice: str = await examiner.examine(topic=topic, content=content) 
        try:
            language, code = post_process(practice=practice)  
            log.info(f"Language: {language}")
            log.info(f"Code: {code}")
            return (language, code)
        except ValueError as e:
            log.error(f"Error post-processing practice (attempt {attempt}/{max_attempts}): {e}")
            if attempt < max_attempts:
                log.info("Retrying practice generation...")
                return await generate_practice(topic, content, attempt + 1, max_attempts)
            else:
                raise ValueError(f"Failed to post-process practice after {max_attempts} attempts.")
    except Exception as e:
        log.error(f"Error generating practice: {e}")
        raise e