import attrs

from zyte_common_items import Item
from zyte_common_items.util import url_to_str


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
class Image(_Media):
    """Image.

    See for example
    :class:`Product.images <zyte_common_items.Product.images>` and
    :class:`Product.mainImage <zyte_common_items.Product.mainImage>`.
    """


@attrs.define
class Audio(_Media):
    """Audio.

    See :class:`Article.audios <zyte_common_items.Article.audios>`.
    """


@attrs.define
class Video(_Media):
    """Video.

    See :class:`Article.videos <zyte_common_items.Article.videos>`.
    """
