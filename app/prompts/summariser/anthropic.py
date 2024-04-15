from app.models.conversation import Conversation


def generate_anthropic_summariser_system_message():
    system_message: str = """
You are good at summarizing technical conversations and can explain complex software engineering concepts in a way that is easy to understand. You will be given a conversation between a user and a large language model in <conversation></conversation> tags. The user has asked the model to help him with certain problems he faced while programming. 

Follow these instructions in <instruction></instruction> tags:
<instruction>
1. Summarise the key ideas present in the model's response without referencing specific function or variable names.
2. Avoid narrating the conversation history without adding value to the summary.
3. Try to generalise and avoid being too specific to the examples present in the conversation, so that the summary can be applied to a wide range of similar scenarios.
</instruction>

An example of the expected output format is as follows:

<output>
**Key Ideas:**
1. **Topic**: This is the summary of the first topic.
2. **Topic**: This is the summary of the second topic.
3. **Topic**: This is the summary of the third topic.
</output>
"""
    return system_message


def generate_anthropic_summariser_user_message(conversation: Conversation):
    user_message: str = f"<conversation>\n{conversation.stringify()}\n</conversation>\n"
    user_message += (
        "Summarise the key ideas of the model's response in the conversation:"
    )

    return user_message
