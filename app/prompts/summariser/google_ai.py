from app.models.conversation import Conversation


def generate_google_ai_summariser_system_message():
    system_message: str = """
You are good at summarizing technical conversations and can explain complex software engineering concepts in a way that is easy to understand. 

You will be given a conversation between a user and a large language model. The user has asked the model to help him with certain problems he faced while programming. Summarise the key ideas present in the model's response.

Here is an example of the expected output format: 

**Key Ideas:**
1. **Topic**: This is the summary of the first topic.
2. **Topic**: This is the summary of the second topic.
3. **Topic**: This is the summary of the third topic.
"""
    return system_message


def generate_google_ai_summariser_user_message(conversation: Conversation):
    user_message: str = conversation.stringify()
    user_message += (
        "\n Summarise the key ideas of the model's response in the conversation:"
    )

    return user_message
