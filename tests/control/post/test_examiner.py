import pytest

from app.control.post.examiner import (_determine_question_and_answer,
                                       _extract_code, _verify_expected_similarity_and_difference, post_process)
from app.exceptions.exception import LogicError
from app.llm.model import LLMType

EXTRACT_CODE_VALID_DATA = [
    (
        "```python\nprint('Hello')```\n```python\n# TODO: Add the missing line(s) below.```",
        ("python", "print('Hello')", "# TODO: Add the missing line(s) below."),
    ),
]


@pytest.mark.parametrize("text, expected", EXTRACT_CODE_VALID_DATA)
def test_valid_extract_code(text, expected):
    language, block_1, block_2 = _extract_code(text)
    assert (language, block_1, block_2) == expected


EXTRACT_CODE_INVALID_DATA = [
    ("Some random text"),
]


@pytest.mark.parametrize("text", EXTRACT_CODE_INVALID_DATA)
def test_invalid_extract_code(text):
    with pytest.raises(ValueError):
        _extract_code(text)


# Define test data for _determine_question_and_answer
DETERMINE_QUESTION_AND_ANSWER_VALID_DATA = [
    (
        "def function(): print('Hello')",
        "def test(): # TODO: Add the missing line(s) below.",
        (
            "def test(): # TODO: Add the missing line(s) below.",
            "def function(): print('Hello')",
        ),
    ),
]


@pytest.mark.parametrize(
    "block_1, block_2, expected", DETERMINE_QUESTION_AND_ANSWER_VALID_DATA
)
def test_valid_determine_question_and_answer(block_1, block_2, expected):
    question, answer = _determine_question_and_answer(block_1, block_2)
    assert (question, answer) == expected


DETERMINE_QUESTION_AND_ANSWER_INVALID_DATA = [
    ("def function(): print('Hello')", "def test(): print('World')"),
    ("print('Hello') # TODO: Add the missing line", "print('World')"),
]


@pytest.mark.parametrize("block_1, block_2", DETERMINE_QUESTION_AND_ANSWER_INVALID_DATA)
def test_invalid_determine_question_and_answer(block_1, block_2):
    with pytest.raises(ValueError):
        _determine_question_and_answer(block_1, block_2)


POST_PROCESS_VALID_DATA = [
    (
        "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\n# TODO: Add the missing line(s) below.```",
        LLMType.GEMINI_PRO,
        (
            "python",
            "def test():\n# TODO: Add the missing line(s) below.",
            "def test():\nprint('Hello')",
        ),
    ),
    (
        "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\n# TODO: Add the missing line(s) below.```</output>",
        LLMType.CLAUDE_3_SONNET,
        (
            "python",
            "def test():\n# TODO: Add the missing line(s) below.",
            "def test():\nprint('Hello')",
        ),
    ),
    (
        "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\n# TODO: Add the missing line(s) below.```</output>",
        LLMType.CLAUDE_INSTANT_1,
        (
            "python",
            "def test():\n# TODO: Add the missing line(s) below.",
            "def test():\nprint('Hello')",
        ),
    ),
    (
        "```python\ndef test():\n# TODO: Add the missing line(s) below.```\n```python\ndef test():\nprint('Hello')```",
        LLMType.OPENAI_GPT3_5,
        (
            "python",
            "def test():\n# TODO: Add the missing line(s) below.",
            "def test():\nprint('Hello')",
        ),
    ),
    (
        "```python\ndef test():\n# TODO: Add the missing line(s) below.\nhappy()```\n```python\ndef test():\nprint('Hello')\nhappy()```",
        LLMType.OPENAI_GPT4_TURBO,
        (
            "python",
            "def test():\n# TODO: Add the missing line(s) below.\nhappy()",
            "def test():\nprint('Hello')\nhappy()",
        ),
    ),
]


@pytest.mark.parametrize("practice, llm_type, expected", POST_PROCESS_VALID_DATA)
def test_valid_post_process(practice, llm_type, expected):
    language, question, answer = post_process(practice=practice, llm_type=llm_type)
    assert (language, question, answer) == expected


POST_PROCESS_INVALID_DATA = [
    (
        "Some random text",
        LLMType.GEMINI_PRO,
    ),
    (
        "Some random text",
        LLMType.CLAUDE_3_SONNET,
    ),
    (
        "```python\ndef test():\n# TODO: Add the missing line(s) below.\nprint('Hello')```python\ndef test():\nprint('Hello')\nprint('Hello')```",
        LLMType.COHERE_COMMAND_R,
    ),
    (
        "```python\ndef test():\n# TODO: Add the missing line(s) below.```python\ndef test():\nprint('Hello')```",
        LLMType.COHERE_COMMAND_R,
    ),
]


@pytest.mark.parametrize("practice, llm_type", POST_PROCESS_INVALID_DATA)
def test_invalid_post_process(practice, llm_type):
    with pytest.raises(LogicError):
        post_process(practice=practice, llm_type=llm_type)

VERIFY_EXPECTED_SIMILARITY_AND_DIFFERENCE_VALID_DATA = [
    (
"""
import pydantic

class ExampleModel(pydantic.BaseModel):
    name: str
    age: int

# Create a model instance
model = ExampleModel(name="John", age=30)

# Validation testing - Check if the model is valid
assert model.validate()

# Property testing - Check if the model has the expected properties
assert model.name == "John"
# TODO: Add the missing line(s) below.
""",
"""
import pydantic

class ExampleModel(pydantic.BaseModel):
    name: str
    age: int

# Create a model instance
model = ExampleModel(name="John", age=30)

# Validation testing - Check if the model is valid
assert model.validate()

# Property testing - Check if the model has the expected properties
assert model.name == "John"
assert model.age == 30
""",
"""
import pydantic

class ExampleModel(pydantic.BaseModel):
    name: str
    age: int

# Create a model instance
model = ExampleModel(name="John", age=30)

# Validation testing - Check if the model is valid
assert model.validate()

# Property testing - Check if the model has the expected properties
assert model.name == "John"
# TODO: Add the missing line(s) below.
""",
"""
import pydantic

class ExampleModel(pydantic.BaseModel):
    name: str
    age: int

# Create a model instance
model = ExampleModel(name="John", age=30)

# Validation testing - Check if the model is valid
assert model.validate()

# Property testing - Check if the model has the expected properties
assert model.name == "John"
assert model.age == 30
"""
    ),
    (
"""
import pydantic

class ExampleModel(pydantic.BaseModel):
    name: str
    age: int

# Create a model instance
model = ExampleModel(name="John", age=30)

# Validation testing - Check if the model is valid
# TODO: Add the missing line(s) below.

# Property testing - Check if the model has the expected properties
assert model.name == "John"
assert model.age == 30
""",
"""
import pydantic

class ExampleModel(pydantic.BaseModel):
    name: str
    age: int

# Create a model instance
model = ExampleModel(name="John", age=30)

# Validation testing - Check if the model is valid
assert model.validate()

# Property testing - Check if the model has the expected properties
assert model.name == "John"
assert model.age == 30
""",
"""
import pydantic

class ExampleModel(pydantic.BaseModel):
    name: str
    age: int

# Create a model instance
model = ExampleModel(name="John", age=30)

# Validation testing - Check if the model is valid
# TODO: Add the missing line(s) below.

# Property testing - Check if the model has the expected properties
assert model.name == "John"
assert model.age == 30
""",
"""
import pydantic

class ExampleModel(pydantic.BaseModel):
    name: str
    age: int

# Create a model instance
model = ExampleModel(name="John", age=30)

# Validation testing - Check if the model is valid
assert model.validate()

# Property testing - Check if the model has the expected properties
assert model.name == "John"
assert model.age == 30
"""
    ),
    (
"""
import pydantic

class ExampleModel(pydantic.BaseModel):
    name: str
    age: int

# Create a model instance
model = ExampleModel(name="John", age=30)

# Validation testing - Check if the model is valid
# TODO: Add the missing line(s) below.
""",
"""
import pydantic

class ExampleModel(pydantic.BaseModel):
    name: str
    age: int

# Create a model instance
model = ExampleModel(name="John", age=30)

# Validation testing - Check if the model is valid
assert model.validate()

# Property testing - Check if the model has the expected properties
assert model.name == "John"
assert model.age == 30
""",
"""
import pydantic

class ExampleModel(pydantic.BaseModel):
    name: str
    age: int

# Create a model instance
model = ExampleModel(name="John", age=30)

# Validation testing - Check if the model is valid
# TODO: Add the missing line(s) below.
""",
"""
import pydantic

class ExampleModel(pydantic.BaseModel):
    name: str
    age: int

# Create a model instance
model = ExampleModel(name="John", age=30)

# Validation testing - Check if the model is valid
assert model.validate()

# Property testing - Check if the model has the expected properties
assert model.name == "John"
assert model.age == 30
"""
    ),
    (
"""
# Initialize an empty list to store the structured data
data = []

# Iterate over the data points
for data_point in data_points:
    # TODO: Add the missing line(s) below.
    data.append({'id': data_point['id'], 'value': data_point['value']})

# Construct a DataFrame from the list
df = pd.DataFrame(data)

""",
"""
# Initialize an empty list to store the structured data
data = []

# Iterate over the data points
for data_point in data_points:
    # Append a structured data (e.g., dictionary) to the list
    do_something_productive()
    data.append({'id': data_point['id'], 'value': data_point['value']})

# Construct a DataFrame from the list
df = pd.DataFrame(data)

""",
"""
# Initialize an empty list to store the structured data
data = []

# Iterate over the data points
for data_point in data_points:
    # TODO: Add the missing line(s) below.
    data.append({'id': data_point['id'], 'value': data_point['value']})

# Construct a DataFrame from the list
df = pd.DataFrame(data)

""",
"""
# Initialize an empty list to store the structured data
data = []

# Iterate over the data points
for data_point in data_points:
    # Append a structured data (e.g., dictionary) to the list
    do_something_productive()
    data.append({'id': data_point['id'], 'value': data_point['value']})

# Construct a DataFrame from the list
df = pd.DataFrame(data)

"""
    )
]

@pytest.mark.parametrize("question, answer, expected_returned_question, expected_returned_answer", VERIFY_EXPECTED_SIMILARITY_AND_DIFFERENCE_VALID_DATA)
def test_valid_verify_expected_similarity_and_difference(question, answer, expected_returned_question, expected_returned_answer):
    assert _verify_expected_similarity_and_difference(half_completed_code=question, fully_completed_code=answer) == (expected_returned_question, expected_returned_answer)
    
VERIFY_EXPECTED_SIMILARITY_AND_DIFFERENCE_INVALID_DATA = [
    (
"""
# Initialize an empty list to store the structured data
data = []

# Iterate over the data points
for data_point in data_points:
    # TODO: Add the missing line(s) below.
    data.append({'id': data_point['id'], 'value': data_point['value']})

# Construct a DataFrame from the list
df = pd.DataFrame(data)

""",
"""
# Initialize an empty list to store the structured data
data = []

# Iterate over the data points
for data_point in data_points:
    # Append a structured data (e.g., dictionary) to the list
    data.append({'id': data_point['id'], 'value': data_point['value']})

# Construct a DataFrame from the list
df = pd.DataFrame(data)

""",
    )
]

@pytest.mark.parametrize("question, answer", VERIFY_EXPECTED_SIMILARITY_AND_DIFFERENCE_INVALID_DATA)
def test_invalid_verify_expected_similarity_and_difference(question, answer):
    with pytest.raises(ValueError):
        _verify_expected_similarity_and_difference(half_completed_code=question, fully_completed_code=answer)