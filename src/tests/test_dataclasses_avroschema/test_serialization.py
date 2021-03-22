import json
from datetime import datetime, timezone
import pytest

from src.main.models_dataclasses_avroschema import (
    Source, Tag, Post, FrozenSetTag, FrozenSetPost, DateField
)


@pytest.mark.parametrize(
    'input, output_bytes, output_avro_json, output_json',
    [
        (
            Source(domain="test", name="test"),
            b'\x08test\x00\x08test',
            b'{"domain": "test", "name": {"string": "test"}}',
            {'domain': 'test', 'name': 'test'}
        ),
        (
            Source(domain="test", name=None),
            b'\x08test\x02',
            b'{"domain": "test", "name": null}',
            {'domain': 'test', 'name': None}
        )
    ]
)
def test_to_json(input, output_bytes, output_avro_json, output_json):
    assert input.serialize() == output_bytes
    assert input.serialize(serialization_type="avro-json") == output_avro_json
    assert input.to_json() == output_json
