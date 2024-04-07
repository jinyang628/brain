import pytest
from app.control.post.summariser import post_process, _reject_unlikely_topics, _remove_header, _extract_info 

POST_PROCESS_VALID_DATA = [
    (
        """
        **Key Ideas:** 
        1. **Topic1 is good**: This is the summary of the first topic. 
        2. **Topic2 is better**: This is the summary of the second topic. 
        3. **Topic3 is awesome**: This is the summary of the third topic.
        """,
        {
            "Topic1 is good": "This is the summary of the first topic.",
            "Topic2 is better": "This is the summary of the second topic.",
            "Topic3 is awesome": "This is the summary of the third topic."
        }
    )
]

@pytest.mark.parametrize("input_str, expected", POST_PROCESS_VALID_DATA)
def test_post_process_valid(input_str, expected):
    print(post_process(summary=input_str))
    print(expected)
    assert post_process(summary=input_str) == expected

POST_PROCESS_INVALID_DATA = [
    (
        123
    ),
    (
        [
            """
            **Key Ideas:** 
            1. **Topic1**: This is the summary of the first topic. 
            2. **Topic2**: This is the summary of the second topic. 
            3. **Topic3**: This is the summary of the third topic.
            """
        ]
    )
]

@pytest.mark.parametrize("input_str", POST_PROCESS_INVALID_DATA)
def test_post_process_invalid(input_str):
    with pytest.raises(TypeError):
        post_process(summary=input_str)

REJECT_UNLIKELY_TOPICS_ACCEPTED_DATA = [
    (
        {
            "Valid Topic": "Summary"
        }
    )
]
@pytest.mark.parametrize("input_dict", REJECT_UNLIKELY_TOPICS_ACCEPTED_DATA)
def test_reject_unlikely_topics_mixed(input_dict):
    assert _reject_unlikely_topics(input_dict) == None

REJECT_UNLIKELY_TOPICS_REJECTED_DATA = [
    (
        {
            "Topic": "Summary"
        }
    ),
    (
        {
            "": "Summary"
        }
    )
]
@pytest.mark.parametrize("input_dict", REJECT_UNLIKELY_TOPICS_REJECTED_DATA)
def test_reject_unlikely_topics_empty(input_dict):
    with pytest.raises(ValueError):
        _reject_unlikely_topics(input_dict)

REJECT_UNLIKELY_TOPICS_INVALID_DATA = [
    (
        123
    ),
    (
        [
            {
                "Topic": "Summary"
            }
        ]
    ),
    (
        None
    )
]

@pytest.mark.parametrize("input_dict", REJECT_UNLIKELY_TOPICS_INVALID_DATA)
def test_reject_unlikely_topics_invalid(input_dict):
    with pytest.raises(TypeError):
        _reject_unlikely_topics(input_dict)

REMOVE_HEADER_VALID_DATA = [
    (
        """**Key Ideas:** 
        1. **Topic1 happy**: This is the summary of the first topic.
        2. **Topic2 sad**: This is the summary of the second topic.""",
        """1. **Topic1 happy**: This is the summary of the first topic.
        2. **Topic2 sad**: This is the summary of the second topic.""",
    )
]

@pytest.mark.parametrize("input_str, expected", REMOVE_HEADER_VALID_DATA)
def test_remove_header_valid(input_str, expected):
    assert _remove_header(input_str) == expected

EXTRACT_INFO_VALID_DATA = [
    (
        """1. **Time Complexity of Insertion**: Inserting an element at the beginning of a Python list is a linear-time operation (O(n)), while appending at the end is constant-time (O(1)).
        2. **Prepending Using `insert`**: The `list.insert(0, item)` method can be used to prepend an element, but it's less efficient for large lists.""",
        {
            'Time Complexity of Insertion': 'Inserting an element at the beginning of a Python list is a linear-time operation (O(n)), while appending at the end is constant-time (O(1)).',
            'Prepending Using `insert`': "The `list.insert(0, item)` method can be used to prepend an element, but it's less efficient for large lists."
        }
    )
]

@pytest.mark.parametrize("input_str, expected", EXTRACT_INFO_VALID_DATA)
def test_extract_info_valid(input_str, expected):
    assert _extract_info(input_str) == expected