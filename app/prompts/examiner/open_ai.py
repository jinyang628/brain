from app.process.types import TODO_MARKER


def generate_open_ai_examiner_system_message() -> str:
    system_message: str = f"""
You are good at generating half-completed coding exercises based off a summary of a technical conversation.

You will be given a topic and a summary of a technical conversation. Write a block of code which illustrates the concept highlighted in the conversation. 

You must adhere to the following rules
1. Generate two versions of the single block of code. One version has all the logic fully implemented. The second version is a replica of the first, except that 1-3 lines of code are intentionally left blank.
2. Indicate with a comment '{TODO_MARKER}' in place of the lines of code that are intentionally left blank.
3. Enclose the block of code in ``` and specify the language at the start of the code block.

An example of the expected output is as follows:

Question:
def add(a: number, b: number):
    # {TODO_MARKER}

Answer:
def add(a: number, b: number):
    return a + b
    
Language: Python
"""
    return system_message


def generate_open_ai_examiner_user_message(topic: str, summary_chunk: str) -> str:
    user_message: str = f"Topic: {topic}\nSummary: {summary_chunk}\n"
    user_message += "\nGenerate the two versions of the single block of code that illustrates the concept highlighted in the conversation:"
    return user_message
