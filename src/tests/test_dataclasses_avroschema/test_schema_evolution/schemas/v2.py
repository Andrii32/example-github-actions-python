from typing import Optional, FrozenSet, List
from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_avroschema import AvroModel, types

from .common import Tag, Source, SuperBody


@dataclass(eq=True, frozen=True)
class Post(AvroModel):
    # source field removed
    timestamp:  datetime
    title:      str
    body:       List[str]
