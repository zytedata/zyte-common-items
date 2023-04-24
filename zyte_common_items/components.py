"""Classes for data nested within items."""
from typing import Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.util import url_to_str


@attrs.define
class AdditionalProperty(Item):
    """A name-value pair.

    See :attr:`Product.additionalProperties
    <zyte_common_items.items.Product.additionalProperties>`.
    """

    #: Name.
    name: str

    #: Value.
    value: str


@attrs.define(kw_only=True)
class AggregateRating(Item):
    """Aggregate data about reviews and ratings.

    At least one of :attr:`ratingValue` or :attr:`reviewCount` is required.

    See :attr:`Product.aggregateRating
    <zyte_common_items.items.Product.aggregateRating>`.
    """

    #: Maximum value of the rating system.
    bestRating: Optional[float] = None

    #: Average value of all ratings.
    ratingValue: Optional[float] = None

    #: Review count.
    reviewCount: Optional[int] = None


@attrs.define
class Brand(Item):
    """Brand.

    See :attr:`Product.brand <zyte_common_items.items.Product.brand`.
    """

    #: Name as it appears on the source webpage (no post-processing).
    name: str


@attrs.define(kw_only=True)
class Breadcrumb(Item):
    """A breadcrumb from the `breadcrumb trail`_ of a webpage.

    See :attr:`Product.breadcrumbs
    <zyte_common_items.items.Product.breadcrumbs>`.

    .. _breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    """

    #: Displayed name.
    name: Optional[str] = None

    #: Target URL.
    url: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )


@attrs.define
class Gtin(Item):
    """GTIN_ type-value pair.

    See :class:`Product.gtin <zyte_common_items.items.Product.gtin>`.

    .. _GTIN: https://en.wikipedia.org/wiki/Global_Trade_Item_Number
    """

    #: Identifier of the GTIN format of ``value``.
    #:
    #: One of: ``"gtin13"``, ``"gtin8"``, ``"gtin14"``, ``"isbn10"``,
    #: ``"isbn13"``, ``"ismn"``, ``"issn"``, ``"upc"``.
    type: str

    #: Value.
    #:
    #: It should only contain digits.
    value: str


@attrs.define
class Image(Item):
    """Image.

    See :class:`Product.images <zyte_common_items.items.Product.images>` and
    :class:`Product.mainImage <zyte_common_items.items.Product.mainImage>`.
    """

    #: URL.
    #:
    #: When multiple URLs exist for a given image, and those URLs point to
    #: image files that are different-quality versions of that image, the URL
    #: of the highest-quality image file should be used.
    #:
    #: `Data URIs`_ are not allowed in this attribute.
    #:
    #: .. _Data URIs: https://en.wikipedia.org/wiki/Data_URI_scheme
    url: str = attrs.field(converter=url_to_str)


@attrs.define(kw_only=True)
class Link(Item):
    """A link from a webpage to another webpage."""

    #: Displayed text.
    text: Optional[str] = None

    #: Target URL.
    url: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )


@attrs.define(kw_only=True)
class NamedLink(Item):
    """A link from a webpage to another webpage."""

    #: The name of the link.
    name: Optional[str] = None

    #: Target URL.
    url: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )


@attrs.define(kw_only=True)
class Metadata(Item):
    """Data extraction process metadata.

    See :class:`Product.metadata <zyte_common_items.items.Product.metadata>`.
    """

    #: Date and time when the product data was downloaded, in UTC timezone and
    #: the following format: ``YYYY-MM-DDThh:mm:ssZ``.
    dateDownloaded: Optional[str] = None

    #: The probability (0 for 0%, 1 for 100%) that the webpage features the
    #: requested data type.
    #:
    #: For example, if the extraction of a product from a given URL is
    #: requested, and that URL points to the webpage of a product with complete
    #: certainty, the value should be `1`. If with complete certainty the
    #: webpage features a job listing instead of a product, the value should be
    #: `0`. When there is no complete certainty, the value could be anything in
    #: between (e.g. `0.96`).
    probability: Optional[float] = None


@attrs.define(kw_only=True)
class BusinessPlaceMetadata(Metadata):
    """Data extraction process metadata.

    See :class:`BusinessPlace.metadata <zyte_common_items.items.BusinessPlace.metadata>`.
    """

    #: The search text the place was found with.
    searchText: Optional[str] = None


@attrs.define(kw_only=True)
class Address(Item):
    """Address item."""

    #: The raw address information, as it appears on the website.
    addressRaw: Optional[str] = None

    #: The street address of the place.
    streetAddress: Optional[str] = None

    #: The city the place is located in.
    addressCity: Optional[str] = None

    #: The locality to which the place belongs.
    addressLocality: Optional[str] = None

    #: The region of the place.
    addressRegion: Optional[str] = None

    #: The country the place is located in.
    #:
    #: The country name or the `ISO 3166-1 alpha-2 country code
    #: <https://en.wikipedia.org/wiki/ISO_3166-1>`__.
    addressCountry: Optional[str] = None

    #: The postal code of the address.
    postalCode: Optional[str] = None

    #: The auxiliary part of the postal code.
    #:
    #: It may include a state abbreviation or town name, depending on local standards.
    postalCodeAux: Optional[str] = None

    #: Geographical latitude of the place.
    latitude: Optional[float] = None

    #: Geographical longitude of the place.
    longitude: Optional[float] = None


@attrs.define(kw_only=True)
class Amenity(Item):
    """An amenity that a business place has"""

    #: Name of amenity.
    name: str

    #: Availability of the amenity.
    value: bool


@attrs.define(kw_only=True)
class StarRating(Item):
    """Official star rating of a place."""

    #: Star rating of the place, as it appears on the page, without processing.
    raw: Optional[str] = None

    #: Star rating value of the place.
    ratingValue: Optional[float] = None


@attrs.define(kw_only=True)
class ParentPlace(Item):
    """If the place is located inside another place, these are the details of the parent place."""

    #: Name of the parent place.
    name: str

    #: Identifier of the parent place.
    placeId: str


@attrs.define(kw_only=True)
class OpeningHoursItem(Item):
    """Specification of opening hours of a business place."""

    #: English weekday name.
    dayOfWeek: Optional[str] = None

    #: Opening time in ISO 8601 format, local time.
    opens: Optional[str] = None

    #: Closing time in ISO 8601 format, local time.
    closes: Optional[str] = None

    #: Day of the week, as it appears on the page, without processing.
    rawDayOfWeek: Optional[str] = None

    #: Opening time, as it appears on the page, without processing.
    rawOpens: Optional[str] = None

    #: Closing time, as it appears on the page, without processing.
    rawCloses: Optional[str] = None


@attrs.define(kw_only=True)
class RealEstateArea(Item):
    """Area of a place, with type, units, value and raw value."""

    #: Area
    value: float

    #: Unit of the value field, one of: SQMT (square meters), SQFT (square
    #: feet), ACRE (acres).
    unitCode: str

    #: Type of area, one of: LOT, FLOOR
    areaType: Optional[str] = None

    #: Area in the raw format, as it appears on the website.
    raw: str
