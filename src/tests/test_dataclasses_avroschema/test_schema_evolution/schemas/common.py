from typing import Optional, FrozenSet, List
from datetime import datetime, timezone

from dataclasses import dataclass, field
from dataclasses_avroschema import AvroModel, types
import pytest


@dataclass(eq=True, frozen=True)
class Source(AvroModel):
    domain: str
    name:   Optional[str]


@dataclass(eq=True, frozen=True)
class Tag(AvroModel):
    name: str


@dataclass(eq=True, frozen=True)
class SuperBody(AvroModel):
    value: str
    tags:  List[Tag]



