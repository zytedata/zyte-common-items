import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import Breadcrumb, DetailsMetadata, NamedLink, Request
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

    canonicalUrl: str | None = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
    """Canonical URL of the page, if available."""

    headline: str | None = None
    """Page headline."""

    title: str | None = None
    """Page title, from its ``<title>`` tag."""

    itemMain: str | None = None
    """Text of the primary content of the page, without navigation elements
    (headers, footers, sidebars or pagination links)."""

    itemMainXPath: str | None = None
    """XPath 1.0 expression pointing to the smallest HTML element that contains
    all of :attr:`itemMain`.

    It may only work with an HTML5-compliant parser.
    """

    breadcrumbs: list[Breadcrumb] | None = None
    """Webpage `breadcrumb trail`_.

    .. _Breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    """

    navigationHeader: list[NamedLink] | None = None
    """Navigation items from the header, typically for site-wide navigation."""

    navigationFooter: list[NamedLink] | None = None
    """Navigation items from the footer, typically for site-wide navigation."""

    navigationSidebar: list[NamedLink] | None = None
    """Navigation items from the sidebars, typically for site-wide
    navigation."""

    pagination: list[NamedLink] | None = None
    """Pagination items, either relative to the current page (e.g. current,
    next, previous) or absolute (e.g. first, last, specific page number)."""

    nextPage: Request | None = None
    """A link to the next page, if available."""

    metadata: PageContentMetadata | None = attrs.field(
        default=None,
        converter=to_metadata_optional(PageContentMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Data extraction process metadata."""
