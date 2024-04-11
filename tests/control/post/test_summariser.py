import pytest

from app.control.post.summariser import (_extract_info,
                                         _reject_unlikely_topics,
                                         _remove_header, post_process)

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
            "Topic3 is awesome": "This is the summary of the third topic.",
        },
    )
]


@pytest.mark.parametrize("input_str, expected", POST_PROCESS_VALID_DATA)
def test_post_process_valid(input_str, expected):
    assert post_process(summary=input_str) == expected


POST_PROCESS_INVALID_DATA = [
    (123),
    (
        [
            """
            **Key Ideas:** 
            1. **Topic1**: This is the summary of the first topic. 
            2. **Topic2**: This is the summary of the second topic. 
            3. **Topic3**: This is the summary of the third topic.
            """
        ]
    ),
]


@pytest.mark.parametrize("input_str", POST_PROCESS_INVALID_DATA)
def test_post_process_invalid(input_str):
    with pytest.raises(TypeError):
        post_process(summary=input_str)


REJECT_UNLIKELY_TOPICS_ACCEPTED_DATA = [({"Valid Topic": "Summary"})]


@pytest.mark.parametrize("input_dict", REJECT_UNLIKELY_TOPICS_ACCEPTED_DATA)
def test_reject_unlikely_topics_mixed(input_dict):
    assert _reject_unlikely_topics(input_dict) == None


REJECT_UNLIKELY_TOPICS_REJECTED_DATA = [({"Topic": "Summary"}), ({"": "Summary"})]


@pytest.mark.parametrize("input_dict", REJECT_UNLIKELY_TOPICS_REJECTED_DATA)
def test_reject_unlikely_topics_empty(input_dict):
    with pytest.raises(ValueError):
        _reject_unlikely_topics(input_dict)


REJECT_UNLIKELY_TOPICS_INVALID_DATA = [(123), ([{"Topic": "Summary"}]), (None)]


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
        """
1. **List Indentation Fix**: The `ResponseProcessor` class is responsible for processing the response based on `fact_id_process_type` and `query_process_type`. It can be customized to remove additional indentation from lists of strings in the JSON output. 
        
2. **Regex Complexity**: Regular expressions can be computationally expensive, especially for complex patterns, large texts, or when they involve backtracking.
        """,
        {
            "List Indentation Fix": "The `ResponseProcessor` class is responsible for processing the response based on `fact_id_process_type` and `query_process_type`. It can be customized to remove additional indentation from lists of strings in the JSON output.",
            "Regex Complexity": "Regular expressions can be computationally expensive, especially for complex patterns, large texts, or when they involve backtracking.",
        },
    )
]


@pytest.mark.parametrize("input_str, expected", EXTRACT_INFO_VALID_DATA)
def test_extract_info_valid(input_str, expected):
    assert _extract_info(input_str) == expected
