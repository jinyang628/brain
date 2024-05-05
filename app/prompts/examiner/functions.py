from enum import StrEnum
from typing import Any

class PracticeFunctions(StrEnum):
    GET_PRACTICE = "get_practice"
    LANGUAGE = "language"
    QUESTION = "question"
    HALF_COMPLETED_CODE = "half_completed_code"
    FULLY_COMPLETED_CODE = "fully_completed_code"
    
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
                        "description": "The coding question that is formulated based on the summary."
                    },
                    PracticeFunctions.HALF_COMPLETED_CODE: {
                        "type": "string",
                        "description": "The half-completed code with the TODO marker in place of the missing code."
                    },
                    PracticeFunctions.FULLY_COMPLETED_CODE: {
                        "type": "string",
                        "description": "The fully-completed code, with the missing parts annotated by the TODO marker filled."
                    },
                    PracticeFunctions.LANGUAGE: {
                        "type": "string",
                        "description": "The programming language used in the practice question."
                    }
                },
                "required": [PracticeFunctions.QUESTION, PracticeFunctions.HALF_COMPLETED_CODE, PracticeFunctions.FULLY_COMPLETED_CODE, PracticeFunctions.LANGUAGE]
            }
        }
    ]
    return practice_functions