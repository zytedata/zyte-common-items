from __future__ import annotations

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    Breadcrumb,
    Image,
    Link,
    ListMetadata,
    ProbabilityMetadata,
)
from zyte_common_items.converters import to_metadata_optional, url_to_str_optional


@attrs.define(kw_only=True)
class ProductListMetadata(ListMetadata):
    """Metadata class for :data:`zyte_common_items.ProductList.metadata`."""


@attrs.define(slots=True, kw_only=True)
class ProductList(Item):
    """Product list from a product listing page of an e-commerce webpage.

    It represents, for example, a single page from a category.

    :attr:`url` is the only required attribute.
    """

    breadcrumbs: list[Breadcrumb] | None = None
    """Webpage `breadcrumb trail`_.

    .. _Breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    """

    canonicalUrl: str | None = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
    """Canonical form of the URL, as indicated by the website.

    See also ``url``.
    """

    categoryName: str | None = None
    """Name of the product listing as it appears on the webpage (no
    post-processing).

    For example, if the webpage is one of the pages of the Robots category,
    ``categoryName`` is ``'Robots'``.
    """

    metadata: ProductListMetadata | None = attrs.field(
        default=None,
        converter=to_metadata_optional(ProductListMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Data extraction process metadata."""

    pageNumber: int | None = None
    """Current page number, if displayed explicitly on the list page.

    Numeration starts with 1.
    """

    paginationNext: Link | None = None
    """Link to the next page."""

    products: list[ProductFromList] | None = None
    """List of products.

    It only includes product information found in the product listing page
    itself. Product information that requires visiting each product URL is not
    meant to be covered.

    The order of the products reflects their position on the rendered page.
    Product order is top-to-bottom, and left-to-right or right-to-left
    depending on the webpage locale.
    """

    url: str = attrs.field(converter=url_to_str_optional)
    """Main URL from which the data has been extracted.

    See also ``canonicalUrl``.
    """


@attrs.define(slots=True, kw_only=True)
class ProductFromList(Item):
    """Product from a product list from a product listing page of an e-commerce
    webpage.

    See :class:`ProductList`, :class:`ProductFromListExtractor`,
    :class:`ProductFromListSelectorExtractor`.
    """

    currency: str | None = None
    """Price currency `ISO 4217`_ alphabetic code (e.g. ``"USD"``).

    See also ``currencyRaw``.

    .. _ISO 4217: https://en.wikipedia.org/wiki/ISO_4217
    """

    currencyRaw: str | None = None
    """Price currency as it appears on the webpage (no post-processing), e.g.
    ``"$"``.

    See also ``currency``.
    """

    mainImage: Image | None = None
    """Main product image."""

    metadata: ProbabilityMetadata | None = attrs.field(
        default=None,
        converter=to_metadata_optional(ProbabilityMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Data extraction process metadata."""

    name: str | None = None
    """Name as it appears on the webpage (no post-processing)."""

    price: str | None = None
    """Price at which the product is being offered.

    It is a string with the price amount, with a full stop as decimal
    separator, and no thousands separator or currency (see ``currency`` and
    ``currencyRaw``), e.g. ``"10500.99"``.

    If ``regularPrice`` is not ``None``, ``price`` should always be lower than
    ``regularPrice``.
    """

    productId: str | None = None
    """Product identifier, unique within an e-commerce website.

    It may come in the form of an SKU or any other identifier, a hash, or even
    a URL.
    """

    regularPrice: str | None = None
    """Price at which the product was being offered in the past, and which is
    presented as a reference next to the current price.

    It may be labeled as the original price, the list price, or the maximum
    retail price for which the product is sold.

    See ``price`` for format details.

    If ``regularPrice`` is not ``None``, it should always be higher than
    ``price``.
    """

    url: str | None = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
    """Main URL from which the product data could be extracted."""
