from typing import List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    AdditionalProperty,
    Address,
    AggregateRating,
    Amenity,
    ArticleListMetadata,
    ArticleMetadata,
    ArticleNavigationMetadata,
    Audio,
    Author,
    BaseSalary,
    Brand,
    Breadcrumb,
    BusinessPlaceMetadata,
    Gtin,
    HiringOrganization,
    Image,
    JobLocation,
    JobPostingMetadata,
    Link,
    NamedLink,
    OpeningHoursItem,
    ParentPlace,
    ProbabilityMetadata,
    ProbabilityRequest,
    ProductListMetadata,
    ProductMetadata,
    ProductNavigationMetadata,
    Reactions,
    RealEstateArea,
    RealEstateMetadata,
    Request,
    SocialMediaPostAuthor,
    SocialMediaPostMetadata,
    StarRating,
    Url,
    Video,
    cast_request,
)
from zyte_common_items.util import MetadataCaster, url_to_str


@attrs.define(slots=True, kw_only=True)
class ArticleFromList(Item):
    """Article from an article list from an article listing page.

    See :class:`ArticleList`.
    """

    #: Clean text of the article, including sub-headings, with newline
    #: separators.
    #:
    #: Format:
    #:
    #: - trimmed (no whitespace at the beginning or the end of the body
    #:   string),
    #: - line breaks included,
    #: - no length limit,
    #: - no normalization of Unicode characters.
    articleBody: Optional[str] = None

    #: All authors of the article.
    authors: Optional[List[Author]] = None

    #: Publication date of the article.
    #:
    #: Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ" or
    #: "YYYY-MM-DDThh:mm:ss±zz:zz".
    #:
    #: With timezone, if available.
    #:
    #: If the actual publication date is not found, the date of the last
    #: modification is used instead.
    datePublished: Optional[str] = None

    #: Same date as
    #: :attr:`~zyte_common_items.ArticleFromList.datePublished`, but
    #: :before parsing/normalization, i.e. as it appears on the website.
    datePublishedRaw: Optional[str] = None

    #: Headline or title.
    headline: Optional[str] = None

    #: Language of the article, as an ISO 639-1 language code.
    #:
    #: Sometimes the article language is not the same as the web page overall
    #: language.
    inLanguage: Optional[str] = None

    #: Main image.
    mainImage: Optional[Image] = None

    #: All images.
    images: Optional[List[Image]] = None

    #: Data extraction process metadata.
    metadata: Optional[ProbabilityMetadata] = attrs.field(
        default=None, converter=attrs.converters.optional(MetadataCaster(ProbabilityMetadata)), kw_only=True  # type: ignore
    )

    #: Main URL.
    url: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )


@attrs.define(kw_only=True)
class Article(Item):
    """Article, typically seen on online news websites, blogs, or announcement
    sections.

    :attr:`url` is the only required attribute.
    """

    #: Headline or title.
    headline: Optional[str] = None

    #: Publication date of the article.
    #:
    #: Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ" or
    #: "YYYY-MM-DDThh:mm:ss±zz:zz".
    #:
    #: With timezone, if available.
    #:
    #: If the actual publication date is not found, the value of
    #: :attr:`~zyte_common_items.Article.dateModified` is used instead.
    datePublished: Optional[str] = None

    #: Same date as
    #: :attr:`~zyte_common_items.Article.datePublished`, but
    #: :before parsing/normalization, i.e. as it appears on the website.
    datePublishedRaw: Optional[str] = None

    #: Date when the article was most recently modified.
    #:
    #: Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ" or
    #: "YYYY-MM-DDThh:mm:ss±zz:zz".
    #:
    #: With timezone, if available.
    dateModified: Optional[str] = None

    #: Same date as
    #: :attr:`~zyte_common_items.Article.dateModified`, but
    #: :before parsing/normalization, i.e. as it appears on the website.
    dateModifiedRaw: Optional[str] = None

    #: All authors of the article.
    authors: Optional[List[Author]] = None

    #: Webpage `breadcrumb trail`_.
    #:
    #: .. _Breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    breadcrumbs: Optional[List[Breadcrumb]] = None

    #: Language of the article, as an ISO 639-1 language code.
    #:
    #: Sometimes the article language is not the same as the web page overall
    #: language.
    inLanguage: Optional[str] = None

    #: Main image.
    mainImage: Optional[Image] = None

    #: All images.
    images: Optional[List[Image]] = None

    #: A short summary of the article.
    #:
    #: It can be either human-provided (if available), or auto-generated.
    description: Optional[str] = None

    #: Clean text of the article, including sub-headings, with newline
    #: separators.
    #:
    #: Format:
    #:
    #: - trimmed (no whitespace at the beginning or the end of the body
    #:   string),
    #: - line breaks included,
    #: - no length limit,
    #: - no normalization of Unicode characters.
    articleBody: Optional[str] = None

    #: Simplified and standardized HTML of the article, including sub-headings,
    #: image captions and embedded content (videos, tweets, etc.).
    #:
    #: Format: HTML string normalized in a consistent way.
    articleBodyHtml: Optional[str] = None

    #: All videos.
    videos: Optional[List[Video]] = None

    #: All audios.
    audios: Optional[List[Audio]] = None

    #: Canonical form of the URL, as indicated by the website.
    #:
    #: See also ``url``.
    canonicalUrl: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )

    #: The main URL of the article page.
    #:
    #: The URL of the final response, after any redirects.
    #:
    #: Required attribute.
    #:
    #: In case there is no article data on the page or the page was not
    #: reached, the returned "empty" item would still contain this URL field.
    url: str = attrs.field(converter=url_to_str)

    #: Data extraction process metadata.
    metadata: Optional[ArticleMetadata] = attrs.field(
        default=None, converter=attrs.converters.optional(MetadataCaster(ArticleMetadata)), kw_only=True  # type: ignore
    )


@attrs.define(slots=True, kw_only=True)
class ArticleList(Item):
    """Article list from an article listing page.

    The :attr:`url` attribute is the only required attribute, all other fields
    are optional.
    """

    #: The main URL of the article list.
    #:
    #: The URL of the final response, after any redirects.
    #:
    #: Required attribute.
    #:
    #: In case there is no article list data on the page or the page was not
    #: reached, the returned item still contain this URL field and all the
    #: other available datapoints.
    url: str = attrs.field(converter=url_to_str)

    #: Canonical form of the URL, as indicated by the website.
    #:
    #: See also ``url``.
    canonicalUrl: Optional[str] = attrs.field(
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )

    #: List of article details found on the page.
    #:
    #: The order of the articles reflects their position on the page.
    articles: Optional[List[ArticleFromList]] = None

    #: Webpage `breadcrumb trail`_.
    #:
    #: .. _Breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    breadcrumbs: Optional[List[Breadcrumb]] = None

    #: Data extraction process metadata.
    metadata: Optional[ArticleListMetadata] = attrs.field(
        default=None, converter=attrs.converters.optional(MetadataCaster(ArticleListMetadata)), kw_only=True  # type: ignore
    )


@attrs.define(kw_only=True)
class ProductVariant(Item):
    """:class:`Product` variant.

    See :attr:`Product.variants`, :class:`ProductVariantExtractor`,
    :class:`ProductVariantSelectorExtractor`.
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

    :attr:`url` is the only required attribute.
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
    metadata: Optional[ProductMetadata] = attrs.field(
        default=None, converter=attrs.converters.optional(MetadataCaster(ProductMetadata)), kw_only=True  # type: ignore
    )

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

    See :class:`ProductList`, :class:`ProductFromListExtractor`,
    :class:`ProductFromListSelectorExtractor`.
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
    metadata: Optional[ProbabilityMetadata] = attrs.field(
        default=None, converter=attrs.converters.optional(MetadataCaster(ProbabilityMetadata)), kw_only=True  # type: ignore
    )

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

    :attr:`url` is the only required attribute.
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
    metadata: Optional[ProductListMetadata] = attrs.field(
        default=None, converter=attrs.converters.optional(MetadataCaster(ProductListMetadata)), kw_only=True  # type: ignore
    )

    #: Current page number, if displayed explicitly on the list page.
    #:
    #: Numeration starts with 1.
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
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
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
        default=None, converter=attrs.converters.optional(url_to_str), kw_only=True
    )

    #:  List of the tags associated with the place.
    tags: Optional[List[str]] = None

    #: Data extraction process metadata.
    metadata: Optional[BusinessPlaceMetadata] = attrs.field(
        default=None, converter=attrs.converters.optional(MetadataCaster(BusinessPlaceMetadata)), kw_only=True  # type: ignore
    )


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
        default=None, converter=attrs.converters.optional(MetadataCaster(RealEstateMetadata)), kw_only=True  # type: ignore
    )


class RequestListCaster:
    """attrs converter to turn lists of :class:`Request` instances into lists
    of :class:`ProbabilityRequest` instances."""

    def __init__(self, target):
        self._target = target

    def __call__(self, value):
        return [cast_request(item, self._target) for item in value]


@attrs.define(kw_only=True)
class ProductNavigation(Item):
    """Represents the navigational aspects of a product listing page on an
    e-commerce website"""

    #: Main URL from which the data is extracted.
    url: str = attrs.field(converter=url_to_str)

    #: Name of the category/page with the product list.
    #:
    #: Format:
    #:
    #: - trimmed (no whitespace at the beginning or the end of the description string)
    categoryName: Optional[str] = None

    #: List of sub-category links ordered by their position in the page.
    subCategories: Optional[List[ProbabilityRequest]] = attrs.field(
        default=None, converter=attrs.converters.optional(RequestListCaster(ProbabilityRequest)), kw_only=True  # type: ignore
    )

    #: List of product links found on the page category ordered by their position in the page.
    items: Optional[List[ProbabilityRequest]] = attrs.field(
        default=None, converter=attrs.converters.optional(RequestListCaster(ProbabilityRequest)), kw_only=True  # type: ignore
    )

    #: A link to the next page, if available.
    nextPage: Optional[Request] = None

    #: Number of the current page.
    #:
    #: It should only be extracted if the webpage shows a page number.
    #:
    #: It must be 1-based. For example, if the first page of a listing is
    #: numbered as 0 on the website, it should be extracted as `1` nonetheless.
    pageNumber: Optional[int] = None

    #: Data extraction process metadata.
    metadata: Optional[ProductNavigationMetadata] = attrs.field(
        default=None, converter=attrs.converters.optional(MetadataCaster(ProductNavigationMetadata)), kw_only=True  # type: ignore
    )


@attrs.define(kw_only=True)
class ArticleNavigation(Item):
    """Represents the navigational aspects of an article listing webpage.

    See :class:`ArticleList`.
    """

    #: Main URL from which the data is extracted.
    url: str = attrs.field(converter=url_to_str)

    #: Name of the category/page.
    #:
    #: Format:
    #:
    #: - trimmed (no whitespace at the beginning or the end of the description string)
    categoryName: Optional[str] = None

    #: List of sub-category links ordered by their position in the page.
    subCategories: Optional[List[ProbabilityRequest]] = attrs.field(
        default=None, converter=attrs.converters.optional(RequestListCaster(ProbabilityRequest)), kw_only=True  # type: ignore
    )

    #: Links to listed items in order of appearance.
    items: Optional[List[ProbabilityRequest]] = attrs.field(
        default=None, converter=attrs.converters.optional(RequestListCaster(ProbabilityRequest)), kw_only=True  # type: ignore
    )

    #: A link to the next page, if available.
    nextPage: Optional[Request] = None

    #: Number of the current page.
    #:
    #: It should only be extracted if the webpage shows a page number.
    #:
    #: It must be 1-based. For example, if the first page of a listing is
    #: numbered as 0 on the website, it should be extracted as `1` nonetheless.
    pageNumber: Optional[int] = None

    #: Data extraction process metadata.
    metadata: Optional[ArticleNavigationMetadata] = attrs.field(
        default=None, converter=attrs.converters.optional(MetadataCaster(ArticleNavigationMetadata)), kw_only=True  # type: ignore
    )


@attrs.define(kw_only=True)
class JobPosting(Item):
    """A job posting, typically seen on job posting websites or websites of
    companies that are hiring.

    :attr:`url` is the only required attribute.
    """

    #: The url of the final response, after any redirects.
    url: str = attrs.field(converter=url_to_str)

    #: The identifier of the job posting.
    jobPostingId: Optional[str] = None

    #: Publication date of the job posting.
    #:
    #: Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"
    #:
    #: With timezone, if available.
    datePublished: Optional[str] = None

    #: Same date as datePublished, but before parsing/normalization, i.e. as it appears on the website.
    datePublishedRaw: Optional[str] = None

    #: The date when the job posting was most recently modified.
    #:
    #: Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"
    #:
    #: With timezone, if available.
    dateModified: Optional[str] = None

    #: Same date as dateModified, but before parsing/normalization, i.e. as it appears on the website.
    dateModifiedRaw: Optional[str] = None

    #: The date after which the job posting is not valid, e.g. the end of an offer.
    #:
    #: Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"
    #:
    #: With timezone, if available.
    validThrough: Optional[str] = None

    #: Same date as validThrough, but before parsing/normalization, i.e. as it appears on the website.
    validThroughRaw: Optional[str] = None

    #: The title of the job posting.
    jobTitle: Optional[str] = None

    #: The headline of the job posting.
    headline: Optional[str] = None

    #: A (typically single) geographic location associated with the job position.
    jobLocation: Optional[JobLocation] = None

    #: A description of the job posting including sub-headings, with newline separators.
    #:
    #: Format:
    #:
    #: - trimmed (no whitespace at the beginning or the end of the description string),
    #:
    #: - line breaks included,
    #:
    #: - no length limit,
    #:
    #: - no normalization of Unicode characters.
    description: Optional[str] = None

    #: Simplified HTML of the description, including sub-headings, image captions and embedded content.
    descriptionHtml: Optional[str] = None

    #: Type of employment (e.g. full-time, part-time, contract, temporary, seasonal, internship).
    employmentType: Optional[str] = None

    #: The base salary of the job or of an employee in the proposed role.
    baseSalary: Optional[BaseSalary] = None

    #: Candidate requirements for the job.
    requirements: Optional[List[str]] = None

    #: Information about the organization offering the job position.
    hiringOrganization: Optional[HiringOrganization] = None

    #: Job start date
    #:
    #: Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"
    #:
    #: With timezone, if available.
    jobStartDate: Optional[str] = None

    #: Same date as jobStartDate, but before parsing/normalization, i.e. as it appears on the website.
    jobStartDateRaw: Optional[str] = None

    #: Specifies the remote status of the position.
    remoteStatus: Optional[str] = None

    #: Contains metadata about the data extraction process.
    metadata: Optional[JobPostingMetadata] = attrs.field(
        default=None, converter=attrs.converters.optional(MetadataCaster(JobPostingMetadata)), kw_only=True  # type: ignore
    )


@attrs.define(kw_only=True)
class SocialMediaPost(Item):
    """Represents a single social media post."""

    #: The URL of the final response, after any redirects.
    url: str = attrs.field(converter=url_to_str)

    #: The identifier of the post.
    postId: Optional[str] = None

    #: Details of reactions to the post.
    reactions: Optional[Reactions] = None

    #: The text content of the post.
    text: Optional[str] = None

    #: The timestamp at which the post was created.
    #:
    #: Format: Timezone: UTC. ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"
    datePublished: Optional[str] = None

    #: The list of hashtags contained in the post.
    hashtags: Optional[List[str]] = None

    #: The list of URLs of media files (images, videos, etc.) linked from the post.
    mediaUrls: Optional[List[Url]] = None

    #: Details of the author of the post.
    #:
    #: No easily identifiable information can be contained in here, such as usernames.
    author: Optional[SocialMediaPostAuthor] = None

    #: Contains metadata about the data extraction process.
    metadata: Optional[SocialMediaPostMetadata] = attrs.field(
        default=None, converter=attrs.converters.optional(MetadataCaster(SocialMediaPostMetadata)), kw_only=True  # type: ignore
    )
