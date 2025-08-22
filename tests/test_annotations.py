from typing import get_type_hints

import pytest

import zyte_common_items

EXPORTED = [
    getattr(zyte_common_items, t)
    for t in dir(zyte_common_items)
    if not t.startswith("_")
]
EXPORTED_TYPES = [t for t in EXPORTED if isinstance(t, type)]


@pytest.mark.parametrize("t", EXPORTED_TYPES)
def test_get_type_hints(t: type) -> None:
    """Test that get_type_hints() works for all exported types."""
    get_type_hints(t)
