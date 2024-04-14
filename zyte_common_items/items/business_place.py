from typing import List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    AdditionalProperty,
    Address,
    AggregateRating,
    Amenity,
    Image,
    Metadata,
    NamedLink,
    OpeningHoursItem,
    ParentPlace,
    StarRating,
)
from zyte_common_items.converters import to_metadata_optional, url_to_str_optional


@attrs.define(kw_only=True)
class BusinessPlaceMetadata(Metadata):
    """Metadata class for :data:`zyte_common_items.BusinessPlace.metadata`."""


@attrs.define(slots=True, kw_only=True)
class BusinessPlace(Item):
    """Business place, with properties typically seen on maps or business
    listings.

    :attr:`url` is the only required attribute.
    """

    #: Unique identifier of the place on the website.
    placeId: Optional[str] = None

    #: The main URL that the place data was extracted from.
    #:
    #: The URL of the final response, after any redirects.
    #:
    #: In case there is no product data on the page or the page was not reached, the returned "empty"
    #: item would still contain url field and metadata field with dateDownloaded.
    url: Optional[str] = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )

    #: The name of the place.
    name: Optional[str] = None

    #: List of actions that can be performed directly from the URLs on the place page, including URLs.
    actions: Optional[List[NamedLink]] = None

    #: List of name-value pais of any unmapped additional properties specific to the place.
    additionalProperties: Optional[List[AdditionalProperty]] = None

    #: The address details of the place.
    address: Optional[Address] = None

    #: The details of the reservation action,
    #: e.g. table reservation in case of restaurants
    #: or room reservation in case of hotels.
    reservationAction: Optional[NamedLink] = None

    #: List of categories the place belongs to.
    categories: Optional[List[str]] = None

    #: The description of the place.
    #:
    #: Stripped of white spaces.
    description: Optional[str] = None

    #: List of frequently mentioned features of this place.
    features: Optional[List[str]] = None

    #: URL to a map of the place.
    map: Optional[str] = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )

    #: A list of URL values of all images of the place.
    images: Optional[List[Image]] = None

    #: List of amenities of the place.
    amenityFeatures: Optional[List[Amenity]] = None

    #: The overall rating, based on a collection of reviews or ratings.
    aggregateRating: Optional[AggregateRating] = None

    #: Official star rating of the place.
    starRating: Optional[StarRating] = None

    #: If the place is located inside another place, these are the details of the parent place.
    containedInPlace: Optional[ParentPlace] = None

    #: Ordered specification of opening hours, including data for opening and closing time for each day of the week.
    openingHours: Optional[List[OpeningHoursItem]] = None

    #: List of partner review sites.
    reviewSites: Optional[List[NamedLink]] = None

    #: The phone number associated with the place, as it appears on the page.
    telephone: Optional[str] = None

    #: How is the price range of the place viewed by its customers (from z to zzzz).
    priceRange: Optional[str] = None

    #: Which timezone is the place situated in.
    #:
    #: Standard: Name compliant with IANA tz database (tzdata).
    timezone: Optional[str] = None

    #: If the information is verified by the owner of this place.
    isVerified: Optional[bool] = None

    #: The URL pointing to the official website of the place.
    website: Optional[str] = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )

    #:  List of the tags associated with the place.
    tags: Optional[List[str]] = None

    #: Data extraction process metadata.
    metadata: Optional[BusinessPlaceMetadata] = attrs.field(
        default=None, converter=to_metadata_optional(BusinessPlaceMetadata), kw_only=True  # type: ignore[misc]
    )
