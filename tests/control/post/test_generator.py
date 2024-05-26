import pytest

from app.control.post.generator import (
    _reject_unlikely_topics,
    post_process,
    _verify_expected_similarity_and_difference, 
    _verify_todo_marker_presence, 
)
from app.exceptions.exception import LogicError


POST_PROCESS_VALID_DATA = [
    (
        "Good topic",
        "A good goal",
        "A good overview",
        [
           {
                "key_concept_title": "A good title",
                "key_concept_explanation": "A good explanation",
                "key_concept_code_example": {
                    "key_concept_code": "A good code",
                    "key_concept_language": "A good language"
                }
            } 
        ],
        [
            {
                "tip_title": "A good title",
                "tip_explanation": "A good explanation"
            }
        ],
        {
            "mcq_practice_title": "A good title",
            "mcq_practice_question": "A good question",
            "mcq_practice_correct_option": "A good option",
            "mcq_practice_wrong_options": ["A good option", "Another good option"]
        },
        {
            "code_practice_title": "A good title",
            "code_practice_question": "A good question",
            "code_practice_half_completed_code": "A good code\nTODO: Add the missing line(s) below.",
            "code_practice_fully_completed_code": "A good code\ntesttesttest",
            "code_practice_language": "A good language"
        },
        {
            "topic": "Good topic",
            "goal": "A good goal",
            "overview": "A good overview",
            "key_concepts": [
                {
                    "key_concept_title": "A good title",
                    "key_concept_explanation": "A good explanation",
                    "key_concept_code_example": {
                        "key_concept_code": "A good code",
                        "key_concept_language": "A good language"
                    }
                }
            ],
            "tips": [
                {
                    "tip_title": "A good title",
                    "tip_explanation": "A good explanation"
                }
            ],
            "mcq_practice": {
                "mcq_practice_title": "A good title",
                "mcq_practice_question": "A good question",
                "mcq_practice_correct_option": "A good option",
                "mcq_practice_wrong_options": ["A good option", "Another good option"]
            },
            "code_practice": {
                "code_practice_title": "A good title",
                "code_practice_question": "A good question",
                "code_practice_half_completed_code": "A good code\nTODO: Add the missing line(s) below.",
                "code_practice_fully_completed_code": "A good code\ntesttesttest",
                "code_practice_language": "A good language"
            }
        }
    )
]


@pytest.mark.parametrize("topic, goal, overview, key_concepts_lst, tips_lst, mcq_practice, code_practice, expected", POST_PROCESS_VALID_DATA)
def test_post_process_valid(topic, goal, overview, key_concepts_lst, tips_lst, mcq_practice, code_practice, expected):
    assert post_process(topic=topic, goal=goal, overview=overview, key_concepts_lst=key_concepts_lst, tips_lst=tips_lst,  mcq_practice=mcq_practice, code_practice=code_practice) == expected

POST_PROCESS_INVALID_DATA = [
    (
        "Good topic",
        "A good goal",
        "A good overview",
        [
           {
                "key_concept_title": "A good title",
                "key_concept_explanation": "A good explanation",
                "key_concept_code_example": {
                    "key_concept_code": "A good code",
                    "key_concept_language": "A good language"
                }
            } 
        ],
        [
            {
                "tip_title": "A good title",
                "tip_explanation": "A good explanation"
            }
        ],
        {
            "mcq_practice_title": "A good title",
            "mcq_practice_question": "A good question",
            "mcq_practice_correct_option": "A good option",
            "mcq_practice_wrong_options": ["A good option", "Another good option"]
        },
        {
            "code_practice_title": "A good title",
            "code_practice_question": "A good question",
            "code_practice_half_completed_code": "A good code",
            "code_practice_fully_completed_code": "A good code\ntesttesttest",
            "code_practice_language": "A good language"
        }
    ),
    (
        "Good topic",
        "A good goal",
        123,
        [
           {
                "key_concept_title": "A good title",
                "key_concept_explanation": "A good explanation",
                "key_concept_code_example": {
                    "key_concept_code": "A good code",
                    "key_concept_language": "A good language"
                }
            } 
        ],
        [
            {
                "tip_title": "A good title",
                "tip_explanation": "A good explanation"
            }
        ],
        {
            "mcq_practice_title": "A good title",
            "mcq_practice_question": "A good question",
            "mcq_practice_correct_option": "A good option",
            "mcq_practice_wrong_options": ["A good option", "Another good option"]
        },
        {
            "code_practice_title": "A good title",
            "code_practice_question": "A good question",
            "code_practice_half_completed_code": "A good code",
            "code_practice_fully_completed_code": "A good code\ntesttesttest",
            "code_practice_language": "A good language"
        }
    )
]


@pytest.mark.parametrize("topic, goal, overview, key_concepts_lst, tips_lst, mcq_practice, code_practice", POST_PROCESS_INVALID_DATA)
def test_post_process_invalid(topic, goal, overview, key_concepts_lst, tips_lst, mcq_practice, code_practice):
    with pytest.raises(LogicError):
        post_process(topic=topic, goal=goal, overview=overview, key_concepts_lst=key_concepts_lst, tips_lst=tips_lst, mcq_practice=mcq_practice, code_practice=code_practice)


REJECT_UNLIKELY_TOPICS_ACCEPTED_DATA = [
    ("Good topic that is long enough")
]


@pytest.mark.parametrize("topic", REJECT_UNLIKELY_TOPICS_ACCEPTED_DATA)
def test_reject_unlikely_topics_mixed(topic):
    assert _reject_unlikely_topics(topic=topic) == None


REJECT_UNLIKELY_TOPICS_REJECTED_DATA = [
    ("Topic"), 
    ("")
]


@pytest.mark.parametrize("topic", REJECT_UNLIKELY_TOPICS_REJECTED_DATA)
def test_reject_unlikely_topics_invalid(topic):
    with pytest.raises(ValueError):
        _reject_unlikely_topics(topic=topic)
        
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

"""
    )
]

@pytest.mark.parametrize("question, answer", VERIFY_EXPECTED_SIMILARITY_AND_DIFFERENCE_VALID_DATA)
def test_valid_verify_expected_similarity_and_difference(question, answer):
    assert _verify_expected_similarity_and_difference(half_completed_code=question, fully_completed_code=answer) == None
    
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
    ),
    (
"""
# Define User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    preferences = Column(JSON, nullable=True) # TODO: Add the missing line(s) below.

# TODO: Add the missing line(s) below.
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
""",
"""
# Define User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    preferences = Column(JSON, nullable=True)

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
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
    assert _verify_todo_marker_presence(half_completed_code=half_completed_code) == None
    
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