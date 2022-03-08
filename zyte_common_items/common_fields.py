"""
Contains the shared field definitions for the top-level items for:
    * Zyte Data API Schema
    * Unified Schema
"""

from typing import Optional

import attr

from zyte_common_items import Item
from zyte_common_items.util import export


@export
@attr.define(slots=True)
class Author(Item):
    name: str
    raw: Optional[str] = None


@export
@attr.define(slots=True)
class Breadcrumb(Item):
    name: Optional[str] = None
    link: Optional[str] = None


@export
@attr.define(slots=True)
class Image(Item):
    url: str


@export
@attr.define(slots=True)
class Media(Item):
    url: str


@export
@attr.define(slots=True)
class PaginationLink(Item):
    url: str
    text: Optional[str] = None


@export
@attr.define(slots=True)
class Offer(Item):
    price: Optional[str] = None
    currency: Optional[str] = None
    regularPrice: Optional[str] = None
    availability: Optional[str] = None  # TODO handle allowed values


@export
@attr.define(slots=True)
class GTIN(Item):
    type: str  # TODO: handle allowed values
    value: str


@export
@attr.define(slots=True)
class Brand(Item):
    name: str


@export
@attr.define(slots=True)
class Rating(Item):
    ratingValue: Optional[float] = None
    bestRating: Optional[float] = None
    reviewCount: Optional[int] = None


@export
@attr.define(slots=True)
class AdditionalProperty(Item):
    name: str
    value: Optional[str] = None


@export
@attr.define(slots=True)
class Topic(Item):
    name: str


@export
@attr.define(slots=True)
class Location(Item):
    raw: str


@export
@attr.define(slots=True)
class VehicleEngine(Item):
    raw: str


@export
@attr.define(slots=True)
class AvailableAtOrFrom(Item):
    raw: str


@export
@attr.define(slots=True)
class FuelEfficiency(Item):
    raw: str


@export
@attr.define(slots=True)
class Salary(Item):
    raw: Optional[str] = None
    value: Optional[float] = None
    currency: Optional[str] = None


@export
@attr.define(slots=True)
class Address(Item):
    postalCode: Optional[str] = None
    streetAddress: Optional[str] = None
    addressCountry: Optional[str] = None
    addressLocality: Optional[str] = None
    addressRegion: Optional[str] = None
    raw: Optional[str] = None


@export
@attr.define(slots=True)
class Area(Item):
    raw: str
    value: Optional[float]
    unitCode: Optional[str]  # SQMT, SQFT, ACRE


@export
@attr.define(slots=True)
class TradeAction(Item):
    tradeType: Optional[str] = None
    price: Optional[str] = None
    currency: Optional[str] = None


@export
@attr.define(slots=True)
class MileageFromOdometer(Item):
    value: Optional[int] = None
    unitCode: Optional[str] = None
