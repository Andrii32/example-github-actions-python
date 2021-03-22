from typing import Optional, FrozenSet, List
from datetime import datetime, timezone

from dataclasses import dataclass, field
from dataclasses_avroschema import AvroModel, types
import pytest


from .schemas import Tag, Source, SuperBody, v1, v2, v3, v4, v5


def test_schema_evolution():
    v1_post = v1.Post(
        timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc),
        source=Source(domain="test", name="test"),
        title="test",
        body=["test", "test"],
    )
    v2_post = v2.Post(
        timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc),
        title="test",
        body=["test", "test"],
    )
    v3_post = v3.Post(
        timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc),
        source=Source(domain="test", name="test"),
        title="test",
        body=["test", "test"],
        tags=[Tag(name="test1"), Tag(name="test2"), Tag(name="test3")]
    )
    v4_post = v4.Post(
        timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc),
        source=Source(domain="test", name="test"),
        title="test",
        content=["test", "test"],
    )
    v5_post = v5.Post(
        timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc),
        source=Source(domain="test", name="test"),
        title="test",
        body=SuperBody(
            value="test",
            tags=[Tag(name="test1"), Tag(name="test2"), Tag(name="test3")]
        ),
    )

    assert v1.Post.avro_schema() == '{"type": "record", "name": "Post", "fields": [{"name": "timestamp", "type": {"type": "long", "logicalType": "timestamp-millis"}}, {"name": "source", "type": {"type": "record", "name": "source_record", "fields": [{"name": "domain", "type": "string"}, {"name": "name", "type": ["string", "null"]}], "doc": "Source(domain: str, name: Union[str, NoneType])"}}, {"name": "title", "type": "string"}, {"name": "body", "type": {"type": "array", "items": "string", "name": "body"}}], "doc": "Post(timestamp: datetime.datetime, source: test_dataclasses_avroschema.test_schema_evolution.schemas.common.Source, title: str, body: List[str])"}'
    assert v2.Post.avro_schema() == '{"type": "record", "name": "Post", "fields": [{"name": "timestamp", "type": {"type": "long", "logicalType": "timestamp-millis"}}, {"name": "title", "type": "string"}, {"name": "body", "type": {"type": "array", "items": "string", "name": "body"}}], "doc": "Post(timestamp: datetime.datetime, title: str, body: List[str])"}'
    assert v3.Post.avro_schema() == '{"type": "record", "name": "Post", "fields": [{"name": "timestamp", "type": {"type": "long", "logicalType": "timestamp-millis"}}, {"name": "source", "type": {"type": "record", "name": "source_record", "fields": [{"name": "domain", "type": "string"}, {"name": "name", "type": ["string", "null"]}], "doc": "Source(domain: str, name: Union[str, NoneType])"}}, {"name": "title", "type": "string"}, {"name": "body", "type": {"type": "array", "items": "string", "name": "body"}}, {"name": "tags", "type": {"type": "array", "items": {"type": "record", "name": "tag_record", "fields": [{"name": "name", "type": "string"}], "doc": "Tag(name: str)"}, "name": "tag"}}], "doc": "Post(timestamp: datetime.datetime, source: test_dataclasses_avroschema.test_schema_evolution.schemas.common.Source, title: str, body: List[str], tags: List[test_dataclasses_avroschema.test_schema_evolution.schemas.common.Tag])"}'
    assert v4.Post.avro_schema() == '{"type": "record", "name": "Post", "fields": [{"name": "timestamp", "type": {"type": "long", "logicalType": "timestamp-millis"}}, {"name": "source", "type": {"type": "record", "name": "source_record", "fields": [{"name": "domain", "type": "string"}, {"name": "name", "type": ["string", "null"]}], "doc": "Source(domain: str, name: Union[str, NoneType])"}}, {"name": "title", "type": "string"}, {"name": "content", "type": {"type": "array", "items": "string", "name": "content"}}], "doc": "Post(timestamp: datetime.datetime, source: test_dataclasses_avroschema.test_schema_evolution.schemas.common.Source, title: str, content: List[str])"}'
    assert v5.Post.avro_schema() == '{"type": "record", "name": "Post", "fields": [{"name": "timestamp", "type": {"type": "long", "logicalType": "timestamp-millis"}}, {"name": "source", "type": {"type": "record", "name": "source_record", "fields": [{"name": "domain", "type": "string"}, {"name": "name", "type": ["string", "null"]}], "doc": "Source(domain: str, name: Union[str, NoneType])"}}, {"name": "title", "type": "string"}, {"name": "body", "type": {"type": "record", "name": "body_superbody_record", "fields": [{"name": "value", "type": "string"}, {"name": "tags", "type": {"type": "array", "items": {"type": "record", "name": "tag_record", "fields": [{"name": "name", "type": "string"}], "doc": "Tag(name: str)"}, "name": "tag"}}], "doc": "SuperBody(value: str, tags: List[test_dataclasses_avroschema.test_schema_evolution.schemas.common.Tag])"}}], "doc": "Post(timestamp: datetime.datetime, source: test_dataclasses_avroschema.test_schema_evolution.schemas.common.Source, title: str, body: test_dataclasses_avroschema.test_schema_evolution.schemas.common.SuperBody)"}'

    # =====================================
    # FIELD REMOVED
    # =====================================
    assert v1_post.serialize(serialization_type="avro-json") == b'{"timestamp": 1577836800000, "source": {"domain": "test", "name": {"string": "test"}}, "title": "test", "body": ["test", "test"]}'
    with pytest.raises(StopIteration):
        v2.Post.deserialize(v1_post.serialize(serialization_type="avro-json"))
    # FAILURE: PostV2 can't deserialize PostV1
    assert v2_post.serialize(serialization_type="avro-json") ==  b'{"timestamp": 1577836800000, "title": "test", "body": ["test", "test"]}'
    with pytest.raises(IndexError):
        v1.Post.deserialize(v2_post.serialize(serialization_type="avro-json"))
    # FAILURE: PostV1 can't deserialize PostV2

    # =====================================
    # FIELD ADDED
    # =====================================
    assert v1_post.serialize(serialization_type="avro-json") == b'{"timestamp": 1577836800000, "source": {"domain": "test", "name": {"string": "test"}}, "title": "test", "body": ["test", "test"]}'
    with pytest.raises(IndexError):
        v3.Post.deserialize(v1_post.serialize(serialization_type="avro-json"))
    # FAILURE: PostV3 can't deserialize PostV1
    assert v3_post.serialize(serialization_type="avro-json") == b'{"timestamp": 1577836800000, "source": {"domain": "test", "name": {"string": "test"}}, "title": "test", "body": ["test", "test"], "tags": [{"name": "test1"}, {"name": "test2"}, {"name": "test3"}]}'
    with pytest.raises(IndexError):
        v1.Post.deserialize(v3_post.serialize(serialization_type="avro-json"))
    # FAILURE: PostV1 can't deserialize PostV3

