from typing import Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import ListMetadata, ProbabilityRequest, Request
from zyte_common_items.converters import (
    to_metadata_optional,
    to_probability_request_list_optional,
    url_to_str,
)


@attrs.define(kw_only=True)
class ArticleNavigationMetadata(ListMetadata):
    """Metadata class for :data:`zyte_common_items.ArticleNavigation.metadata`."""


@attrs.define(kw_only=True)
class ArticleNavigation(Item):
    """Represents the navigational aspects of an article listing webpage.

    See :class:`ArticleList`.
    """

    url: str = attrs.field(converter=url_to_str)
    """Main URL from which the data is extracted."""

    categoryName: Optional[str] = None
    """Name of the category/page.

    Format:

    - trimmed (no whitespace at the beginning or the end of the description
      string)
    """

    subCategories: Optional[list[ProbabilityRequest]] = attrs.field(
        default=None,
        converter=to_probability_request_list_optional,
        kw_only=True,  # type: ignore[misc]
    )
    """List of sub-category links ordered by their position in the page."""

    items: Optional[list[ProbabilityRequest]] = attrs.field(
        default=None,
        converter=to_probability_request_list_optional,
        kw_only=True,  # type: ignore[misc]
    )
    """Links to listed items in order of appearance."""

    nextPage: Optional[Request] = None
    """A link to the next page, if available."""

    pageNumber: Optional[int] = None
    """Number of the current page.

    It should only be extracted if the webpage shows a page number.

    It must be 1-based. For example, if the first page of a listing is
    numbered as 0 on the website, it should be extracted as `1` nonetheless.
    """

    metadata: Optional[ArticleNavigationMetadata] = attrs.field(
        default=None,
        converter=to_metadata_optional(ArticleNavigationMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Data extraction process metadata."""
