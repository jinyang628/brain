from app.models.conversation import Conversation


def generate_open_ai_summariser_system_message():
    system_message: str = """
You are good at generating revision notes from technical conversations and can transform highly specific conversations into transferable software engineering principles. You will be given a conversation between a user and a large language model. The user has asked the model to help him with certain problems he faced while programming. 

Follow these instructions:
1. State the topic which the revision notes cover
2. State the goal of the revision notes and what users should learn after reading through the notes.
3. Provide an overview of the key ideas present in the revision notes.
4. List 2-4 key concepts present in the conversation. Each key concept should have a title, an explanation in one or two sentences. If useful, provide a short code example illustrating the corresponding key concept and state the programming language of the code.
"""
    return system_message


def generate_open_ai_summariser_user_message(conversation: Conversation):
    user_message: str = conversation.stringify()
    user_message += "\nSummarise the key ideas of the model's response but avoid referencing the model or the user in your summary. Describe the content as if it is from a textbook:"

    return user_message
