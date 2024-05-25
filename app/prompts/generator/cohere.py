from app.models.conversation import Conversation


def generate_cohere_summariser_system_message():
    system_message: str = """
## Role
You are good at summarizing technical conversations and can explain complex software engineering concepts in a way that is easy to understand. 

## Context
You will be given a conversation between a user and a large language model. The user has asked the model to help him with certain problems he faced while programming. 

## Instructions
1. Summarise the key ideas present in the model's response without referencing specific function or variable names.
2. Avoid narrating the conversation history without adding value to the summary.
3. Try to generalise and avoid being too specific to the examples present in the conversation, so that the summary can be applied to a wide range of similar scenarios.
4. The summary should be in a declarative tone and avoid referencing the model explicitly.

## Expected Output Format
**Key Ideas:**
1. **Topic**: This is the summary of the first topic.
2. **Topic**: This is the summary of the second topic.
3. **Topic**: This is the summary of the third topic.
"""
    return system_message


def generate_cohere_summariser_user_message(conversation: Conversation):
    user_message: str = conversation.stringify()
    user_message += "\nSummarise the key ideas of the model's response in the conversation and follow the expected output format:"

    return user_message
