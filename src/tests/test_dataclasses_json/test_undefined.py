import pytest


from src.main.models_dataclasses_json import Tag


def test_undefined_field_on_initialization():
    with pytest.raises(TypeError):
        Tag(name="test", no_field="test")


def test_undefined_field_on_deserialization():
    with pytest.raises(TypeError):
        Tag.from_json({"name": "test", "no_field": "test"})
