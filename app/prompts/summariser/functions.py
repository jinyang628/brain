from enum import StrEnum
from typing import Any

class SummaryFunctions(StrEnum):
    GET_SUMMARY = "get_summary"
    TOPIC = "topic"
    CONTENT = "content"

def get_summary_functions() -> list[dict[str, Any]]:
    summary_functions: list[dict[str, Any]] = [
        {
            "name": SummaryFunctions.GET_SUMMARY,
            "description": "Summarise the key ideas present in the model's response.",
            "parameters": {
                "type": "object",
                "properties": {
                    SummaryFunctions.TOPIC: {
                        "type": "string",
                        "description": "The topic of the summary."
                    },
                    SummaryFunctions.CONTENT: {
                        "type": "string",
                        "description": "The content of the summary."
                    }
                },
                "required": [SummaryFunctions.TOPIC, SummaryFunctions.CONTENT], 
            }
        }
    ]
    return summary_functions