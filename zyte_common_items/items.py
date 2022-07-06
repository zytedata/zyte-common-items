from typing import List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    AdditionalProperty,
    AggregateRating,
    Brand,
    Breadcrumb,
    Gtin,
    Image,
    Metadata,
)


@attrs.define(slots=True, kw_only=True)
class _ProductBase(Item):
    #: List of name-value pais of data about a specific, otherwise unmapped
    #: feature.
    #:
    #: Additional properties usually appear in product pages in the form of a
    #: specification table or a free-form specification list.
    additionalProperties: Optional[List[AdditionalProperty]] = None

    #: Availability status.
    #:
    #: The value is expected to be one of: ``"InStock"``, ``"OutOfStock"``.
    availability: Optional[str] = None

    #: Canonical form of the URL, as indicated by the website.
    #:
    #: See also ``url``.
    canonicalUrl: Optional[str] = None

    color: Optional[str] = None

    #: Price currency `ISO 4217`_ alphabetic code.
    #:
    #: See also ``currencyRaw``.
    #:
    #: .. _ISO 4217: https://en.wikipedia.org/wiki/ISO_4217
    currency: Optional[str] = None

    #: Price currency as it appears on the product webpage (no
    #: post-processing).
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

    #: Name as it appears on the product webpage (no post-processing).
    name: Optional[str] = None

    #: Price at which the product is being offered.
    #:
    #: It is a string with the price amount, with a full stop as decimal
    #: separator, and no thousands separator or currency (see ``currency`` and
    #: ``currencyRaw``).
    #:
    #: If ``regularPrice`` is not ``None``, ``price`` should always be lower
    #: than ``regularPrice``.
    price: Optional[str] = None

    #: Product identifier, unique across an e-commerce website.
    #:
    #: It may come in the form of an SKU, any other identifier, a hash, or even
    #: a URL.
    #:
    #: See also: ``gtin``, ``mpn``, ``sku``.
    productId: Optional[str] = None

    #: Price at which the product was being offered in the past, and which is
    #: presented as a reference next to the current price.
    #:
    #: It may be labeled as the original price, the list price, or the maximum
    #: retail price for which the product is sold.
    #:
    #: It is a string with the price amount, with a full stop as decimal
    #: separator, and no thousands separator or currency (see ``currency`` and
    #: ``currencyRaw``).
    #:
    #: If ``regularPrice`` is not ``None``, it should always be higher than
    #: ``price``.
    regularPrice: Optional[str] = None
    size: Optional[str] = None

    #: `Stock keeping unit (SKU)`_ identifier, i.e. a merchant-specific product
    #: identifier.
    #:
    #: See also: ``gtin``, ``mpn``, ``productId``.
    #:
    #: .. _Stock keeping unit (SKU): https://en.wikipedia.org/wiki/Stock_keeping_unit
    sku: Optional[str] = None
    style: Optional[str] = None


@attrs.define(slots=True, kw_only=True)
class ProductVariant(_ProductBase):
    #: Main URL from which the product variant data has been extracted.
    #:
    #: See also ``canonicalUrl``.
    url: Optional[str] = None


@attrs.define(slots=True, kw_only=True)
class Product(_ProductBase):
    """Product from an e-commerce website.

    The :attr:`url` attribute is the only required attribute, all other fields
    are optional.
    """

    aggregateRating: Optional[AggregateRating] = None

    #: Brand
    brand: Optional[Brand] = None

    #: `Breadcrumb trail`_ of the product webpage.
    #:
    #: .. _Breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    breadcrumbs: Optional[List[Breadcrumb]] = None
    description: Optional[str] = None
    descriptionHtml: Optional[str] = None
    features: Optional[List[str]] = None
    metadata: Optional[Metadata] = None

    #: Main URL from which the product data has been extracted.
    #:
    #: See also ``canonicalUrl``.
    url: str
    variants: Optional[List[ProductVariant]] = None
