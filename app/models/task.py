import logging
from enum import StrEnum

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
        try:
            validated_tasks: list[Task] = []
            for task_str in task_str_lst:
                validated_tasks.append(Task(task_str))
            return validated_tasks
        except Exception as e:
            log.error(f"Error validating task: {e}")
            raise e
