from enum import StrEnum
from typing import Any

class SummaryFunctions(StrEnum):
    GET_SUMMARY = "get_summary"
    
    # Unique element to output 
    TOPIC = "topic"
    GOAL = "goal"
    OVERVIEW = "overview"

    KEY_CONCEPTS = "key_concepts"
    # List of tuples containing these 3 elements
    TITLE = "title" # Compulsory
    EXPLANATION = "explanation" # Compulsory
    CODE_EXAMPLE = "code_example" # Optional
    # CODE_EXAMPLE contains these 2 compulsory elements
    CODE = "code"
    LANGUAGE = "language"

def get_summary_functions() -> list[dict[str, Any]]:
    summary_functions: list[dict[str, Any]] = [
        {
            "name": SummaryFunctions.GET_SUMMARY,
            "description": "Generate revision notes based on the key ideas present in the model's response.",
            "parameters": {
                "type": "object",
                "properties": {
                    SummaryFunctions.TOPIC: {
                        "type": "string",
                        "description": "The topic which the revision notes cover in fewer than 7 words."
                    },
                    SummaryFunctions.GOAL: {
                        "type": "string",
                        "description": "The goal of the revision notes in one sentence. Students should achieve this goal after reading the notes."
                    },
                    SummaryFunctions.OVERVIEW: {
                        "type": "string",
                        "description": "A high-level summary of the key ideas present in the revision notes in one sentence."
                    },
                    SummaryFunctions.KEY_CONCEPTS: {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                SummaryFunctions.TITLE: {
                                    "type": "string",
                                    "description": "The title of the key concept."
                                },
                                SummaryFunctions.EXPLANATION: {
                                    "type": "string",
                                    "description": "State the key concept in one or two sentences."
                                },
                                SummaryFunctions.CODE_EXAMPLE: {
                                    "type": "object",
                                    "properties": {
                                        SummaryFunctions.CODE: {
                                            "type": "string",
                                            "description": "The code example illustrating the key concept."
                                        },
                                        SummaryFunctions.LANGUAGE: {
                                            "type": "string",
                                            "description": "The programming language of the code example."
                                        }
                                    },
                                    "required": [SummaryFunctions.CODE, SummaryFunctions.LANGUAGE],
                                }
                            },
                            "required": [SummaryFunctions.TITLE, SummaryFunctions.EXPLANATION]
                        }
                    }
                },
                "required": [SummaryFunctions.TOPIC, SummaryFunctions.GOAL, SummaryFunctions.OVERVIEW, SummaryFunctions.KEY_CONCEPTS]
            }
        }
    ]
    return summary_functions
