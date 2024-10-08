from app.process.types import TODO_MARKER


def generate_cohere_examiner_system_message() -> str:
    system_message: str = f"""
## Role
You are good at generating half-completed coding exercises based off a summary of a technical conversation.

## Task
You will be given a topic and a summary of a technical conversation. Write a block of code which illustrates the concept highlighted in the conversation. 

## Instructions
1. Generate two versions of the single block of code. One version has all the logic fully implemented. The second version is a replica of the first, except that 1-3 lines of code are intentionally left blank.
2. Indicate with '{TODO_MARKER}' in place of the lines of code that are intentionally left blank.
3. Enclose the block of code in ``` and specify the language at the start of the code block.

## Expected Output Format
Practice:
```python
def contains_greater_than_five():
    # This code checks if at least one item in a list is greater than 5.
    my_list = [1, 2, 3, 4, 5, 6]
    {TODO_MARKER}
        print("At least one item is greater than 5.")
    else:
        print("No item is greater than 5.")
```

Answer:
```python
def contains_greater_than_five():
    # This code checks if at least one item in a list is greater than 5.
    my_list = [1, 2, 3, 4, 5, 6]
    if any(x > 5 for x in my_list):
        print("At least one item is greater than 5.")
    else:
        print("No item is greater than 5.")
```
"""
    return system_message


def generate_cohere_examiner_user_message(topic: str, summary_chunk: str) -> str:
    user_message: str = f"Topic: {topic}\nSummary: {summary_chunk}\n"
    user_message += "\nGenerate the two versions of the single block of code that illustrates the concept highlighted in the conversation:"
    return user_message
