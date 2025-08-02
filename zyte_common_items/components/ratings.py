from typing import Optional

import attrs

from zyte_common_items.base import Item


@attrs.define(kw_only=True)
class AggregateRating(Item):
    """Aggregate data about reviews and ratings.

    At least one of :attr:`ratingValue` or :attr:`reviewCount` is required.

    See :attr:`Product.aggregateRating
    <zyte_common_items.Product.aggregateRating>`.
    """

    bestRating: Optional[float] = None
    """Maximum value of the rating system."""

    ratingValue: Optional[float] = None
    """Average value of all ratings."""

    reviewCount: Optional[int] = None
    """Review count."""


@attrs.define(kw_only=True)
class StarRating(Item):
    """Official star rating of a place."""

    raw: Optional[str] = None
    """Star rating of the place, as it appears on the page, without processing.
    """

    ratingValue: Optional[float] = None
    """Star rating value of the place."""
