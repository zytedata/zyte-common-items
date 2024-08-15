from __future__ import annotations

from typing import Any, Dict, List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    AdditionalProperty,
    AggregateRating,
    Brand,
    Breadcrumb,
    DetailsMetadata,
    Gtin,
    Image,
)
from zyte_common_items.converters import (
    to_metadata_optional,
    url_to_str,
    url_to_str_optional,
)


@attrs.define(kw_only=True)
class ProductMetadata(DetailsMetadata):
    """Metadata class for :data:`zyte_common_items.Product.metadata`."""


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
        default=None, converter=url_to_str_optional, kw_only=True
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

    #: Extracted custom attributes.
    customAttributes: Optional[Dict[str, Any]] = None

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
        default=None, converter=to_metadata_optional(ProductMetadata), kw_only=True  # type: ignore[misc]
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
        default=None, converter=url_to_str_optional, kw_only=True
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
        default=None, converter=url_to_str_optional, kw_only=True
    )
