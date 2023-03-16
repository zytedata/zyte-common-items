from typing import List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    AdditionalProperty,
    Address,
    AggregateRating,
    Amenity,
    Anchor,
    Brand,
    Breadcrumb,
    BusinessPlaceMetadata,
    Gtin,
    Image,
    Link,
    Metadata,
    OpeningHours,
    ParentPlace,
    StarRating,
)
from zyte_common_items.util import url_to_str, validate_timezone


@attrs.define(kw_only=True)
class ProductVariant(Item):
    """:class:`Product` variant.

    See :attr:`Product.variants`.
    """

    #: List of name-value pais of data about a specific, otherwise unmapped
    #: feature.
    #:
    #: Additional properties usually appear in product pages in the form of a
    #: specification table or a free-form specification list.
    #:
    #: Additional properties that require 1 or more extra requests may not be
    #: extracted.
    #:
    #: See also ``features``.
    additionalProperties: Optional[List[AdditionalProperty]] = None

    #: Availability status.
    #:
    #: The value is expected to be one of: ``"InStock"``, ``"OutOfStock"``.
    availability: Optional[str] = None

    #: Canonical form of the URL, as indicated by the website.
    #:
    #: See also ``url``.
    canonicalUrl: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )

    #: Color.
    #:
    #: It is extracted as displayed (e.g. ``"white"``).
    #:
    #: See also ``size``, ``style``.
    color: Optional[str] = None

    #: Price currency `ISO 4217`_ alphabetic code (e.g. ``"USD"``).
    #:
    #: See also ``currencyRaw``.
    #:
    #: .. _ISO 4217: https://en.wikipedia.org/wiki/ISO_4217
    currency: Optional[str] = None

    #: Price currency as it appears on the webpage (no post-processing), e.g.
    #: ``"$"``.
    #:
    #: See also ``currency``.
    currencyRaw: Optional[str] = None

    #: List of standardized GTIN_ product identifiers associated with the
    #: product, which are unique for the product across different sellers.
    #:
    #: See also: ``mpn``, ``productId``, ``sku``.
    #:
    #: .. _GTIN: https://en.wikipedia.org/wiki/Global_Trade_Item_Number
    gtin: Optional[List[Gtin]] = None

    #: All product images.
    #:
    #: The main image (see ``mainImage``) should be first in the list.
    #:
    #: Images only displayed as part of the product description are excluded.
    images: Optional[List[Image]] = None

    #: Main product image.
    mainImage: Optional[Image] = None

    #: `Manufacturer part number (MPN)`_.
    #:
    #: A product should have the same MPN across different e-commerce websites.
    #:
    #: See also: ``gtin``, ``productId``, ``sku``.
    #:
    #: .. _Manufacturer part number (MPN): https://en.wikipedia.org/wiki/Part_number
    mpn: Optional[str] = None

    #: Name as it appears on the webpage (no post-processing).
    name: Optional[str] = None

    #: Price at which the product is being offered.
    #:
    #: It is a string with the price amount, with a full stop as decimal
    #: separator, and no thousands separator or currency (see ``currency`` and
    #: ``currencyRaw``), e.g. ``"10500.99"``.
    #:
    #: If ``regularPrice`` is not ``None``, ``price`` should always be lower
    #: than ``regularPrice``.
    price: Optional[str] = None

    #: Product identifier, unique within an e-commerce website.
    #:
    #: It may come in the form of an SKU or any other identifier, a hash, or
    #: even a URL.
    #:
    #: See also: ``gtin``, ``mpn``, ``sku``.
    productId: Optional[str] = None

    #: Price at which the product was being offered in the past, and which is
    #: presented as a reference next to the current price.
    #:
    #: It may be labeled as the original price, the list price, or the maximum
    #: retail price for which the product is sold.
    #:
    #: See ``price`` for format details.
    #:
    #: If ``regularPrice`` is not ``None``, it should always be higher than
    #: ``price``.
    regularPrice: Optional[str] = None

    #: Size or dimensions.
    #:
    #: Pertinent to products such as garments, shoes, accessories, etc.
    #:
    #: It is extracted as displayed (e.g. ``"XL"``).
    #:
    #: See also ``color``, ``style``.
    size: Optional[str] = None

    #: `Stock keeping unit (SKU)`_ identifier, i.e. a merchant-specific product
    #: identifier.
    #:
    #: See also: ``gtin``, ``mpn``, ``productId``.
    #:
    #: .. _Stock keeping unit (SKU): https://en.wikipedia.org/wiki/Stock_keeping_unit
    sku: Optional[str] = None

    #: Style.
    #:
    #: Pertinent to products such as garments, shoes, accessories, etc.
    #:
    #: It is extracted as displayed (e.g. ``"polka dots"``).
    #:
    #: See also ``color``, ``size``.
    style: Optional[str] = None

    #: Main URL from which the product variant data could be extracted.
    #:
    #: See also ``canonicalUrl``.
    url: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )


@attrs.define(kw_only=True)
class Product(Item):
    """Product from an e-commerce website.

    The :attr:`url` attribute is the only required attribute, all other fields
    are optional.
    """

    #: List of name-value pais of data about a specific, otherwise unmapped
    #: feature.
    #:
    #: Additional properties usually appear in product pages in the form of a
    #: specification table or a free-form specification list.
    #:
    #: Additional properties that require 1 or more extra requests may not be
    #: extracted.
    #:
    #: See also ``features``.
    additionalProperties: Optional[List[AdditionalProperty]] = None

    #: Aggregate data about reviews and ratings.
    aggregateRating: Optional[AggregateRating] = None

    #: Availability status.
    #:
    #: The value is expected to be one of: ``"InStock"``, ``"OutOfStock"``.
    availability: Optional[str] = None

    #: Brand.
    brand: Optional[Brand] = None

    #: Webpage `breadcrumb trail`_.
    #:
    #: .. _Breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    breadcrumbs: Optional[List[Breadcrumb]] = None

    #: Canonical form of the URL, as indicated by the website.
    #:
    #: See also ``url``.
    canonicalUrl: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )

    #: Color.
    #:
    #: It is extracted as displayed (e.g. ``"white"``).
    #:
    #: See also ``size``, ``style``.
    color: Optional[str] = None

    #: Price currency `ISO 4217`_ alphabetic code (e.g. ``"USD"``).
    #:
    #: See also ``currencyRaw``.
    #:
    #: .. _ISO 4217: https://en.wikipedia.org/wiki/ISO_4217
    currency: Optional[str] = None

    #: Price currency as it appears on the webpage (no post-processing), e.g.
    #: ``"$"``.
    #:
    #: See also ``currency``.
    currencyRaw: Optional[str] = None

    #: Plain-text description.
    #:
    #: If the description is split across different parts of the source
    #: webpage, only the main part, containing the most useful pieces of
    #: information, should be extracted into this attribute.
    #:
    #: It may contain data found in other attributes (``features``,
    #: ``additionalProperties``).
    #:
    #: Format-wise:
    #:
    #: -   Line breaks and non-ASCII characters are allowed.
    #:
    #: -   There is no length limit for this attribute, the content should not
    #:     be truncated.
    #:
    #: -   There should be no whitespace at the beginning or end.
    #:
    #: See also ``descriptionHtml``.
    description: Optional[str] = None

    #: HTML description.
    #:
    #: See ``description`` for extraction details.
    #:
    #: The format is not the raw HTML from the source webpage. See the `HTML
    #: normalization specification`_ for details.
    #:
    #: .. _HTML normalization specification: https://docs.zyte.com/automatic-extraction/article.html#format-of-articlebodyhtml-field
    descriptionHtml: Optional[str] = None

    #: List of features.
    #:
    #: They are usually listed as bullet points in product webpages.
    #:
    #: See also ``additionalProperties``.
    features: Optional[List[str]] = None

    #: List of standardized GTIN_ product identifiers associated with the
    #: product, which are unique for the product across different sellers.
    #:
    #: See also: ``mpn``, ``productId``, ``sku``.
    #:
    #: .. _GTIN: https://en.wikipedia.org/wiki/Global_Trade_Item_Number
    gtin: Optional[List[Gtin]] = None

    #: All product images.
    #:
    #: The main image (see ``mainImage``) should be first in the list.
    #:
    #: Images only displayed as part of the product description are excluded.
    images: Optional[List[Image]] = None

    #: Main product image.
    mainImage: Optional[Image] = None

    #: Data extraction process metadata.
    metadata: Optional[Metadata] = None

    #: `Manufacturer part number (MPN)`_.
    #:
    #: A product should have the same MPN across different e-commerce websites.
    #:
    #: See also: ``gtin``, ``productId``, ``sku``.
    #:
    #: .. _Manufacturer part number (MPN): https://en.wikipedia.org/wiki/Part_number
    mpn: Optional[str] = None

    #: Name as it appears on the webpage (no post-processing).
    name: Optional[str] = None

    #: Price at which the product is being offered.
    #:
    #: It is a string with the price amount, with a full stop as decimal
    #: separator, and no thousands separator or currency (see ``currency`` and
    #: ``currencyRaw``), e.g. ``"10500.99"``.
    #:
    #: If ``regularPrice`` is not ``None``, ``price`` should always be lower
    #: than ``regularPrice``.
    price: Optional[str] = None

    # Redefined to extend the documentation.
    #: Product identifier, unique within an e-commerce website.
    #:
    #: It may come in the form of an SKU or any other identifier, a hash, or
    #: even a URL.
    #:
    #: See also: ``gtin``, ``mpn``, ``sku``.
    productId: Optional[str] = None

    #: Price at which the product was being offered in the past, and which is
    #: presented as a reference next to the current price.
    #:
    #: It may be labeled as the original price, the list price, or the maximum
    #: retail price for which the product is sold.
    #:
    #: See ``price`` for format details.
    #:
    #: If ``regularPrice`` is not ``None``, it should always be higher than
    #: ``price``.
    regularPrice: Optional[str] = None

    #: Size or dimensions.
    #:
    #: Pertinent to products such as garments, shoes, accessories, etc.
    #:
    #: It is extracted as displayed (e.g. ``"XL"``).
    #:
    #: See also ``color``, ``style``.
    size: Optional[str] = None

    #: `Stock keeping unit (SKU)`_ identifier, i.e. a merchant-specific product
    #: identifier.
    #:
    #: See also: ``gtin``, ``mpn``, ``productId``.
    #:
    #: .. _Stock keeping unit (SKU): https://en.wikipedia.org/wiki/Stock_keeping_unit
    sku: Optional[str] = None

    #: Style.
    #:
    #: Pertinent to products such as garments, shoes, accessories, etc.
    #:
    #: It is extracted as displayed (e.g. ``"polka dots"``).
    #:
    #: See also ``color``, ``size``.
    style: Optional[str] = None

    #: Main URL from which the data has been extracted.
    #:
    #: See also ``canonicalUrl``.
    url: str = attrs.field(converter=url_to_str)

    #: List of variants.
    #:
    #: When slightly different versions of a product are displayed on the same
    #: product page, allowing you to choose a specific product version from a
    #: selection, each of those product versions are considered a product
    #: variant.
    #:
    #: Product variants usually differ in ``color`` or ``size``.
    #:
    #: The following items are *not* considered product variants:
    #:
    #: -   Different products within the same bundle of products.
    #:
    #: -   Product add-ons, e.g. premium upgrades of a base product.
    #:
    #: Only variant-specific data is extracted as product variant details. For
    #: example, if variant-specific versions of the product description do not
    #: exist in the source webpage, the description attributes of the product
    #: variant are *not* filled with the base product description.
    #:
    #: Extracted product variants may not include those that are not visible in
    #: the source webpage.
    #:
    #: Product variant details may not include those that require multiple
    #: additional requests (e.g. 1 or more requests per variant).
    variants: Optional[List[ProductVariant]] = None


@attrs.define(slots=True, kw_only=True)
class ProductFromList(Item):
    """Product from a product list from a product listing page of an e-commerce
    webpage.

    See :class:`ProductList`.
    """

    #: Price currency `ISO 4217`_ alphabetic code (e.g. ``"USD"``).
    #:
    #: See also ``currencyRaw``.
    #:
    #: .. _ISO 4217: https://en.wikipedia.org/wiki/ISO_4217
    currency: Optional[str] = None

    #: Price currency as it appears on the webpage (no post-processing), e.g.
    #: ``"$"``.
    #:
    #: See also ``currency``.
    currencyRaw: Optional[str] = None

    #: Main product image.
    mainImage: Optional[Image] = None

    #: Data extraction process metadata.
    metadata: Optional[Metadata] = None

    #: Name as it appears on the webpage (no post-processing).
    name: Optional[str] = None

    #: Price at which the product is being offered.
    #:
    #: It is a string with the price amount, with a full stop as decimal
    #: separator, and no thousands separator or currency (see ``currency`` and
    #: ``currencyRaw``), e.g. ``"10500.99"``.
    #:
    #: If ``regularPrice`` is not ``None``, ``price`` should always be lower
    #: than ``regularPrice``.
    price: Optional[str] = None

    #: Product identifier, unique within an e-commerce website.
    #:
    #: It may come in the form of an SKU or any other identifier, a hash, or
    #: even a URL.
    productId: Optional[str] = None

    #: Price at which the product was being offered in the past, and which is
    #: presented as a reference next to the current price.
    #:
    #: It may be labeled as the original price, the list price, or the maximum
    #: retail price for which the product is sold.
    #:
    #: See ``price`` for format details.
    #:
    #: If ``regularPrice`` is not ``None``, it should always be higher than
    #: ``price``.
    regularPrice: Optional[str] = None

    #: Main URL from which the product data could be extracted.
    url: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )


@attrs.define(slots=True, kw_only=True)
class ProductList(Item):
    """Product list from a product listing page of an e-commerce webpage.

    It represents, for example, a single page from a category.

    The :attr:`url` attribute is the only required attribute, all other fields
    are optional.
    """

    #: Webpage `breadcrumb trail`_.
    #:
    #: .. _Breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    breadcrumbs: Optional[List[Breadcrumb]] = None

    #: Canonical form of the URL, as indicated by the website.
    #:
    #: See also ``url``.
    canonicalUrl: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )

    #: Name of the product listing as it appears on the webpage
    #: (no post-processing).
    #:
    #: For example, if the webpage is one of the pages of the Robots category,
    #: ``categoryName`` is ``'Robots'``.
    categoryName: Optional[str] = None

    #: Data extraction process metadata.
    metadata: Optional[Metadata] = None

    #: Number of the current page.
    #:
    #: It should only be extracted if the webpage shows a page number.
    #:
    #: It must be 1-based. For example, if the first page of a listing is
    #: numbered as 0 on the website, it should be extracted as `1` nonetheless.
    pageNumber: Optional[int] = None

    #: Link to the next page.
    paginationNext: Optional[Link] = None

    #: List of products.
    #:
    #: It only includes product information found in the product listing page
    #: itself. Product information that requires visiting each product URL is
    #: not meant to be covered.
    #:
    #: The order of the products reflects their position on the rendered page.
    #: Product order is top-to-bottom, and left-to-right or right-to-left
    #: depending on the webpage locale.
    products: Optional[List[ProductFromList]] = None

    #: Main URL from which the data has been extracted.
    #:
    #: See also ``canonicalUrl``.
    url: str = attrs.field(converter=url_to_str)


@attrs.define(slots=True, kw_only=True)
class BusinessPlace(Item):
    """Business Place from a Google Maps Search."""

    #: Unique identifier of the place on the website.
    placeId: Optional[str] = None

    #: The main URL that the place data was extracted from.
    #:
    #: The URL of the final response, after any redirects.
    #:
    #: Required attribute.
    #:
    #: In case there is no product data on the page or the page was not reached, the returned "empty"
    #: item would still contain url field and metadata field with dateDownloaded.
    #:
    #: example: https://www.google.com/maps?cid=8273826543880430215
    url: str = attrs.field(converter=url_to_str)

    #: The name of the place
    name: Optional[str] = None

    #: List of actions that can be performed directly from the URLs on the place page, including URLs.
    actions: Optional[List[Anchor]] = None

    #: List of name-value pais of any unmapped additional properties specific to the place
    additionalProperties: Optional[List[AdditionalProperty]] = None

    #: The address details of the place.
    address: Optional[Address] = None

    #: The details of the reservation action,
    #: e.g. table reservation in case of restaurants
    #: or room reservation in case of hotels.
    reservationAction: Optional[Anchor] = None

    #: List of categories the place belongs to.
    categories: Optional[List[str]] = None

    #: The description of the place
    #:
    #: Stripped of white spaces
    description: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(lambda x: x.strip())
    )

    #: List of frequently mentioned features of this place.
    features: Optional[List[str]] = None

    #: URL to a map of the place.
    map: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
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
    openingHours: Optional[List[OpeningHours]] = None

    #: List of partner review sites.
    reviewSites: Optional[List[Anchor]] = None

    #: The phone number associated with the place, as it appears on the page.
    telephone: Optional[str] = None

    #: How is the price range of the place viewed by its customers (from z to zzzz).
    priceRange: Optional[str] = attrs.field(
        default=None,
        validator=attrs.validators.optional(attrs.validators.matches_re("^{1,4}$")),
    )

    #: Which timezone is the place situated in.
    #:
    #: Standard: Name compliant with IANA tz database (tzdata).
    timezone: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(validate_timezone)
    )

    #: If the information is verified by the owner of this place.
    isVerified: Optional[bool] = None

    #: The URL pointing to the official website of the place.
    website: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )

    #:  List of the tags associated with the place.
    tags: Optional[List[str]] = None

    #: Data extraction process metadata.
    metadata: Optional[BusinessPlaceMetadata] = None
