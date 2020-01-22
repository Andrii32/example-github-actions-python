import json
from contextlib import nullcontext as does_not_raise
from datetime import datetime, timezone
import pytest

from pydantic import error_wrappers

from src.main.models_pydantic import Source, Post


"""pydantic validates object fields in moment of initialization"""


@pytest.mark.parametrize(
    'timestamp,expectation',
    [
        (datetime(2020, 1, 1, tzinfo=timezone.utc), does_not_raise()),
        (datetime.now(timezone.utc),                does_not_raise()),
        (datetime.utcnow(),                         pytest.raises(error_wrappers.ValidationError)),
    ]
)
def test_timestamp_validation_initialize(timestamp, expectation):
    with expectation:
        Post(
            timestamp=timestamp,
            source=Source(domain='test', name='test'),
            title='test',
            body=frozenset(),
            tags=frozenset()
        )


"""pydantic validates object fields in moment of initialization"""


@pytest.mark.parametrize(
    'timestamp,expectation',
    [
        (datetime(2020, 1, 1, tzinfo=timezone.utc), does_not_raise()),
        (datetime.now(timezone.utc),                does_not_raise()),
        (datetime.utcnow(),                         pytest.raises(error_wrappers.ValidationError)),
    ]
)
def test_timestamp_validation_deserialize(timestamp, expectation):
    with expectation:
        Post.parse_raw(
            json.dumps({
                "timestamp": timestamp.isoformat(),
                "source": {"domain": 'test', "name": 'test'},
                "title": 'test',
                "body": [],
                "tags": []
            })
        )
