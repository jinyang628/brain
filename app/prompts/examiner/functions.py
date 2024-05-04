from enum import StrEnum
from typing import Any

class PracticeFunctions(StrEnum):
    GET_PRACTICE = "get_practice"
    LANGUAGE = "language"
    QUESTION = "question"
    ANSWER = "answer"
    
def get_practice_functions() -> list[dict[str, str]]:
    practice_functions: list[dict[str, Any]]= [
        {
            "name": PracticeFunctions.GET_PRACTICE,
            "description": "Generate practice questions based on the summary.",
            "parameters": {
                "type": "object",
                "properties": {
                    PracticeFunctions.QUESTION: {
                        "type": "string",
                        "description": "The half-completed code block with the TODO marker in place of the missing code."
                    },
                    PracticeFunctions.ANSWER: {
                        "type": "string",
                        "description": "The fully-completed code block with the missing parts in the annotated by the TODO marker filled."
                    },
                    PracticeFunctions.LANGUAGE: {
                        "type": "string",
                        "description": "The language of the practice questions."
                    }
                },
                "required": [PracticeFunctions.QUESTION, PracticeFunctions.ANSWER, PracticeFunctions.LANGUAGE]
            }
        }
    ]
    return practice_functions