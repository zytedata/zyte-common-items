from datetime import datetime
from typing import Optional, TypeVar

import attrs

from zyte_common_items import Item
from zyte_common_items._dateutils import parse_iso_datetime
from zyte_common_items.util import convert_to_class

MetadataT = TypeVar("MetadataT", bound="BaseMetadata")
""":class:`~typing.TypeVar` for :class:`BaseMetadata`."""


class BaseMetadata(Item):
    """Base metadata class"""

    def cast(self, cls: type[MetadataT]) -> MetadataT:
        """Convert *value*, a metadata instance, into a different metadata *cls*."""
        return convert_to_class(self, cls)


@attrs.define(kw_only=True)
class ProbabilityMetadata(BaseMetadata):
    """Data extraction process metadata."""

    probability: Optional[float] = 1.0
    """The probability (0 for 0%, 1 for 100%) that the resource features the
    expected data type.

    For example, if the extraction of a product from a given URL is requested,
    and that URL points to the webpage of a product with complete certainty,
    the value should be `1`. If with complete certainty the webpage features a
    job listing instead of a product, the value should be `0`. When there is no
    complete certainty, the value could be anything in between (e.g. `0.96`).
    """


@attrs.define(kw_only=True)
class ListMetadata(BaseMetadata):
    """Minimal metadata for list item classes, such as ProductList or ArticleList.

    See
    :class:`ArticleList.metadata <zyte_common_items.ArticleList.metadata>`.
    """

    dateDownloaded: Optional[str] = None
    """Date and time when the product data was downloaded, in UTC timezone and
    the following format: ``YYYY-MM-DDThh:mm:ssZ``."""

    validationMessages: Optional[dict[str, list[str]]] = None
    """Contains paths to fields with the description of issues found with their
    values."""

    def get_date_downloaded_parsed(self) -> Optional[datetime]:
        """Return dateDownloaded as a TZ-aware datetime object"""
        if self.dateDownloaded is None:
            return None
        return parse_iso_datetime(self.dateDownloaded)


@attrs.define(kw_only=True)
class DetailsMetadata(ListMetadata):
    """Minimal metadata for details item classes, such as Product or Article."""

    probability: Optional[float] = 1.0
    """The probability (0 for 0%, 1 for 100%) that the resource features the
    expected data type.

    For example, if the extraction of a product from a given URL is requested,
    and that URL points to the webpage of a product with complete certainty,
    the value should be `1`. If with complete certainty the webpage features a
    job listing instead of a product, the value should be `0`. When there is no
    complete certainty, the value could be anything in between (e.g. `0.96`).
    """


@attrs.define(kw_only=True)
class SearchMetadata(DetailsMetadata):
    """Minimal metadata for classes of items that can declare search
    metadata."""

    searchText: Optional[str] = None
    """The search text used to find the item."""


@attrs.define(kw_only=True)
class Metadata(SearchMetadata):
    """Generic metadata class.

    It defines all attributes of metadata classes for specific item types, so
    that it can be used during extraction instead of a more specific class, and
    later converted to the corresponding, more specific metadata class.
    """

    displayedQuery: Optional[str] = None
    """Search query as seen in the webpage."""

    searchedQuery: Optional[str] = None
    """Search query as specified in the input URL."""

    totalOrganicResults: Optional[int] = None
    """Total number of organic results reported by the search engine."""
