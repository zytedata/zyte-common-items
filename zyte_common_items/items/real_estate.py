from typing import List, Optional

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
from zyte_common_items.converters import to_metadata_optional, url_to_str


@attrs.define(kw_only=True)
class RealEstateMetadata(DetailsMetadata):
    """Metadata class for :data:`zyte_common_items.RealEstate.metadata`."""


@attrs.define(slots=True, kw_only=True)
class RealEstate(Item):
    """Real state offer, typically seen on real estate offer aggregator
    websites.

    :attr:`url` is the only required attribute.
    """

    #: The url of the final response, after any redirects.
    url: str = attrs.field(converter=url_to_str)

    #: Webpage `breadcrumb trail`_.
    #:
    #: .. _Breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    breadcrumbs: Optional[List[Breadcrumb]] = None

    #: The identifier of the real estate, usually assigned by the seller and unique within a website, similar to product SKU.
    realEstateId: Optional[str] = None

    #: The name of the real estate.
    name: Optional[str] = None

    #: Publication date of the real estate offer.
    #:
    #: Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"
    #:
    #: With timezone, if available.
    datePublished: Optional[str] = None

    #: Same date as datePublished, but before parsing/normalization, i.e. as it appears on the website.
    datePublishedRaw: Optional[str] = None

    #: The description of the real estate.
    #:
    #: Format:
    #:
    #: - trimmed (no whitespace at the beginning or the end of the description string),
    #:
    #: - line breaks included,
    #:
    #: - no length limit,
    #:
    #: - no normalization of Unicode characters,
    #:
    #: - no concatenation of description from different parts of the page.
    description: Optional[str] = None

    #: The details of the main image of the real estate.
    mainImage: Optional[Image] = None

    #: A list of URL values of all images of the real estate.
    images: Optional[List[Image]] = None

    #: The details of the address of the real estate.
    address: Optional[Address] = None

    #: Real estate area details.
    area: Optional[RealEstateArea] = None

    #: The total number of bathrooms in the real estate.
    numberOfBathroomsTotal: Optional[int] = None

    #: The number of full bathrooms in the real estate.
    numberOfFullBathrooms: Optional[int] = None

    #: The number of partial bathrooms in the real estate.
    numberOfPartialBathrooms: Optional[int] = None

    #: The number of bedrooms in the real estate.
    numberOfBedrooms: Optional[int] = None

    #: The number of rooms (excluding bathrooms and closets) of the real estate.
    numberOfRooms: Optional[int] = None

    #: Type of a trade action: buying or renting.
    tradeType: Optional[str] = None

    #: The offer price of the real estate.
    price: Optional[str] = None

    #: The rental period to which the rental price applies, only available in case of rental. Usually weekly, monthly, quarterly, yearly.
    rentalPeriod: Optional[str] = None

    #: Currency associated with the price, as appears on the page (no post-processing).
    currencyRaw: Optional[str] = None

    #: The currency of the price, in 3-letter ISO 4217 format.
    currency: Optional[str] = None

    #: A name-value pair field holding information pertaining to specific features. Usually in a form of a specification table or freeform specification list.
    additionalProperties: Optional[List[AdditionalProperty]] = None

    #: Type of the property, e.g. flat, house, land.
    propertyType: Optional[str] = None

    #: The year the real estate was built.
    yearBuilt: Optional[int] = None

    #: The URL of the virtual tour of the real estate.
    virtualTourUrl: Optional[str] = None

    #: Contains metadata about the data extraction process.
    metadata: Optional[RealEstateMetadata] = attrs.field(
        default=None, converter=to_metadata_optional(RealEstateMetadata), kw_only=True  # type: ignore[misc]
    )
