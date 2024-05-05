import pytest

from app.control.post.examiner import (_determine_question_and_answer,
                                       _extract_code, _verify_expected_similarity_and_difference, _verify_todo_marker_presence, post_process)
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
        "python",
        "Print hello",
        "def test():\nprint('Hello')```\n```python\ndef test():\n# TODO: Add the missing line(s) below.",
        "def test():\nprint('Hello')```\n```python\ndef test():\nprint('Hello')",
        (
            "python",
            "Print hello",
            "def test():\nprint('Hello')```\n```python\ndef test():\n# TODO: Add the missing line(s) below.",
            "def test():\nprint('Hello')```\n```python\ndef test():\nprint('Hello')"
        )
    ),
    (
        "javascript",
        "Print hello",
        "function test():\nprint('Hello')```\n```python\ndef test():\n// TODO: Add the missing line(s) below.",
        "function test():\nprint('Hello')```\n```python\ndef test():\nprint('Hello')",
        (
            "javascript",
            "Print hello",
            "function test():\nprint('Hello')```\n```python\ndef test():\n// TODO: Add the missing line(s) below.",
            "function test():\nprint('Hello')```\n```python\ndef test():\nprint('Hello')"
        )
    )
]


@pytest.mark.parametrize("language, question, half_completed_code, fully_completed_code, expected", POST_PROCESS_VALID_DATA)
def test_valid_post_process(language, question, half_completed_code, fully_completed_code, expected):
    language, question, half_completed_code, fully_completed_code = post_process(language=language, question=question, half_completed_code=half_completed_code, fully_completed_code=fully_completed_code)
    assert (language, question, half_completed_code, fully_completed_code) == expected


POST_PROCESS_INVALID_DATA = [
    (
        True,
        "Print hello",
        "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\n# TODO: Add the missing line(s) below.```",
        "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\nprint('Hello')```",
    ),
    (
        "python",
        123,
        "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\n# TODO: Add the missing line(s) below.```",
        "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\nprint('Hello')```",
    ),
    (
        "python",
        123,
        "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\n```",
        "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\nprint('Hello')```",
    ),
    (
        "python",
        "Print hello",
        "```python\ndef test():\nprint('Hello')```\n```python\ndef test():\n# TODO: Add the missing line(s) below.```",
        "```python\ndef test():\nprint('Hello')```\n```python\ndef testing():\nprint('Hello')```",
    )
]


@pytest.mark.parametrize("language, question, half_completed_code, fully_completed_code", POST_PROCESS_INVALID_DATA)
def test_invalid_post_process(language, question, half_completed_code, fully_completed_code):
    with pytest.raises(LogicError):
        post_process(language=language, question=question, half_completed_code=half_completed_code, fully_completed_code=fully_completed_code)

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
        
VERIFY_TODO_MARKER_PRESENCE_VALID_DATA = [
    (
"""
def test():
    # TODO: Add the missing line(s) below.
"""
    ),
    (
"""
function test(): boolean
    // TODO: Add the missing line(s) below.
"""
    )
]

@pytest.mark.parametrize("half_completed_code", VERIFY_TODO_MARKER_PRESENCE_VALID_DATA)
def test_valid_verify_todo_marker_presence(half_completed_code):
    assert _verify_todo_marker_presence(half_completed_code=half_completed_code) == half_completed_code
    
VERIFY_TODO_MARKER_PRESENCE_INVALID_DATA = [
    (
"""
def test():
    # Add the missing line(s) below.
"""
    ),
]

@pytest.mark.parametrize("half_completed_code", VERIFY_TODO_MARKER_PRESENCE_INVALID_DATA)
def test_invalid_verify_todo_marker_presence(half_completed_code):
    with pytest.raises(ValueError):
        _verify_todo_marker_presence(half_completed_code=half_completed_code)