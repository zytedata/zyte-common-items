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

    #: Maximum value of the rating system.
    bestRating: Optional[float] = None

    #: Average value of all ratings.
    ratingValue: Optional[float] = None

    #: Review count.
    reviewCount: Optional[int] = None


@attrs.define(kw_only=True)
class StarRating(Item):
    """Official star rating of a place."""

    #: Star rating of the place, as it appears on the page, without processing.
    raw: Optional[str] = None

    #: Star rating value of the place.
    ratingValue: Optional[float] = None
