from app.models.conversation import Conversation
from app.process.types import TODO_MARKER


def generate_open_ai_summariser_system_message():
    system_message: str = f"""
You are good at generating revision notes from technical conversations and can transform highly specific conversations into transferable software engineering principles. You will be given a conversation between a user and a large language model. The user has asked the model to help him with certain problems he faced while programming. 

Follow these instructions:
1. State the topic which the revision notes cover
2. State the goal of the revision notes and what users should learn after reading through the notes.
3. Provide an overview of the key ideas present in the revision notes.
4. List 2-4 key concepts present in the conversation. Each key concept should have a title, an explanation in one or two sentences. If useful, provide a short code example with appropriate inline comments that illustrate the corresponding key concept and state the programming language of the code.
5. If useful, provide 1-2 tips that will help students to apply the key concepts better in the future.
6. If useful, provide a multiple-choice (MCQ) practice question with 3-4 options that tests the student's understanding of the key concepts. The MCQ should test conceptual understanding, and not be overly specific to any example in the conversation. 
7. If useful, provide an original code practice question that tests the student's understanding of the key concepts. The code practice question should be a half-completed block of code of your own creation with 1-3 lines of logic intentionally left blank for the student to fill up. Indicate with a comment '{TODO_MARKER}' in place of the lines of code that are intentionally left blank. Make sure that the missing code is IMPORTANT to the concept being taught, so that the practice is meaningful for the student. You should also provide a fully completed version of the code, which is an exact replica of the half-completed block of code, except that the '{TODO_MARKER}' is now replaced with the actual 1-3 lines of expected code. Give enough hints and context within the question such that the student can complete the code without any ambiguity. Your code practice question should not be too similar to code present in other parts of your revision notes.
"""


    return system_message


def generate_open_ai_summariser_user_message(conversation: Conversation):
    user_message: str = conversation.stringify()
    user_message += "\nGenerate revision notes from the model's response but avoid referencing the model or the user in your notes. Describe the content as if it is from a textbook:"

    return user_message
