import attrs
import pytest

from zyte_common_items.processors import metadata_processor as new_metadata_processor
from zyte_common_items.util import metadata_processor, split_in_unknown_and_known_fields


@attrs.define(auto_attribs=True, slots=True)
class _TestItem:
    k1: int
    k2: int


def test_split_in_unknown_and_known_fields():
    input_ = {"k1": 1, "k2": 2, "extra": 3}
    unknown, known = split_in_unknown_and_known_fields(input_, _TestItem)
    item = _TestItem(**known)
    assert attrs.asdict(item) == {"k1": 1, "k2": 2}
    assert unknown == {"extra": 3}

    unknown, known = split_in_unknown_and_known_fields(known, _TestItem)
    assert unknown == {}

    for empty_input in ({}, None):  # type: ignore[var-annotated]
        ret = split_in_unknown_and_known_fields(empty_input, _TestItem)
        assert ret == ({}, {})

    with pytest.raises(ValueError, match="The cls <class 'str'> is not attrs class"):
        split_in_unknown_and_known_fields(input_, str)


def test_deprecated_metadata_processor():
    with pytest.deprecated_call():
        assert metadata_processor(None, None) == new_metadata_processor(None, None)
