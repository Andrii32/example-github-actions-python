import json
from datetime import datetime, timezone
import pytest


from src.main.models_dataclasses_json import Source, Tag, Post, FrozenSetPost


"""dataclasses-json works fine with objects in frozenset"""


@pytest.mark.parametrize(
    'input, output',
    [
        (
            Post(
                timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc),
                source=Source(domain="test", name="test"),
                title="test",
                body=frozenset(["test", "test"]),
                tags=frozenset([Tag(name="test1"), Tag(name="test2"), Tag(name="test3")])
            ),
            {
                "timestamp": datetime(2020, 1, 1, tzinfo=timezone.utc).isoformat(),
                "source": {"domain": "test", "name": "test"},
                "title": "test",
                "body": ["test"],
                "tags": [{"name": "test1"}, {"name": "test2"}, {"name": "test3"}],
            }
        )
    ]
)
def test_to_json(input, output):
    first = Post.from_json(Post.to_json(input))
    second = Post.from_json(json.dumps(output))
    assert first.__hash__() == second.__hash__()
    assert first == second


@pytest.mark.parametrize(
    'input, output',
    [
        (
            FrozenSetPost(
                values=frozenset(
                    [
                        Post(
                            timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc),
                            source=Source(domain="test", name="test"),
                            title="test",
                            body=frozenset(["test", "test"]),
                            tags=frozenset([Tag(name="test1"), Tag(name="test2"), Tag(name="test3")])
                        )
                    ]
                )
            ),
            {
                "values": [
                    {
                        "timestamp": datetime(2020, 1, 1, tzinfo=timezone.utc).isoformat(),
                        "source": {"domain": "test", "name": "test"},
                        "title": "test",
                        "body": ["test"],
                        "tags": [{"name": "test1"}, {"name": "test2"}, {"name": "test3"}],
                    }
                ]
            }
        ),
    ]
)
def test_to_json_union(input, output):
    assert frozenset([1, 2, 3]) == frozenset([3, 2, 1])
    first = FrozenSetPost.from_json(FrozenSetPost.to_json(input))
    second = FrozenSetPost.from_json(json.dumps(output))
    assert first == second
