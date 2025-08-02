from typing import List, Optional

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

    description: Optional[str] = None
    """Result excerpt."""

    name: Optional[str] = None
    """Result title."""

    url: Optional[str] = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
    """Result URL."""

    rank: Optional[int] = None
    """Result position among other organic results from the same search engine
    results page.

    This is the rank within a specific page, not within an entire search.
    That is, the first result of any page, even if it not the first page of a
    search, must be 1.
    """

    displayedUrlText: Optional[str] = None
    """Text displayed to represent :attr:`url`.

    It may not be an actual URL, but some stylized or simplified
    representation of it. For example, if :attr:`url` is
    https://en.wikipedia.org/wiki/Foobar, :attr:`displayedUrlText` could be
    something like ``"https://en.wikipedia.org  › wiki › Foobar"``.
    """


@attrs.define(kw_only=True)
class SerpMetadata(ListMetadata):
    """Metadata class for :data:`zyte_common_items.Serp.metadata`."""

    displayedQuery: Optional[str] = None
    """Search query as seen in the webpage."""

    searchedQuery: Optional[str] = None
    """Search query as specified in the input URL."""

    totalOrganicResults: Optional[int] = None
    """Total number of organic results reported by the search engine."""


@attrs.define(kw_only=True)
class Serp(Item):
    """Data from a `search engine results page
    <https://en.wikipedia.org/wiki/Search_engine_results_page>`_."""

    organicResults: Optional[List[SerpOrganicResult]] = None
    """List of search results excluding paid results."""

    url: str = attrs.field(converter=url_to_str)
    """Search URL."""

    pageNumber: Optional[int] = None
    """Page number."""

    metadata: Optional[SerpMetadata] = attrs.field(
        default=None,
        converter=to_metadata_optional(SerpMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Contains metadata about the data extraction process."""
