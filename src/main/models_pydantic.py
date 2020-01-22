from typing import Optional, FrozenSet
from datetime import datetime, timezone

from pydantic import BaseModel, validator


def validate_timestamp(v: datetime) -> datetime:
    if v.tzinfo is None or v.tzinfo != timezone.utc:
        raise ValueError('must be utc timezone')
    return v


class Source(BaseModel):
    domain: str
    name:   Optional[str]


class Tag(BaseModel):
    name: str

    def __hash__(self):
        return self.name.__hash__()


class Post(BaseModel):
    timestamp:  datetime
    source:     Source
    title:      str
    body:       FrozenSet[str]
    tags:       FrozenSet[Tag]

    @validator('timestamp')
    def timestamp_timezone_to_utc(cls, v: datetime):
        return validate_timestamp(v)
