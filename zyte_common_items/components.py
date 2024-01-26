"""Classes for data nested within items."""
import base64
from typing import List, Optional, Type, TypeVar

import attrs

from zyte_common_items.base import Item, ProbabilityMixin
from zyte_common_items.util import convert_to_class, url_to_str

# Metadata ####################################################################


@attrs.define(kw_only=True)
class ProbabilityMetadata(Item):
    """Data extraction process metadata that indicates a probability."""

    #: The probability (0 for 0%, 1 for 100%) that the resource features the
    #: expected data type.
    #:
    #: For example, if the extraction of a product from a given URL is
    #: requested, and that URL points to the webpage of a product with complete
    #: certainty, the value should be `1`. If with complete certainty the
    #: webpage features a job listing instead of a product, the value should be
    #: `0`. When there is no complete certainty, the value could be anything in
    #: between (e.g. `0.96`).
    probability: Optional[float] = 1.0


@attrs.define(kw_only=True)
class _ListMetadata(Item):
    """Data extraction process metadata that indicates the download date.

    See
    :class:`ArticleList.metadata <zyte_common_items.ArticleList.metadata>`.
    """

    #: Date and time when the product data was downloaded, in UTC timezone and
    #: the following format: ``YYYY-MM-DDThh:mm:ssZ``.
    dateDownloaded: Optional[str] = None


@attrs.define(kw_only=True)
class _DetailsMetadata(_ListMetadata):
    """Data extraction process metadata that indicates the download date and a
    probability."""

    #: The probability (0 for 0%, 1 for 100%) that the resource features the
    #: expected data type.
    #:
    #: For example, if the extraction of a product from a given URL is
    #: requested, and that URL points to the webpage of a product with complete
    #: certainty, the value should be `1`. If with complete certainty the
    #: webpage features a job listing instead of a product, the value should be
    #: `0`. When there is no complete certainty, the value could be anything in
    #: between (e.g. `0.96`).
    probability: Optional[float] = 1.0


@attrs.define(kw_only=True)
class Metadata(_DetailsMetadata):
    """Generic metadata class.

    It defines all attributes of metadata classes for specific item types, so
    that it can be used during extraction instead of a more specific class, and
    later converted to the corresponding, more specific metadata class.
    """

    #: The search text used to find the item.
    searchText: Optional[str] = None


@attrs.define(kw_only=True)
class ArticleMetadata(_DetailsMetadata):
    """Metadata class for :data:`zyte_common_items.Article.metadata`."""


@attrs.define(kw_only=True)
class ArticleListMetadata(_ListMetadata):
    """Metadata class for :data:`zyte_common_items.ArticleList.metadata`."""


@attrs.define(kw_only=True)
class ArticleNavigationMetadata(_ListMetadata):
    """Metadata class for :data:`zyte_common_items.ArticleNavigation.metadata`."""


@attrs.define(kw_only=True)
class BusinessPlaceMetadata(Metadata):
    """Metadata class for :data:`zyte_common_items.BusinessPlace.metadata`."""


@attrs.define(kw_only=True)
class JobPostingMetadata(Metadata):
    """Metadata class for :data:`zyte_common_items.JobPosting.metadata`."""


@attrs.define(kw_only=True)
class ProductMetadata(_DetailsMetadata):
    """Metadata class for :data:`zyte_common_items.Product.metadata`."""


@attrs.define(kw_only=True)
class ProductListMetadata(_ListMetadata):
    """Metadata class for :data:`zyte_common_items.ProductList.metadata`."""


@attrs.define(kw_only=True)
class ProductNavigationMetadata(_ListMetadata):
    """Metadata class for :data:`zyte_common_items.ProductNavigation.metadata`."""


@attrs.define(kw_only=True)
class RealEstateMetadata(_DetailsMetadata):
    """Metadata class for :data:`zyte_common_items.RealEstate.metadata`."""


@attrs.define(kw_only=True)
class SocialMediaPostMetadata(Metadata):
    pass


###############################################################################


@attrs.define
class _Media(Item):
    #: URL.
    #:
    #: When multiple URLs exist for a given media element, pointing to
    #: different-quality versions, the highest-quality URL should be used.
    #:
    #: `Data URIs`_ are not allowed in this attribute.
    #:
    #: .. _Data URIs: https://en.wikipedia.org/wiki/Data_URI_scheme
    url: str = attrs.field(converter=url_to_str)


@attrs.define
class AdditionalProperty(Item):
    """A name-value pair.

    See :attr:`Product.additionalProperties
    <zyte_common_items.Product.additionalProperties>`.
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
    <zyte_common_items.Product.aggregateRating>`.
    """

    #: Maximum value of the rating system.
    bestRating: Optional[float] = None

    #: Average value of all ratings.
    ratingValue: Optional[float] = None

    #: Review count.
    reviewCount: Optional[int] = None


@attrs.define
class Audio(_Media):
    """Audio.

    See :class:`Article.audios <zyte_common_items.Article.audios>`.
    """


@attrs.define(kw_only=True)
class Author(Item):
    """Author of an article.

    See :attr:`Article.authors <zyte_common_items.Article.authors>`.
    """

    #: Email.
    email: Optional[str] = None

    #: URL of the details page of the author.
    url: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )

    #: Full name.
    name: Optional[str] = None

    #: Text from which :attr:`~zyte_common_items.Author.name` was
    #: extracted.
    nameRaw: Optional[str] = None


@attrs.define
class Brand(Item):
    """Brand.

    See :attr:`Product.brand <zyte_common_items.Product.brand>`.
    """

    #: Name as it appears on the source webpage (no post-processing).
    name: str


@attrs.define(kw_only=True)
class Breadcrumb(Item):
    """A breadcrumb from the `breadcrumb trail`_ of a webpage.

    See :attr:`Product.breadcrumbs
    <zyte_common_items.Product.breadcrumbs>`.

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

    See :class:`Product.gtin <zyte_common_items.Product.gtin>`.

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
class Image(_Media):
    """Image.

    See for example
    :class:`Product.images <zyte_common_items.Product.images>` and
    :class:`Product.mainImage <zyte_common_items.Product.mainImage>`.
    """


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


@attrs.define(kw_only=True)
class Header(Item):
    """An HTTP header"""

    #: Name of the header
    name: str

    #: Value of the header
    value: str


@attrs.define(slots=False)
class Request(Item):
    """Describe a web request to load a page"""

    #: HTTP URL
    url: str = attrs.field(converter=url_to_str)

    #: HTTP method
    method: str = "GET"

    #: HTTP request body, Base64-encoded
    body: Optional[str] = None

    #: HTTP headers
    headers: Optional[List[Header]] = None

    #: Name of the page being requested.
    name: Optional[str] = None

    _body_bytes = None

    @property
    def body_bytes(self) -> Optional[bytes]:
        """Request.body as bytes"""
        # todo: allow to set body bytes in __init__, to avoid encoding/decoding.
        if self._body_bytes is None:
            if self.body is not None:
                self._body_bytes = base64.b64decode(self.body)
        return self._body_bytes

    def to_scrapy(self, callback, **kwargs):
        """
        Convert a request to scrapy.Request.
        All kwargs are passed to scrapy.Request as-is.
        """
        import scrapy

        header_list = [(header.name, header.value) for header in self.headers or []]

        return scrapy.Request(
            url=self.url,
            callback=callback,
            method=self.method or "GET",
            headers=header_list,
            body=self.body_bytes,
            **kwargs,
        )


@attrs.define(kw_only=True)
class Url(Item):
    """A URL."""

    # : URL.
    url: str = attrs.field(converter=url_to_str)


@attrs.define
class Video(_Media):
    """Video.

    See :class:`Article.videos <zyte_common_items.Article.videos>`.
    """


@attrs.define(kw_only=True)
class ProbabilityRequest(Request, ProbabilityMixin):
    """A :class:`Request` that includes a probability value."""

    #: Data extraction process metadata.
    metadata: Optional[ProbabilityMetadata] = None


RequestT = TypeVar("RequestT", bound=Request)


def cast_request(value: Request, cls: Type[RequestT]) -> RequestT:
    """Convert *value*, an instance of :class:`Request` or a subclass, into
    *cls*, a different class that is also either :class:`Request` or a
    subclass."""
    new_value = convert_to_class(value, cls)
    if type(value) is Request and cls is ProbabilityRequest:
        new_value.metadata = ProbabilityMetadata(probability=1.0)
    return new_value


def request_list_processor(request_list: List[Request]) -> List[ProbabilityRequest]:
    """Convert all objects in *request_list*, which are instances of
    :class:`Request` or a subclass, into instances of
    :class:`ProbabilityRequest`."""
    return [cast_request(request, ProbabilityRequest) for request in request_list]


@attrs.define(kw_only=True)
class JobLocation(Item):
    """Location of a job offer."""

    #: Job location, as it appears on the website.
    raw: Optional[str] = None


@attrs.define(kw_only=True)
class BaseSalary(Item):
    """Base salary of a job offer."""

    #: Salary amount as it appears on the website.
    raw: Optional[str] = None

    #: The minimum value of the base salary as a number string.
    valueMin: Optional[str] = None

    #: The maximum value of the base salary as a number string.
    valueMax: Optional[str] = None

    #: The type of rate associated with the salary, e.g. monthly, annual, daily.
    rateType: Optional[str] = None

    #: Currency associated with the salary amount.
    currency: Optional[str] = None

    #: Currency associated with the salary amount, without normalization.
    currencyRaw: Optional[str] = None


@attrs.define(kw_only=True)
class HiringOrganization(Item):
    """Organization that is hiring for a job offer."""

    #: Name of the hiring organization.
    name: Optional[str] = None

    #: Organization information as available on the website.
    nameRaw: Optional[str] = None

    #: Identifier of the organization used by job posting website.
    id: Optional[str] = None


@attrs.define(kw_only=True)
class Reactions(Item):
    """Details of reactions to a post."""

    #: Number of times the post has been shared.
    reposts: Optional[int] = None

    #: Number of likes or other positive reactions to the post.
    likes: Optional[int] = None

    #: Number of dislikes or other negative reactions to the post.
    dislikes: Optional[int] = None


@attrs.define(kw_only=True)
class SocialMediaPostAuthor(Item):
    """Details of the author of a social media post."""

    #: The number of the followers that observe the author.
    numberOfFollowers: Optional[int] = None

    #: The number of the users that the author follows.
    numberOfFollowing: Optional[int] = None

    #: The date of the creation of the author's account.
    dateAccountCreated: Optional[str] = None

    #: The location of the author, if it's available in the author profile. Country or city location only.
    location: Optional[str] = None

    #: Indication if the author's account is verified.
    isVerified: Optional[bool] = None
