from typing import List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    Breadcrumb,
    DetailsMetadata,
    NamedLink,
    Request,
)
from zyte_common_items.converters import to_metadata_optional, url_to_str_optional


@attrs.define(kw_only=True)
class PageContentMetadata(DetailsMetadata):
    """Metadata class for :data:`zyte_common_items.PageContent.metadata`."""


@attrs.define(kw_only=True)
class PageContent(Item):
    """Main content and navigation elements of a webpage of any type.

    :attr:`url` is the only required attribute.
    """

    url: str = attrs.field(converter=url_to_str_optional)
    """URL of the page."""

    canonicalUrl: Optional[str] = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
    """Canonical URL of the page, if available."""

    headline: Optional[str] = None
    """Page headline."""

    title: Optional[str] = None
    """Page title, from its ``<title>`` tag."""

    itemMain: Optional[str] = None
    """Text of the primary content of the page, without navigation elements
    (headers, footers, sidebars or pagination links)."""

    itemMainXPath: Optional[str] = None
    """XPath 1.0 expression pointing to the smallest HTML element that contains
    all of :attr:`itemMain`.

    It may only work with an HTML5-compliant parser.
    """

    breadcrumbs: Optional[List[Breadcrumb]] = None
    """Webpage `breadcrumb trail`_.

    .. _Breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    """

    navigationHeader: Optional[List[NamedLink]] = None
    """Navigation items from the header, typically for site-wide navigation."""

    navigationFooter: Optional[List[NamedLink]] = None
    """Navigation items from the footer, typically for site-wide navigation."""

    navigationSidebar: Optional[List[NamedLink]] = None
    """Navigation items from the sidebars, typically for site-wide
    navigation."""

    pagination: Optional[List[NamedLink]] = None
    """Pagination items, either relative to the current page (e.g. current,
    next, previous) or absolute (e.g. first, last, specific page number)."""

    nextPage: Optional[Request] = None
    """A link to the next page, if available."""

    metadata: Optional[PageContentMetadata] = attrs.field(
        default=None,
        converter=to_metadata_optional(PageContentMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Data extraction process metadata."""
