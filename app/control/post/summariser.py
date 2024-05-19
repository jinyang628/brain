import logging
from typing import Any, Optional

from app.exceptions.exception import LogicError
from app.prompts.summariser.functions import SummaryFunctions

log = logging.getLogger(__name__)


def post_process(
    topic: str, 
    goal: str, 
    overview: str, 
    key_concepts_lst: list[dict[str, str]]
    ) -> dict[str, Any]:
    """_summary_

    Args:
        topic (str): The topic of the summary
        goal (str): The goal of the summary
        overview (str): The overview of the summary
        key_concepts_lst (list[dict[str, str]]): The list of key concepts of the summary

    Returns:
        dict[str, Any]: A dictionary containing the parts of the summary
    """
    try:
        if not isinstance(topic, str):
            raise TypeError(f"Topic is not a string: {topic}")
        if not isinstance(goal, str):
            raise TypeError(f"Goal is not a string: {goal}")
        if not isinstance(overview, str):
            raise TypeError(f"Overview is not a string: {overview}")
        if not isinstance(key_concepts_lst, list):
            raise TypeError(f"Key concepts list is not a list: {key_concepts_lst}")
        
        _reject_unlikely_topics(topic=topic)
        _enforce_code_language_presence(key_concepts_lst=key_concepts_lst)
        
        return {
            SummaryFunctions.TOPIC.value: topic, 
            SummaryFunctions.GOAL.value: goal, 
            SummaryFunctions.OVERVIEW.value: overview, 
            SummaryFunctions.KEY_CONCEPTS.value: key_concepts_lst
        }
    except (TypeError, ValueError) as e:
        log.error(f"Logic error while post-processing summary: {e}")
        raise LogicError(message=str(e))
    except Exception as e:
        log.error(f"Unexpected error while post-processing summary: {e}")
        raise e


def _reject_unlikely_topics(topic: str):
    """Throws an error if the topic is unlikely to be valid/of good quality.

    The observation is that most valid topics have more than one word. One-word topics generated by LLM tend to be things like "Issue", "Problem", "Solution", etc. that are not what we want.
    
    Args:
        topic (str): the topic-content dictionary to be checked.
    """
    
    if len(topic.split(" ")) <= 1:
        raise ValueError(f"Topic '{topic}' is unlikely to be a valid topic.")
    
def _enforce_code_language_presence(key_concepts_lst: list[dict[str, str]]):
    """Enforces that the code language is present if the code example is present.

    Args:
        key_concepts_lst (list[dict[str, str]]): the list of key concepts to be checked.
    """
    for key_concept in key_concepts_lst:
        code_example: Optional[dict[str, str]] = key_concept.get(SummaryFunctions.CODE_EXAMPLE.value)
        if not code_example:
            continue
        if code_example.get(SummaryFunctions.CODE.value) and not code_example.get(SummaryFunctions.LANGUAGE.value):
            raise ValueError(f"Code example present but code language not specified for key concept: {key_concept}")