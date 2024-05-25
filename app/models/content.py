import logging
from enum import StrEnum

from app.exceptions.exception import LogicError

log = logging.getLogger(__name__)

# This class must match Content Enum from fingers and stomach repo
class Content(StrEnum):
    MCQ = "mcq"
    CODE = "code"

    def validate(content_str_lst: list[str]) -> list["Content"]:
        """Validates the content strings and transforms them into Content objects.
        
        Returns:
            list[Content]: The validated content.
        """
        validated_content: list[Content] = []
        for content_str in content_str_lst:
            try:
                validated_content.append(Content(content_str))
            except KeyError as e:
                log.error(f"Error validating content because enum string is wrong: {e}")
                raise LogicError(f"Invalid content string: {content_str}") from e
            except Exception as e:
                log.error(f"Unexpected error while validating content: {e}")
                raise e
        return validated_content

