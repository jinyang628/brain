from app.models.conversation import Conversation


def generate_google_ai_summariser_system_message():
    system_message: str = """
    You are very good at summarizing technical conversations and can explain complex software engineering concepts in a way that is easy to understand. You will be given a conversation between a user and a large language model. Summarise the key ideas.  
    """
    return system_message


def generate_google_ai_summariser_user_message(conversation: Conversation):
    user_message: str = conversation.stringify()
    user_message += "\n Summarise the key ideas in the conversation:"

    return user_message
