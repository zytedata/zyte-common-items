import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    AdditionalProperty,
    Address,
    Breadcrumb,
    DetailsMetadata,
    Image,
    RealEstateArea,
)
from zyte_common_items.converters import to_metadata_optional, url_to_str_optional


@attrs.define(kw_only=True)
class RealEstateMetadata(DetailsMetadata):
    """Metadata class for :data:`zyte_common_items.RealEstate.metadata`."""


@attrs.define(slots=True, kw_only=True)
class RealEstate(Item):
    """Real state offer, typically seen on real estate offer aggregator
    websites.

    :attr:`url` is the only required attribute.
    """

    url: str = attrs.field(converter=url_to_str_optional)
    """The url of the final response, after any redirects."""

    breadcrumbs: list[Breadcrumb] | None = None
    """Webpage `breadcrumb trail`_.

    .. _Breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    """

    realEstateId: str | None = None
    """The identifier of the real estate, usually assigned by the seller and
    unique within a website, similar to product SKU."""

    name: str | None = None
    """The name of the real estate."""

    datePublished: str | None = None
    """Publication date of the real estate offer.

    Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"

    With timezone, if available.
    """

    datePublishedRaw: str | None = None
    """Same date as datePublished, but before parsing/normalization, i.e. as it
    appears on the website."""

    description: str | None = None
    """The description of the real estate.

    Format:

    - trimmed (no whitespace at the beginning or the end of the description
      string),
    - line breaks included,
    - no length limit,
    - no normalization of Unicode characters,
    - no concatenation of description from different parts of the page.
    """

    mainImage: Image | None = None
    """The details of the main image of the real estate."""

    images: list[Image] | None = None
    """A list of URL values of all images of the real estate."""

    address: Address | None = None
    """The details of the address of the real estate."""

    area: RealEstateArea | None = None
    """Real estate area details."""

    numberOfBathroomsTotal: int | None = None
    """The total number of bathrooms in the real estate."""

    numberOfFullBathrooms: int | None = None
    """The number of full bathrooms in the real estate."""

    numberOfPartialBathrooms: int | None = None
    """The number of partial bathrooms in the real estate."""

    numberOfBedrooms: int | None = None
    """The number of bedrooms in the real estate."""

    numberOfRooms: int | None = None
    """The number of rooms (excluding bathrooms and closets) of the real
    estate."""

    tradeType: str | None = None
    """Type of a trade action: buying or renting."""

    price: str | None = None
    """The offer price of the real estate."""

    rentalPeriod: str | None = None
    """The rental period to which the rental price applies, only available in
    case of rental. Usually weekly, monthly, quarterly, yearly."""

    currencyRaw: str | None = None
    """Currency associated with the price, as appears on the page (no
    post-processing)."""

    currency: str | None = None
    """The currency of the price, in 3-letter ISO 4217 format."""

    additionalProperties: list[AdditionalProperty] | None = None
    """A name-value pair field holding information pertaining to specific
    features. Usually in a form of a specification table or freeform
    specification list."""

    propertyType: str | None = None
    """Type of the property, e.g. flat, house, land."""

    yearBuilt: int | None = None
    """The year the real estate was built."""

    virtualTourUrl: str | None = None
    """The URL of the virtual tour of the real estate."""

    metadata: RealEstateMetadata | None = attrs.field(
        default=None,
        converter=to_metadata_optional(RealEstateMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Contains metadata about the data extraction process."""
