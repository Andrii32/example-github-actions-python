import json
from datetime import datetime, timezone
import pytest


from dataclasses_avroschema import AvroModel, types

from src.main.models_dataclasses_avroschema import (
    Source, Tag, Post, FrozenSetTag, FrozenSetPost, DateField
)


@pytest.mark.parametrize(
    'input, output',
    [
        (
            Tag,
            '{"type": "record", "name": "Tag", "fields": [{"name": "name", "type": "string"}], "doc": "Tag(name: str)"}'
        ),
        (
            Source,
            '{"type": "record", "name": "Source", "fields": [{"name": "domain", "type": "string"}, {"name": "name", "type": ["string", "null"]}], "doc": "Source(domain: str, name: Union[str, NoneType])"}'
        ),
        (
            DateField,
            '{"type": "record", "name": "DateField", "fields": [{"name": "value", "type": {"type": "long", "logicalType": "timestamp-millis"}}], "doc": "DateField(value: datetime.datetime)"}'
        )
    ]
)
def test_schema_success(input, output):
    assert input.avro_schema() == output


"""
dataclasses-avroschema can't create a schema for dataclass with set,frozenset objects
"""


@pytest.mark.parametrize(
    'input, output',
    [
        (
            FrozenSetTag,
            None
        ),
        (
            FrozenSetPost,
            None
        )
    ]
)
def test_schema_failure(input, output):
    with pytest.raises(ValueError):
        assert input.avro_schema() == output

