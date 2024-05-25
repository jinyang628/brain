import pytest

from app.control.post.generator import (
    _reject_unlikely_topics,
    post_process
)
from app.exceptions.exception import LogicError

POST_PROCESS_VALID_DATA = [
    (
        "Good topic",
        "A good summary",
        {
            "Good topic": "A good summary"
        }
    )
]


@pytest.mark.parametrize("topic, content, expected", POST_PROCESS_VALID_DATA)
def test_post_process_valid(topic, content, expected):
    assert post_process(topic=topic, content=content) == expected


POST_PROCESS_INVALID_DATA = [
    (123, "content"),
    (
        [
            """
            **Key Ideas:** 
            1. **Topic1**: This is the summary of the first topic. 
            2. **Topic2**: This is the summary of the second topic. 
            3. **Topic3**: This is the summary of the third topic.
            """
        ],
        "GOOD CONTENT"
    ),
]


@pytest.mark.parametrize("topic, content", POST_PROCESS_INVALID_DATA)
def test_post_process_invalid(topic, content):
    with pytest.raises(LogicError):
        post_process(topic=topic, content=content)


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