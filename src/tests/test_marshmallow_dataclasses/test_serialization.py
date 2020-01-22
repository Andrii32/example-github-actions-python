import pytest

import marshmallow_dataclass

from src.main.models_marshmallow_dataclasses import Post


"""
marshmallow-dataclasses can't create a schema for dataclass with set,frozenset objects
"""


def test_create_schema():
    with pytest.raises(TypeError):
        marshmallow_dataclass.class_schema(Post)
