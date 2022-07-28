"""Classes for data nested within items."""

from typing import Optional

import attrs

from zyte_common_items.base import Item


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
    url: Optional[str] = None


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
    url: str


@attrs.define(kw_only=True)
class Link(Item):
    """A link from a webpage to another webpage."""

    #: Displayed text.
    text: Optional[str] = None

    #: Target URL.
    url: Optional[str] = None


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
