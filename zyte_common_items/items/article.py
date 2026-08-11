import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    Audio,
    Author,
    Breadcrumb,
    DetailsMetadata,
    Image,
    Video,
)
from zyte_common_items.converters import to_metadata_optional, url_to_str_optional


@attrs.define(kw_only=True)
class ArticleMetadata(DetailsMetadata):
    """Metadata class for :data:`zyte_common_items.Article.metadata`."""


@attrs.define(kw_only=True)
class Article(Item):
    """Article, typically seen on online news websites, blogs, or announcement
    sections.

    :attr:`url` is the only required attribute.
    """

    headline: str | None = None
    """Headline or title."""

    datePublished: str | None = None
    """Publication date of the article.

    Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ" or
    "YYYY-MM-DDThh:mm:ss±zz:zz".

    With timezone, if available.

    If the actual publication date is not found, the value of
    :attr:`~zyte_common_items.Article.dateModified` is used instead.
    """

    datePublishedRaw: str | None = None
    """Same date as :attr:`~zyte_common_items.Article.datePublished`, but
    before parsing/normalization, i.e. as it appears on the website."""

    dateModified: str | None = None
    """Date when the article was most recently modified.

    Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ" or
    "YYYY-MM-DDThh:mm:ss±zz:zz".

    With timezone, if available.
    """

    dateModifiedRaw: str | None = None
    """Same date as :attr:`~zyte_common_items.Article.dateModified`, but before
    parsing/normalization, i.e. as it appears on the website."""

    authors: list[Author] | None = None
    """All authors of the article."""

    breadcrumbs: list[Breadcrumb] | None = None
    """Webpage `breadcrumb trail`_.

    .. _Breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    """

    inLanguage: str | None = None
    """Language of the article, as an ISO 639-1 language code.

    Sometimes the article language is not the same as the web page overall
    language.
    """

    mainImage: Image | None = None
    """Main image."""

    images: list[Image] | None = None
    """All images."""

    description: str | None = None
    """A short summary of the article.

    It can be either human-provided (if available), or auto-generated.
    """

    articleBody: str | None = None
    """Clean text of the article, including sub-headings, with newline
    separators.

    Format:

    - trimmed (no whitespace at the beginning or the end of the body string),
    - line breaks included,
    - no length limit,
    - no normalization of Unicode characters.
    """

    articleBodyHtml: str | None = None
    """Simplified and standardized HTML of the article, including sub-headings,
    image captions and embedded content (videos, tweets, etc.).

    Format: HTML string normalized in a consistent way.
    """

    videos: list[Video] | None = None
    """All videos."""

    audios: list[Audio] | None = None
    """All audios."""

    canonicalUrl: str | None = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
    """Canonical form of the URL, as indicated by the website.

    See also ``url``.
    """

    url: str = attrs.field(converter=url_to_str_optional)
    """The main URL of the article page.

    The URL of the final response, after any redirects.

    Required attribute.

    In case there is no article data on the page or the page was not reached,
    the returned "empty" item would still contain this URL field.
    """

    metadata: ArticleMetadata | None = attrs.field(
        default=None,
        converter=to_metadata_optional(ArticleMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Data extraction process metadata."""
