import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import ListMetadata
from zyte_common_items.converters import to_metadata_optional, url_to_str_optional


@attrs.define(kw_only=True)
class SerpOrganicResult(Item):
    """Data from a non-paid result of a search engine results page."""

    description: str | None = None
    """Result excerpt."""

    name: str | None = None
    """Result title."""

    url: str | None = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
    """Result URL."""

    rank: int | None = None
    """Result position among other organic results from the same search engine
    results page.

    This is the rank within a specific page, not within an entire search.
    That is, the first result of any page, even if it not the first page of a
    search, must be 1.
    """

    displayedUrlText: str | None = None
    """Text displayed to represent :attr:`url`.

    It may not be an actual URL, but some stylized or simplified
    representation of it. For example, if :attr:`url` is
    https://en.wikipedia.org/wiki/Foobar, :attr:`displayedUrlText` could be
    something like ``"https://en.wikipedia.org  › wiki › Foobar"``.
    """


@attrs.define(kw_only=True)
class SerpMetadata(ListMetadata):
    """Metadata class for :data:`zyte_common_items.Serp.metadata`."""

    displayedQuery: str | None = None
    """Search query as seen in the webpage."""

    searchedQuery: str | None = None
    """Search query as specified in the input URL."""

    totalOrganicResults: int | None = None
    """Total number of organic results reported by the search engine."""


@attrs.define(kw_only=True)
class Serp(Item):
    """Data from a `search engine results page
    <https://en.wikipedia.org/wiki/Search_engine_results_page>`_."""

    organicResults: list[SerpOrganicResult] | None = None
    """List of search results excluding paid results."""

    url: str = attrs.field(converter=url_to_str_optional)
    """Search URL."""

    pageNumber: int | None = None
    """Page number."""

    metadata: SerpMetadata | None = attrs.field(
        default=None,
        converter=to_metadata_optional(SerpMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Contains metadata about the data extraction process."""
