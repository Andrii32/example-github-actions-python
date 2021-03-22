from typing import Optional, FrozenSet, List
from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_avroschema import AvroModel, types

from .common import Tag, Source, SuperBody


@dataclass(eq=True, frozen=True)
class Post(AvroModel):
    # tags field added
    timestamp:  datetime
    source:     Source
    title:      str
    body:       List[str]
    tags:       List[Tag]
