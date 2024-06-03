from enum import StrEnum
from typing import Any

class NotesFunctions(StrEnum):
    GET_NOTES = "get_notes"
    
    # Unique element to output 
    TOPIC = "topic" # Compulsory
    GOAL = "goal" # Compulsory
    CONTEXT = "context" # Compulsory
    OVERVIEW = "overview" # Compulsory

    # List element to output
    KEY_CONCEPTS = "key_concepts" # Compulsory
    # List of tuples containing these 3 elements
    KEY_CONCEPT_TITLE = "key_concept_title" # Compulsory
    KEY_CONCEPT_EXPLANATION = "key_concept_explanation" # Compulsory
    KEY_CONCEPT_CODE_EXAMPLE = "key_concept_code_example" # Optional
    # KEY_CONCEPT_CODE_EXAMPLE contains these 2 elements
    KEY_CONCEPT_CODE = "key_concept_code" # Compulsory
    KEY_CONCEPT_LANGUAGE = "key_concept_language" # Compulsory
    
    # List element to output
    TIPS = "tips" # Optional
    # List of tuples containing these 2 elements
    TIP_TITLE = "tip_title" # Compulsory
    TIP_EXPLANATION = "tip_explanation" # Compulsory
    
    # Unique element to output
    MCQ_PRACTICE = "mcq_practice" # Optional
    # MCQ_PRACTICE contains these 4 elements
    MCQ_PRACTICE_TITLE = "mcq_practice_title" # Compulsory
    MCQ_PRACTICE_QUESTION = "mcq_practice_question" # Compulsory
    MCQ_PRACTICE_WRONG_OPTIONS = "mcq_practice_wrong_options" # Compulsory
    MCQ_PRACTICE_CORRECT_OPTION = "mcq_practice_correct_option" # Compulsory
    
    # Unique element to output
    CODE_PRACTICE = "code_practice" # Optional
    # CODE_PRACTICE contains these 3 elements
    CODE_PRACTICE_TITLE = "code_practice_title" # Compulsory
    CODE_PRACTICE_QUESTION = "code_practice_question" # Compulsory
    CODE_PRACTICE_HALF_COMPLETED_CODE = "code_practice_half_completed_code" # Compulsory
    CODE_PRACTICE_FULLY_COMPLETED_CODE = "code_practice_fully_completed_code" # Compulsory
    CODE_PRACTICE_LANGUAGE = "code_practice_language" # Compulsory

def get_notes_functions(
    contains_mcq_practice: bool, 
    contains_code_practice: bool
) -> list[dict[str, Any]]:
    """Returns the function-calling function that will be passed into the LLM

    Args:
        contains_mcq_practice (bool): True if the users want to include multiple-choice questions in the notes.
        contains_code_practice (bool): True if the users want to include coding questions in the notes.

    Returns:
        list[dict[str, Any]]: The function-calling function that will be passed into the LLM
    """
    properties = {
        NotesFunctions.TOPIC: {
            "type": "string",
            "description": "The topic which the revision notes cover in fewer than 7 words."
        },
        NotesFunctions.GOAL: {
            "type": "string",
            "description": "The goal of the revision notes in one sentence. Students should achieve this goal after reading the notes."
        },
        NotesFunctions.CONTEXT: {
            "type": "string",
            "description": "A summary of the questions which the user asked in fewer than 2 sentences. These questions serve as the context behind the revision notes."
        },
        NotesFunctions.OVERVIEW: {
            "type": "string",
            "description": "A high-level summary of the key ideas present in the revision notes in one sentence."
        },
        NotesFunctions.KEY_CONCEPTS: {
            "type": "array",
            "description": "A list of key concepts that students should learn.",
            "items": {
                "type": "object",
                "properties": {
                    NotesFunctions.KEY_CONCEPT_TITLE: {
                        "type": "string",
                        "description": "The title of the key concept."
                    },
                    NotesFunctions.KEY_CONCEPT_EXPLANATION: {
                        "type": "string",
                        "description": "State the key concept in one or two sentences. Bold important terms."
                    },
                    NotesFunctions.KEY_CONCEPT_CODE_EXAMPLE: {
                        "type": "object",
                        "properties": {
                            NotesFunctions.KEY_CONCEPT_CODE: {
                                "type": "string",
                                "description": "The code example illustrating the key concept."
                            },
                            NotesFunctions.KEY_CONCEPT_LANGUAGE: {
                                "type": "string",
                                "description": "The programming language of the code example."
                            }
                        },
                        "required": [NotesFunctions.KEY_CONCEPT_CODE, NotesFunctions.KEY_CONCEPT_LANGUAGE],
                    }
                },
                "required": [NotesFunctions.KEY_CONCEPT_TITLE, NotesFunctions.KEY_CONCEPT_EXPLANATION]
            }
        },
        NotesFunctions.TIPS: {
            "type": "array",
            "description": "A list of tips that will help students to apply the key concepts better in the future. Return None if there are no good tips.",
            "items": {
                "type": "object",
                "properties": {
                    NotesFunctions.TIP_TITLE: {
                        "type": "string",
                        "description": "The title of the tip."
                    },
                    NotesFunctions.TIP_EXPLANATION: {
                        "type": "string",
                        "description": "State the tip in one or two sentences."
                    }
                },
                "required": [NotesFunctions.TIP_TITLE, NotesFunctions.TIP_EXPLANATION]
            }
        }
    }

    if contains_mcq_practice:
        properties[NotesFunctions.MCQ_PRACTICE] = {
            "type": "object",
            "description": "A multiple-choice question to test students' understanding of the key concepts. Return None if there are no suitable multiple-choice questions.",
            "properties": {
                NotesFunctions.MCQ_PRACTICE_TITLE: {
                    "type": "string",
                    "description": "A short descriptive title for the multiple-choice question."
                },
                NotesFunctions.MCQ_PRACTICE_QUESTION: {
                    "type": "string",
                    "description": "The multiple-choice question that students have to answer."
                },
                NotesFunctions.MCQ_PRACTICE_WRONG_OPTIONS: {
                    "type": "array",
                    "description": "A list of wrong options for the multiple-choice question.",
                    "items": {
                        "type": "string"
                    }
                },
                NotesFunctions.MCQ_PRACTICE_CORRECT_OPTION: {
                    "type": "string",
                    "description": "The correct option for the multiple-choice question.",
                },
            },
            "required": [NotesFunctions.MCQ_PRACTICE_TITLE, NotesFunctions.MCQ_PRACTICE_QUESTION, NotesFunctions.MCQ_PRACTICE_WRONG_OPTIONS, NotesFunctions.MCQ_PRACTICE_CORRECT_OPTION]
        }

    if contains_code_practice:
        properties[NotesFunctions.CODE_PRACTICE] = {
            "type": "object",
            "description": "A coding question to test students' understanding of the key concepts. Return None if there are no suitable coding questions.",
            "properties": {
                NotesFunctions.CODE_PRACTICE_TITLE: {
                    "type": "string",
                    "description": "A short descriptive title for the coding question."
                },
                NotesFunctions.CODE_PRACTICE_QUESTION: {
                    "type": "string",
                    "description": "The coding question that is formulated based on the key concepts, with enough context and hints for the student to complete the code without ambiguity."
                },
                NotesFunctions.CODE_PRACTICE_HALF_COMPLETED_CODE: {
                    "type": "string",
                    "description": "The half-completed code with the TODO marker in place of the missing code."
                },
                NotesFunctions.CODE_PRACTICE_FULLY_COMPLETED_CODE: {
                    "type": "string",
                    "description": "The fully-completed code, with the missing parts annotated by the TODO marker filled."
                },
                NotesFunctions.CODE_PRACTICE_LANGUAGE: {
                    "type": "string",
                    "description": "The programming language used in the practice question."
                }
            },
            "required": [NotesFunctions.CODE_PRACTICE_TITLE, NotesFunctions.CODE_PRACTICE_QUESTION, NotesFunctions.CODE_PRACTICE_HALF_COMPLETED_CODE, NotesFunctions.CODE_PRACTICE_FULLY_COMPLETED_CODE, NotesFunctions.CODE_PRACTICE_LANGUAGE]
        }

    notes_functions: list[dict[str, Any]] = [
        {
            "name": NotesFunctions.GET_NOTES,
            "description": "Generate revision notes based on the key ideas present in the model's response.",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": [
                    NotesFunctions.TOPIC, 
                    NotesFunctions.GOAL, 
                    NotesFunctions.CONTEXT,
                    NotesFunctions.OVERVIEW, 
                    NotesFunctions.KEY_CONCEPTS,
                    NotesFunctions.TIPS,
                    NotesFunctions.MCQ_PRACTICE,
                    NotesFunctions.CODE_PRACTICE
                ]
            }
        }
    ]

    return notes_functions