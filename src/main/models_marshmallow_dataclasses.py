from typing import Optional, FrozenSet
from dataclasses import dataclass, field
from datetime import datetime, timezone

import marshmallow_dataclass
from marshmallow.exceptions import ValidationError


def validate_timestamp(v: datetime) -> datetime:
    if v.tzinfo is None or v.tzinfo != timezone.utc:
        raise ValidationError('must be utc timezone')
    return v


@dataclass(frozen=True)
class Source:
    domain: str
    name:   Optional[str]


SourceSchema = marshmallow_dataclass.class_schema(Source)


@dataclass(frozen=True)
class Tag:
    name: str


TagSchema = marshmallow_dataclass.class_schema(Tag)


@dataclass(frozen=True)
class Post:
    timestamp:  datetime = field(metadata={"validate": validate_timestamp})
    source:     Source
    title:      str
    body:       FrozenSet[str]
    tags:       FrozenSet[Tag]
