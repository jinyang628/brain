from app.models.conversation import Conversation


def generate_open_ai_summariser_system_message():
    system_message: str = """
You are good at generalising concepts out of technical conversations and can transforming highly specific conversation into transferable software engineering principles. You will be given a conversation between a user and a large language model. The user has asked the model to help him with certain problems he faced while programming. 

Follow these instructions:
1. Come up with a topic that encapsulates the main learning points in the conversation, and summarise the content that relates to this topic. Do not just narrate the conversation history. 
2. Try to generalise and avoid being too specific to the examples present in the conversation, so that the summary can be applied to a wide range of similar scenarios.
"""
    return system_message


def generate_open_ai_summariser_user_message(conversation: Conversation):
    user_message: str = conversation.stringify()
    user_message += "\nSummarise the key ideas of the model's response but avoid referencing the model or the user in your summary. Describe the content as if it is from a textbook:"

    return user_message
