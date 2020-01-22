import json
import pytest

from src.main.models_pydantic import Source


"""pydantic does excludes nulls if exclude_none parameter is true """


@pytest.mark.parametrize(
    'input, output, exclude_none',
    [
        (Source(domain="test", name="test"), {"domain": "test", "name": "test"}, True),
        (Source(domain="test", name=None),   {"domain": "test"},                 True),
        (Source(domain="test", name="test"), {"domain": "test", "name": "test"}, False),
        (Source(domain="test", name=None),   {"domain": "test", "name": None},   False),
    ]
)
def test_json_exclude_none(input, output, exclude_none):
    assert input.json(exclude_none=exclude_none) == json.dumps(output)


@pytest.mark.parametrize(
    'input, output',
    [
        ({"domain": "test", "name": "test"}, Source(domain="test", name="test")),
        ({"domain": "test"},                 Source(domain="test", name=None)),
    ]
)
def test_source_parse_raw(input, output):
    assert Source.parse_raw(json.dumps(input)) == output
