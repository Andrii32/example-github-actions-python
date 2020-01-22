from contextlib import nullcontext as does_not_raise
from datetime import datetime, timezone
import pytest

from src.main.models_marshmallow_dataclasses import Source, Post


"""marshmallow-dataclasses does not validate object fields in moment of initialization"""


@pytest.mark.parametrize(
    'timestamp,expectation',
    [
        (datetime(2020, 1, 1, tzinfo=timezone.utc), does_not_raise()),
        (datetime.now(timezone.utc),                does_not_raise()),
        (datetime.utcnow(),                         does_not_raise()),
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
