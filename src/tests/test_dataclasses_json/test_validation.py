import json
from contextlib import nullcontext as does_not_raise
from datetime import datetime, timezone
import pytest

from src.main.models_dataclasses_json import Source, Post


"""validation is done using dataclasses __post_init__"""


@pytest.mark.parametrize(
    'timestamp,expectation',
    [
        (datetime(2020, 1, 1, tzinfo=timezone.utc), does_not_raise()),
        (datetime.now(timezone.utc),                does_not_raise()),
        (datetime.utcnow(),                         pytest.raises(ValueError)),
    ]
)
def test_timestamp_validation_on_initialization(timestamp, expectation):
    with expectation:
        Post(
            timestamp=timestamp,
            source=Source(domain='test', name='test'),
            title='test',
            body=frozenset(),
            tags=frozenset()
        )


"""marshmallow-dataclasses does not validate object fields in moment of serialization"""


@pytest.mark.parametrize(
    'timestamp,expectation',
    [
        (datetime(2020, 1, 1, tzinfo=timezone.utc), does_not_raise()),
        (datetime.now(timezone.utc),                does_not_raise()),
        (datetime.utcnow(),                         pytest.raises(ValueError)),
    ]
)
def test_timestamp_validation_on_serialization(timestamp, expectation):
    with expectation:
        Post.to_json(
            Post(
                timestamp=timestamp,
                source=Source(domain='test', name='test'),
                title='test',
                body=frozenset(),
                tags=frozenset()
            )
        )


"""marshmallow-dataclasses validates object fields in moment of deserialization"""


@pytest.mark.parametrize(
    'timestamp,expectation',
    [
        (datetime(2020, 1, 1, tzinfo=timezone.utc), does_not_raise()),
        (datetime.now(timezone.utc),                does_not_raise()),
        (datetime.utcnow(),                         pytest.raises(ValueError)),
    ]
)
def test_timestamp_validation_on_deserialization(timestamp, expectation):
    with expectation:
        Post.from_json(
            json.dumps(
                {
                    "timestamp": timestamp.isoformat(),
                    "source": {"domain": 'test', "name": 'test'},
                    "title": 'test',
                    "body": [],
                    "tags": []
                }
            )
        )
