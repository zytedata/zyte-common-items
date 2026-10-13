import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import ListMetadata
from zyte_common_items.converters import (
    to_metadata_optional,
    url_to_str,
    url_to_str_optional,
)


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
class SerpAiOverviewReference(Item):
    """Source cited by the AI overview of a search engine results page."""

    url: str = attrs.field(converter=url_to_str)
    """URL of the cited page.

    It may be a redirect URL of the search engine rather than the URL of the
    cited page itself.
    """

    source: str | None = None
    """Human-readable name of the source, e.g. the publisher name."""

    domain: str | None = None
    """Bare domain of the cited page, e.g. ``"en.wikipedia.org"``.

    It is missing if :attr:`url` is a redirect URL that does not reveal the
    cited page.
    """

    title: str | None = None
    """Title of the cited page."""

    text: str | None = None
    """Text excerpt from the cited page."""


@attrs.define(kw_only=True)
class SerpAiOverview(Item):
    """AI-generated answer shown on a search engine results page."""

    text: str
    """Plain-text rendering of the AI overview."""

    markdown: str | None = None
    """Markdown rendering of the AI overview.

    Citations are inline markers like ``[[1]](https://example.com)``, where the
    number is the 1-based index of the citation in :attr:`references` and the
    URL is its :attr:`~SerpAiOverviewReference.url`.
    """

    references: list[SerpAiOverviewReference] | None = None
    """Sources cited by the AI overview."""


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

    aiOverview: SerpAiOverview | None = None
    """AI-generated answer to the search query.

    It is missing if the search engine results page does not show one.
    """
