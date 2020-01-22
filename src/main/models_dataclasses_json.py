from typing import Optional, FrozenSet
from datetime import datetime, timezone

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from marshmallow import fields


def validate_timestamp(v: datetime) -> datetime:
    if v.tzinfo is None or v.tzinfo != timezone.utc:
        raise ValueError('must be utc timezone')
    return v


@dataclass_json()
@dataclass(eq=True, frozen=True)
class Source:
    domain: str
    name:   Optional[str]


@dataclass_json()
@dataclass(eq=True, frozen=True)
class Tag:
    name: str


@dataclass_json()
@dataclass(eq=True, frozen=True)
class Post:
    timestamp:  datetime = field(
        metadata={
            'dataclasses_json': {
                'encoder': datetime.isoformat,
                'decoder': datetime.fromisoformat,
                'mm_field': fields.DateTime(format='iso')
            }
        }
    )
    source:     Source
    title:      str
    body:       FrozenSet[str]
    tags:       FrozenSet[Tag]

    def __post_init__(self):
        validate_timestamp(self.timestamp)


@dataclass_json()
@dataclass(eq=True, frozen=True)
class FrozenSetPost:
    values: FrozenSet[Post]
