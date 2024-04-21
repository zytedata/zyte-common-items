from typing import Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.util import url_to_str


@attrs.define(kw_only=True)
class Breadcrumb(Item):
    """A breadcrumb from the `breadcrumb trail`_ of a webpage.

    See :attr:`Product.breadcrumbs
    <zyte_common_items.Product.breadcrumbs>`.

    .. _breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    """

    #: Displayed name.
    name: Optional[str] = None

    #: Target URL.
    url: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )
