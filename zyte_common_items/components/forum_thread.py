from __future__ import annotations

import attrs

from zyte_common_items.base import Item


@attrs.define(kw_only=True)
class Topic(Item):
    """Topic that is discussed on the page."""

    #: Name of the topic.
    name: str
