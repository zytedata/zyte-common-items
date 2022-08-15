import attrs
import pytest

from zyte_common_items.util import split_in_unknown_and_known_fields


@attrs.define(auto_attribs=True, slots=True)
class _TestItem:
    k1: int
    k2: int


def test_split_in_unknown_and_known_fields():
    input = dict(k1=1, k2=2, extra=3)
    unknown, known = split_in_unknown_and_known_fields(input, _TestItem)
    item = _TestItem(**known)
    assert attrs.asdict(item) == dict(k1=1, k2=2)
    assert unknown == dict(extra=3)

    unknown, known = split_in_unknown_and_known_fields(known, _TestItem)
    assert unknown == {}

    for empty_input in ({}, None):  # type: ignore[var-annotated]
        ret = split_in_unknown_and_known_fields(empty_input, _TestItem)
        assert ret == ({}, {})

    with pytest.raises(ValueError):
        split_in_unknown_and_known_fields(input, str)
