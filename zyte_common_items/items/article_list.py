from __future__ import annotations

from typing import List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    Author,
    Breadcrumb,
    Image,
    ListMetadata,
    ProbabilityMetadata,
)
from zyte_common_items.converters import (
    to_metadata_optional,
    url_to_str,
    url_to_str_optional,
)


@attrs.define(kw_only=True)
class ArticleListMetadata(ListMetadata):
    """Metadata class for :data:`zyte_common_items.ArticleList.metadata`."""


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
        default=None, converter=url_to_str_optional, kw_only=True
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
        default=None, converter=to_metadata_optional(ArticleListMetadata), kw_only=True  # type: ignore[misc]
    )


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
        default=None,
        converter=to_metadata_optional(ProbabilityMetadata),  # type: ignore[misc]
        kw_only=True,
    )

    #: Main URL.
    url: Optional[str] = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
