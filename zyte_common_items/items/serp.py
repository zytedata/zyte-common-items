from typing import List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import ListMetadata, SerpOrganicResult
from zyte_common_items.converters import to_metadata_optional


@attrs.define(kw_only=True)
class SerpMetadata(ListMetadata):
    """Metadata class for :data:`zyte_common_items.Serp.metadata`."""

    #: Search query as seen in the webpage.
    displayedQuery: Optional[str] = None

    #: Search query as specified in the input URL.
    searchedQuery: Optional[str] = None

    #: Total number of organic results reported by the search engine.
    totalOrganicResults: Optional[int] = None


@attrs.define(kw_only=True)
class Serp(Item):
    """Data from a `search engine results page
    <https://en.wikipedia.org/wiki/Search_engine_results_page>`_."""

    #: List of search results excluding paid results.
    organicResults: Optional[List[SerpOrganicResult]] = None

    #: Search URL.
    url: str

    #: Page number.
    pageNumber: Optional[int] = None

    #: Contains metadata about the data extraction process.
    metadata: Optional[SerpMetadata] = attrs.field(
        default=None, converter=to_metadata_optional(SerpMetadata), kw_only=True  # type: ignore[misc]
    )
