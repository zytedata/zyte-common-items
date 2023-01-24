from typing import List, Union

import attrs
from web_poet import Unset, UnsetType

from zyte_common_items.base import Item
from zyte_common_items.components import (
    AdditionalProperty,
    AggregateRating,
    Brand,
    Breadcrumb,
    Gtin,
    Image,
    Link,
    Metadata,
)
from zyte_common_items.util import url_to_str


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
    additionalProperties: Union[List[AdditionalProperty], None, UnsetType] = Unset

    #: Availability status.
    #:
    #: The value is expected to be one of: ``"InStock"``, ``"OutOfStock"``.
    availability: Union[str, None, UnsetType] = Unset

    #: Canonical form of the URL, as indicated by the website.
    #:
    #: See also ``url``.
    canonicalUrl: Union[str, None, UnsetType] = attrs.field(
        default=Unset, converter=attrs.converters.optional(url_to_str), kw_only=True
    )

    #: Color.
    #:
    #: It is extracted as displayed (e.g. ``"white"``).
    #:
    #: See also ``size``, ``style``.
    color: Union[str, None, UnsetType] = Unset

    #: Price currency `ISO 4217`_ alphabetic code (e.g. ``"USD"``).
    #:
    #: See also ``currencyRaw``.
    #:
    #: .. _ISO 4217: https://en.wikipedia.org/wiki/ISO_4217
    currency: Union[str, None, UnsetType] = Unset

    #: Price currency as it appears on the webpage (no post-processing), e.g.
    #: ``"$"``.
    #:
    #: See also ``currency``.
    currencyRaw: Union[str, None, UnsetType] = Unset

    #: List of standardized GTIN_ product identifiers associated with the
    #: product, which are unique for the product across different sellers.
    #:
    #: See also: ``mpn``, ``productId``, ``sku``.
    #:
    #: .. _GTIN: https://en.wikipedia.org/wiki/Global_Trade_Item_Number
    gtin: Union[List[Gtin], None, UnsetType] = Unset

    #: All product images.
    #:
    #: The main image (see ``mainImage``) should be first in the list.
    #:
    #: Images only displayed as part of the product description are excluded.
    images: Union[List[Image], None, UnsetType] = Unset

    #: Main product image.
    mainImage: Union[Image, None, UnsetType] = Unset

    #: `Manufacturer part number (MPN)`_.
    #:
    #: A product should have the same MPN across different e-commerce websites.
    #:
    #: See also: ``gtin``, ``productId``, ``sku``.
    #:
    #: .. _Manufacturer part number (MPN): https://en.wikipedia.org/wiki/Part_number
    mpn: Union[str, None, UnsetType] = Unset

    #: Name as it appears on the webpage (no post-processing).
    name: Union[str, None, UnsetType] = Unset

    #: Price at which the product is being offered.
    #:
    #: It is a string with the price amount, with a full stop as decimal
    #: separator, and no thousands separator or currency (see ``currency`` and
    #: ``currencyRaw``), e.g. ``"10500.99"``.
    #:
    #: If ``regularPrice`` is not ``None``, ``price`` should always be lower
    #: than ``regularPrice``.
    price: Union[str, None, UnsetType] = Unset

    #: Product identifier, unique within an e-commerce website.
    #:
    #: It may come in the form of an SKU or any other identifier, a hash, or
    #: even a URL.
    #:
    #: See also: ``gtin``, ``mpn``, ``sku``.
    productId: Union[str, None, UnsetType] = Unset

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
    regularPrice: Union[str, None, UnsetType] = Unset

    #: Size or dimensions.
    #:
    #: Pertinent to products such as garments, shoes, accessories, etc.
    #:
    #: It is extracted as displayed (e.g. ``"XL"``).
    #:
    #: See also ``color``, ``style``.
    size: Union[str, None, UnsetType] = Unset

    #: `Stock keeping unit (SKU)`_ identifier, i.e. a merchant-specific product
    #: identifier.
    #:
    #: See also: ``gtin``, ``mpn``, ``productId``.
    #:
    #: .. _Stock keeping unit (SKU): https://en.wikipedia.org/wiki/Stock_keeping_unit
    sku: Union[str, None, UnsetType] = Unset

    #: Style.
    #:
    #: Pertinent to products such as garments, shoes, accessories, etc.
    #:
    #: It is extracted as displayed (e.g. ``"polka dots"``).
    #:
    #: See also ``color``, ``size``.
    style: Union[str, None, UnsetType] = Unset

    #: Main URL from which the product variant data could be extracted.
    #:
    #: See also ``canonicalUrl``.
    url: Union[str, None, UnsetType] = attrs.field(
        default=Unset, converter=attrs.converters.optional(url_to_str), kw_only=True
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
    additionalProperties: Union[List[AdditionalProperty], None, UnsetType] = Unset

    #: Aggregate data about reviews and ratings.
    aggregateRating: Union[AggregateRating, None, UnsetType] = Unset

    #: Availability status.
    #:
    #: The value is expected to be one of: ``"InStock"``, ``"OutOfStock"``.
    availability: Union[str, None, UnsetType] = Unset

    #: Brand.
    brand: Union[Brand, None, UnsetType] = Unset

    #: Webpage `breadcrumb trail`_.
    #:
    #: .. _Breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    breadcrumbs: Union[List[Breadcrumb], None, UnsetType] = Unset

    #: Canonical form of the URL, as indicated by the website.
    #:
    #: See also ``url``.
    canonicalUrl: Union[str, None, UnsetType] = attrs.field(
        default=Unset, converter=attrs.converters.optional(url_to_str), kw_only=True
    )

    #: Color.
    #:
    #: It is extracted as displayed (e.g. ``"white"``).
    #:
    #: See also ``size``, ``style``.
    color: Union[str, None, UnsetType] = Unset

    #: Price currency `ISO 4217`_ alphabetic code (e.g. ``"USD"``).
    #:
    #: See also ``currencyRaw``.
    #:
    #: .. _ISO 4217: https://en.wikipedia.org/wiki/ISO_4217
    currency: Union[str, None, UnsetType] = Unset

    #: Price currency as it appears on the webpage (no post-processing), e.g.
    #: ``"$"``.
    #:
    #: See also ``currency``.
    currencyRaw: Union[str, None, UnsetType] = Unset

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
    description: Union[str, None, UnsetType] = Unset

    #: HTML description.
    #:
    #: See ``description`` for extraction details.
    #:
    #: The format is not the raw HTML from the source webpage. See the `HTML
    #: normalization specification`_ for details.
    #:
    #: .. _HTML normalization specification: https://docs.zyte.com/automatic-extraction/article.html#format-of-articlebodyhtml-field
    descriptionHtml: Union[str, None, UnsetType] = Unset

    #: List of features.
    #:
    #: They are usually listed as bullet points in product webpages.
    #:
    #: See also ``additionalProperties``.
    features: Union[List[str], None, UnsetType] = Unset

    #: List of standardized GTIN_ product identifiers associated with the
    #: product, which are unique for the product across different sellers.
    #:
    #: See also: ``mpn``, ``productId``, ``sku``.
    #:
    #: .. _GTIN: https://en.wikipedia.org/wiki/Global_Trade_Item_Number
    gtin: Union[List[Gtin], None, UnsetType] = Unset

    #: All product images.
    #:
    #: The main image (see ``mainImage``) should be first in the list.
    #:
    #: Images only displayed as part of the product description are excluded.
    images: Union[List[Image], None, UnsetType] = Unset

    #: Main product image.
    mainImage: Union[Image, None, UnsetType] = Unset

    #: Data extraction process metadata.
    metadata: Union[Metadata, None, UnsetType] = Unset

    #: `Manufacturer part number (MPN)`_.
    #:
    #: A product should have the same MPN across different e-commerce websites.
    #:
    #: See also: ``gtin``, ``productId``, ``sku``.
    #:
    #: .. _Manufacturer part number (MPN): https://en.wikipedia.org/wiki/Part_number
    mpn: Union[str, None, UnsetType] = Unset

    #: Name as it appears on the webpage (no post-processing).
    name: Union[str, None, UnsetType] = Unset

    #: Price at which the product is being offered.
    #:
    #: It is a string with the price amount, with a full stop as decimal
    #: separator, and no thousands separator or currency (see ``currency`` and
    #: ``currencyRaw``), e.g. ``"10500.99"``.
    #:
    #: If ``regularPrice`` is not ``None``, ``price`` should always be lower
    #: than ``regularPrice``.
    price: Union[str, None, UnsetType] = Unset

    # Redefined to extend the documentation.
    #: Product identifier, unique within an e-commerce website.
    #:
    #: It may come in the form of an SKU or any other identifier, a hash, or
    #: even a URL.
    #:
    #: See also: ``gtin``, ``mpn``, ``sku``.
    productId: Union[str, None, UnsetType] = Unset

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
    regularPrice: Union[str, None, UnsetType] = Unset

    #: Size or dimensions.
    #:
    #: Pertinent to products such as garments, shoes, accessories, etc.
    #:
    #: It is extracted as displayed (e.g. ``"XL"``).
    #:
    #: See also ``color``, ``style``.
    size: Union[str, None, UnsetType] = Unset

    #: `Stock keeping unit (SKU)`_ identifier, i.e. a merchant-specific product
    #: identifier.
    #:
    #: See also: ``gtin``, ``mpn``, ``productId``.
    #:
    #: .. _Stock keeping unit (SKU): https://en.wikipedia.org/wiki/Stock_keeping_unit
    sku: Union[str, None, UnsetType] = Unset

    #: Style.
    #:
    #: Pertinent to products such as garments, shoes, accessories, etc.
    #:
    #: It is extracted as displayed (e.g. ``"polka dots"``).
    #:
    #: See also ``color``, ``size``.
    style: Union[str, None, UnsetType] = Unset

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
    variants: Union[List[ProductVariant], None, UnsetType] = Unset


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
    currency: Union[str, None, UnsetType] = Unset

    #: Price currency as it appears on the webpage (no post-processing), e.g.
    #: ``"$"``.
    #:
    #: See also ``currency``.
    currencyRaw: Union[str, None, UnsetType] = Unset

    #: Main product image.
    mainImage: Union[Image, None, UnsetType] = Unset

    #: Data extraction process metadata.
    metadata: Union[Metadata, None, UnsetType] = Unset

    #: Name as it appears on the webpage (no post-processing).
    name: Union[str, None, UnsetType] = Unset

    #: Price at which the product is being offered.
    #:
    #: It is a string with the price amount, with a full stop as decimal
    #: separator, and no thousands separator or currency (see ``currency`` and
    #: ``currencyRaw``), e.g. ``"10500.99"``.
    #:
    #: If ``regularPrice`` is not ``None``, ``price`` should always be lower
    #: than ``regularPrice``.
    price: Union[str, None, UnsetType] = Unset

    #: Product identifier, unique within an e-commerce website.
    #:
    #: It may come in the form of an SKU or any other identifier, a hash, or
    #: even a URL.
    productId: Union[str, None, UnsetType] = Unset

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
    regularPrice: Union[str, None, UnsetType] = Unset

    #: Main URL from which the product data could be extracted.
    url: Union[str, None, UnsetType] = attrs.field(
        default=Unset, converter=attrs.converters.optional(url_to_str), kw_only=True
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
    breadcrumbs: Union[List[Breadcrumb], None, UnsetType] = Unset

    #: Canonical form of the URL, as indicated by the website.
    #:
    #: See also ``url``.
    canonicalUrl: Union[str, None, UnsetType] = attrs.field(
        default=Unset, converter=attrs.converters.optional(url_to_str), kw_only=True
    )

    #: Name of the product listing as it appears on the webpage
    #: (no post-processing).
    #:
    #: For example, if the webpage is one of the pages of the Robots category,
    #: ``categoryName`` is ``'Robots'``.
    categoryName: Union[str, None, UnsetType] = Unset

    #: Data extraction process metadata.
    metadata: Union[Metadata, None, UnsetType] = Unset

    #: Number of the current page.
    #:
    #: It should only be extracted if the webpage shows a page number.
    #:
    #: It must be 1-based. For example, if the first page of a listing is
    #: numbered as 0 on the website, it should be extracted as `1` nonetheless.
    pageNumber: Union[int, None, UnsetType] = Unset

    #: Link to the next page.
    paginationNext: Union[Link, None, UnsetType] = Unset

    #: List of products.
    #:
    #: It only includes product information found in the product listing page
    #: itself. Product information that requires visiting each product URL is
    #: not meant to be covered.
    #:
    #: The order of the products reflects their position on the rendered page.
    #: Product order is top-to-bottom, and left-to-right or right-to-left
    #: depending on the webpage locale.
    products: Union[List[ProductFromList], None, UnsetType] = Unset

    #: Main URL from which the data has been extracted.
    #:
    #: See also ``canonicalUrl``.
    url: str = attrs.field(converter=url_to_str)
