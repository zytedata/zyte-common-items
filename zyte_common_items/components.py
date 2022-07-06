"""Classes for data nested within items."""

from typing import Optional

import attrs

from zyte_common_items.base import Item


@attrs.define(slots=True)
class AdditionalProperty(Item):
    """A name-value pair.

    See :attr:`Product.additionalProperties
    <zyte_common_items.Product.additionalProperties>`.
    """

    name: str
    value: str


@attrs.define(slots=True, kw_only=True)
class AggregateRating(Item):
    bestRating: Optional[float] = None
    ratingValue: Optional[float] = None
    reviewCount: Optional[int] = None


@attrs.define(slots=True)
class Brand(Item):
    """Details of a brand."""

    #: Name as it appears on the source webpage (no post-processing).
    name: str


@attrs.define(slots=True, kw_only=True)
class Breadcrumb(Item):
    """A breadcrumb from the `breadcrumb trail`_ of a webpage.

    .. _breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    """

    #: Text displayed.
    name: Optional[str] = None
    #: Target URL.
    url: Optional[str] = None


@attrs.define(slots=True)
class Gtin(Item):
    """GTIN_ type-value pair.

    See :class:`Product.gtin <zyte_common_items.Product.gtin>`.

    .. _GTIN: https://en.wikipedia.org/wiki/Global_Trade_Item_Number
    """

    #: Name of the GTIN format of ``value``.
    #:
    #: One of: ``"gtin13"``, ``"gtin8"``, ``"gtin14"``, ``"isbn10"``,
    #: ``"isbn13"``, ``"ismn"``, ``"issn"``, ``"upc"``.
    type: str

    #: GTIN value.
    #:
    #: It should only contain digits.
    value: str


@attrs.define(slots=True)
class Image(Item):
    """Image data."""

    #: URL.
    #:
    #: When multiple URLs exist for a given image, pointing to image files
    #: which are different-quality versions of the same image, the URL of the
    #: highest-quality image file should be used.
    #:
    #: `Data URIs`_ are not allowed in this attribute.
    #:
    #: .. _Data URIs: https://en.wikipedia.org/wiki/Data_URI_scheme
    url: str


@attrs.define(slots=True, kw_only=True)
class Metadata(Item):
    dateDownloaded: Optional[str] = None
    probability: Optional[float] = None
