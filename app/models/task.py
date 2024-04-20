import logging
from enum import StrEnum

from app.exceptions.exception import LogicError

log = logging.getLogger(__name__)

# This class must match TaskEnum from fingers and stomach repo
class Task(StrEnum):
    SUMMARISE = "summarise"
    PRACTICE = "practice"

    def validate(task_str_lst: list[str]) -> list["Task"]:
        """Validates whether the task strings and transforms them into Task objects.
        
        Returns:
            list[Task]: The validated tasks.
        """
        validated_tasks: list[Task] = []
        for task_str in task_str_lst:
            try:
                validated_tasks.append(Task(task_str))
            except KeyError as e:
                log.error(f"Error validating task because enum string is wrong: {e}")
                raise LogicError(f"Invalid task string: {task_str}") from e
            except Exception as e:
                log.error(f"Unexpected error while validating tasks: {e}")
                raise e
        return validated_tasks

