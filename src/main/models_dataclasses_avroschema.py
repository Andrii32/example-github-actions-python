from typing import Optional, FrozenSet
from datetime import datetime, timezone

from dataclasses import dataclass, field
from dataclasses_avroschema import AvroModel, types
from marshmallow import fields


@dataclass(eq=True, frozen=True)
class Source(AvroModel):
    domain: str
    name:   Optional[str]


@dataclass(eq=True, frozen=True)
class Tag(AvroModel):
    name: str


@dataclass(eq=True, frozen=True)
class DateField(AvroModel):
    value:  datetime


@dataclass(eq=True, frozen=True)
class Post(AvroModel):
    timestamp:  datetime
    source:     Source
    title:      str
    body:       FrozenSet[str]
    tags:       FrozenSet[Tag]

    def __post_init__(self):
        validate_timestamp(self.timestamp)


@dataclass(eq=True, frozen=True)
class FrozenSetTag(AvroModel):
    values: FrozenSet[Tag]


@dataclass(eq=True, frozen=True)
class FrozenSetPost(AvroModel):
    values: FrozenSet[Post]


@dataclass(eq=True, frozen=True)
class FrozenSetTagImproved(AvroModel):
    values: FrozenSet[Tag]


@dataclass(eq=True, frozen=True)
class FrozenSetPostImproved(AvroModel):
    values: FrozenSet[Post]
