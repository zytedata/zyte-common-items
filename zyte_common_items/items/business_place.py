import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    AdditionalProperty,
    Address,
    AggregateRating,
    Amenity,
    Image,
    NamedLink,
    OpeningHoursItem,
    ParentPlace,
    SearchMetadata,
    StarRating,
)
from zyte_common_items.converters import to_metadata_optional, url_to_str_optional


@attrs.define(kw_only=True)
class BusinessPlaceMetadata(SearchMetadata):
    """Metadata class for :data:`zyte_common_items.BusinessPlace.metadata`."""


@attrs.define(slots=True, kw_only=True)
class BusinessPlace(Item):
    """Business place, with properties typically seen on maps or business
    listings.

    :attr:`url` is the only required attribute.
    """

    placeId: str | None = None
    """Unique identifier of the place on the website."""

    url: str | None = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
    """The main URL that the place data was extracted from.

    The URL of the final response, after any redirects.

    In case there is no product data on the page or the page was not reached,
    the returned "empty" item would still contain url field and metadata field
    with dateDownloaded.
    """

    name: str | None = None
    """The name of the place."""

    actions: list[NamedLink] | None = None
    """List of actions that can be performed directly from the URLs on the
    place page, including URLs."""

    additionalProperties: list[AdditionalProperty] | None = None
    """List of name-value pais of any unmapped additional properties specific
    to the place."""

    address: Address | None = None
    """The address details of the place."""

    reservationAction: NamedLink | None = None
    """The details of the reservation action, e.g. table reservation in case of
    restaurants or room reservation in case of hotels."""

    categories: list[str] | None = None
    """List of categories the place belongs to."""

    description: str | None = None
    """The description of the place.

    Stripped of white spaces.
    """

    features: list[str] | None = None
    """List of frequently mentioned features of this place."""

    map: str | None = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
    """URL to a map of the place."""

    images: list[Image] | None = None
    """A list of URL values of all images of the place."""

    amenityFeatures: list[Amenity] | None = None
    """List of amenities of the place."""

    aggregateRating: AggregateRating | None = None
    """The overall rating, based on a collection of reviews or ratings."""

    starRating: StarRating | None = None
    """Official star rating of the place."""

    containedInPlace: ParentPlace | None = None
    """If the place is located inside another place, these are the details of
    the parent place."""

    openingHours: list[OpeningHoursItem] | None = None
    """Ordered specification of opening hours, including data for opening and
    closing time for each day of the week."""

    reviewSites: list[NamedLink] | None = None
    """List of partner review sites."""

    telephone: str | None = None
    """The phone number associated with the place, as it appears on the page.
    """

    priceRange: str | None = None
    """How is the price range of the place viewed by its customers (from z to
    zzzz)."""

    timezone: str | None = None
    """Which timezone is the place situated in.

    Standard: Name compliant with IANA tz database (tzdata).
    """

    isVerified: bool | None = None
    """If the information is verified by the owner of this place."""

    website: str | None = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
    """The URL pointing to the official website of the place."""

    tags: list[str] | None = None
    """List of the tags associated with the place."""

    metadata: BusinessPlaceMetadata | None = attrs.field(
        default=None,
        converter=to_metadata_optional(BusinessPlaceMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Data extraction process metadata."""
