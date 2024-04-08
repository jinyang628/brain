def generate_google_ai_examiner_system_message() -> str:
    system_message: str = """
You are good at generating half-completed coding exercises based off a summary of a technical conversation.

You will be given a topic and a summary of a technical conversation. Write a block of code which illustrates the concept highlighted in the conversation. 

You must adhere to the following rules
1. Generate two versions of the single block of code. One version has all the logic fully implemented. The second version is a replica of the first, except that 1 line of code is intentionally left blank.
2. Indicate with '# TODO: Add the missing line below.' above the line of code that is intentionally left blank.
3. Enclose the block of code in ``` and specify the language at the start of the code block.

Here is an example of the expected output format:

Practice:
```python
def example_function():
    # This is an example of the code that illustrates the concept highlighted in the conversation.
    foo()
    bar()
    # TODO: Add the missing line below.
    baz()
```

Answer:
```python
def example_function():
    # This is an example of the code that illustrates the concept highlighted in the conversation.
    foo()
    bar()
    cat()
    baz()
```
"""
    return system_message


def generate_google_ai_examiner_user_message(topic: str, content: str) -> str:
    user_message: str = f"Topic: {topic}\nContent: {content}\n"
    user_message += "\nWrite a block of code that illustrates the concept highlighted in the conversation:"
    return user_message
