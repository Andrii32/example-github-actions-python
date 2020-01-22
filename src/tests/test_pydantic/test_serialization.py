
from datetime import datetime, timezone
import pytest


from src.main.models_pydantic import Source, Tag, Post


"""
pydantic does not helps with making objects immutable
hash functions have to be implemented in order to be able put object inside set/frozenset

pydantic can't serialize sets/frozensets with objects inside, because it serializes to dict first
"""


@pytest.mark.parametrize(
    'input, expectation',
    [
        (
            Post(
                timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc),
                source=Source(domain="test", name="test"),
                title="test",
                body=frozenset(["test", "test"]),
                tags=frozenset([Tag(name="test1"), Tag(name="test2"), Tag(name="test3")])
            ),
            pytest.raises(TypeError)  # TypeError: unhashable type: 'dict'
        )
    ]
)
def test_post_json(input, expectation):
    with expectation:
        assert Post.json(input)
