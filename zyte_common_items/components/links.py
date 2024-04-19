from typing import Optional

import attrs

from zyte_common_items import Item
from zyte_common_items.util import url_to_str


@attrs.define(kw_only=True)
class Link(Item):
    """A link from a webpage to another webpage."""

    #: Displayed text.
    text: Optional[str] = None

    #: Target URL.
    url: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )


@attrs.define(kw_only=True)
class NamedLink(Item):
    """A link from a webpage to another webpage."""

    #: The name of the link.
    name: Optional[str] = None

    #: Target URL.
    url: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )


@attrs.define(kw_only=True)
class Url(Item):
    """A URL."""

    # : URL.
    url: str = attrs.field(converter=url_to_str)
