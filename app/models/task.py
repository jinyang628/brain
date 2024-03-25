from enum import StrEnum
import logging

log = logging.getLogger(__name__)

# This class must match TaskEnum from fingers and stomach repo 
class Task(StrEnum):
    SUMMARISE = "summarise"
    PRACTICE = "practice"
    
    def validate(task_str_lst: list[str]) -> list["Task"]:
        try:
            validated_tasks: list[Task] = []
            for task_str in task_str_lst:
                validated_tasks.append(Task(task_str))
            return validated_tasks
        except Exception as e:
            log.error(f"Error validating task: {e}")
            raise e