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
    KEY_CONCEPT_HEADER = "key_concept_header"
    KEY_CONCEPT_CONTENT = "key_concept_content"
    KEY_CONCEPT_CODE_EXAMPLE = "key_concept_code_example"
    KEY_CONCEPT_CODE_LANGUAGE = "key_concept_code_language"

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
                                SummaryFunctions.KEY_CONCEPT_HEADER: {
                                    "type": "string",
                                    "description": "The title of the key concept."
                                },
                                SummaryFunctions.KEY_CONCEPT_CONTENT: {
                                    "type": "string",
                                    "description": "State the key concept in one or two sentences."
                                },
                                SummaryFunctions.KEY_CONCEPT_CODE_EXAMPLE: {
                                    "type": "string",
                                    "description": "A short code example illustrating the key concept if necessary."
                                },
                                SummaryFunctions.KEY_CONCEPT_CODE_LANGUAGE: {
                                    "type": "string",
                                    "description": "The programming language of the code example."
                                }
                            },
                            "required": [SummaryFunctions.KEY_CONCEPT_HEADER, SummaryFunctions.KEY_CONCEPT_CONTENT],
                            "allOf": [
                                {
                                    "if": {
                                        "properties": {
                                            SummaryFunctions.KEY_CONCEPT_CODE_EXAMPLE: {
                                                "type": "string"
                                            }
                                        },
                                        "required": [SummaryFunctions.KEY_CONCEPT_CODE_EXAMPLE]
                                    },
                                    "then": {
                                        "required": [SummaryFunctions.KEY_CONCEPT_CODE_LANGUAGE]
                                    },
                                    "else": {
                                        "not": {
                                            "required": [SummaryFunctions.KEY_CONCEPT_CODE_LANGUAGE]
                                        }
                                    }
                                }
                            ]
                        }
                    }
                },
                "required": [SummaryFunctions.TOPIC, SummaryFunctions.GOAL, SummaryFunctions.OVERVIEW, SummaryFunctions.KEY_CONCEPTS]
            }
        }
    ]
    return summary_functions
