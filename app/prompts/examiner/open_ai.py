from app.process.types import TODO_MARKER


def generate_open_ai_examiner_system_message() -> str:
    system_message: str = f"""
You are good at generating half-completed coding exercises based off a summary of a technical conversation.

You will be given a topic and a summary of a technical conversation. Come up with a coding question based on the content, and write a half-completed block of code with 1-3 lines intentionally left blank for the student to fill up. Indicate with a comment '{TODO_MARKER}' in place of the lines of code that are intentionally left blank. 

You should also provide a fully completed version of the code, which is an exact replica of the half-completed block of code, except that the `{TODO_MARKER}` is now replaced with the actual 1-3 lines of expected code. 

Give enough hints and context within the question such that the student can complete the code without any ambiguity.

An example of the expected output is as follows:

Question:
Write a function that adds two numbers together.

Half-completed code:
def add(a: number, b: number):
    # {TODO_MARKER}

Fully-completed code:
def add(a: number, b: number):
    return a + b
    
Language: Python
"""
    return system_message


def generate_open_ai_examiner_user_message(topic: str, summary_chunk: str) -> str:
    user_message: str = f"Topic: {topic}\nSummary: {summary_chunk}\n"
    user_message += "\nGenerate the two versions of the single block of code that illustrates the concept highlighted in the conversation:"
    return user_message
