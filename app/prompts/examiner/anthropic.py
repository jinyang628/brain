from app.process.types import TODO_MARKER


def generate_anthropic_examiner_system_message() -> str:
    system_message: str = f"""
You are good at generating half-completed coding exercises based off a summary of a technical conversation.

You will be given a topic and a summary of a technical conversation within <conversation></conversation> tags. Write a block of code which illustrates the concept highlighted in the conversation. 

You must adhere to the following rules
1. Generate two versions of the single block of code within <output></output> tags. One version has all the logic fully implemented and should be written within <practice></practice> tags. The second version is a replica of the first, except that 1-3 lines of code are intentionally left blank and should be written within <answer></answer> tags.
2. Indicate with '{TODO_MARKER}' in place of the lines of code that are intentionally left blank.
3. Enclose the block of code in ``` and specify the language at the start of the code block.

Here is an example of the expected output format:

<output>
<practice>
```python
def contains_greater_than_five():
    # This code checks if at least one item in a list is greater than 5.
    my_list = [1, 2, 3, 4, 5, 6]
    {TODO_MARKER}
        print("At least one item is greater than 5.")
    else:
        print("No item is greater than 5.")
```
</practice>

<answer>
```python
def contains_greater_than_five():
    # This code checks if at least one item in a list is greater than 5.
    my_list = [1, 2, 3, 4, 5, 6]
    if any(x > 5 for x in my_list):
        print("At least one item is greater than 5.")
    else:
        print("No item is greater than 5.")
```
</answer>
</output>
"""
    return system_message


def generate_anthropic_examiner_user_message(topic: str, summary_chunk: str) -> str:
    user_message: str = (
        f"<conversation>\nTopic: {topic}\nSummary: {summary_chunk}\n</conversation>\n"
    )
    user_message += "\nGenerate the two versions of the single block of code that illustrates the concept highlighted in the conversation: <output>"
    return user_message
