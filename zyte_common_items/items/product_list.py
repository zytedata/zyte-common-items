from __future__ import annotations

from typing import List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    Breadcrumb,
    Image,
    Link,
    ListMetadata,
    ProbabilityMetadata,
)
from zyte_common_items.converters import (
    to_metadata_optional,
    url_to_str,
    url_to_str_optional,
)


@attrs.define(kw_only=True)
class ProductListMetadata(ListMetadata):
    """Metadata class for :data:`zyte_common_items.ProductList.metadata`."""


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
        default=None, converter=url_to_str_optional, kw_only=True
    )

    #: Name of the product listing as it appears on the webpage
    #: (no post-processing).
    #:
    #: For example, if the webpage is one of the pages of the Robots category,
    #: ``categoryName`` is ``'Robots'``.
    categoryName: Optional[str] = None

    #: Data extraction process metadata.
    metadata: Optional[ProductListMetadata] = attrs.field(
        default=None, converter=to_metadata_optional(ProductListMetadata), kw_only=True  # type: ignore[misc]
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
        default=None, converter=to_metadata_optional(ProbabilityMetadata), kw_only=True  # type: ignore[misc]
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
        default=None, converter=url_to_str_optional, kw_only=True
    )
