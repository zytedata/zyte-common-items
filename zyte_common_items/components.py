"""Classes for data nested within items."""

from typing import Optional

import attrs

from zyte_common_items.base import Item


@attrs.define(slots=True)
class AdditionalProperty(Item):
    name: str
    value: str


@attrs.define(slots=True, kw_only=True)
class AggregateRating(Item):
    bestRating: Optional[float] = None
    ratingValue: Optional[float] = None
    reviewCount: Optional[int] = None


@attrs.define(slots=True)
class Brand(Item):
    name: str


@attrs.define(slots=True, kw_only=True)
class Breadcrumb(Item):
    name: Optional[str] = None
    url: Optional[str] = None


@attrs.define(slots=True)
class Gtin(Item):
    type: str
    value: str


@attrs.define(slots=True)
class Image(Item):
    url: Optional[str]


@attrs.define(slots=True, kw_only=True)
class Metadata(Item):
    dateDownloaded: Optional[str] = None
    probability: Optional[float] = None
