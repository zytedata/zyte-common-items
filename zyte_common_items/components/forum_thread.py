from __future__ import annotations

from typing import Optional

import attrs

from zyte_common_items.base import Item


@attrs.define(kw_only=True)
class Reactions(Item):
    """Details of reactions to a forum thread post."""

    #: Publication date of the post.
    #:
    #: Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ" or
    #: "YYYY-MM-DDThh:mm:ss±zz:zz".
    #:
    #: With timezone, if available.
    datePublished: Optional[str] = None

    #: Same date as
    #: :attr:`~zyte_common_items.Post.datePublished`, but
    #: :before parsing/normalization, i.e. as it appears on the website.
    datePublishedRaw: Optional[str] = None

    #: Text of the post.
    text: Optional[str] = None


@attrs.define(kw_only=True)
class Post(Item):
    """Post available on a forum thread page."""

    #: Publication date of the post.
    #:
    #: Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ" or
    #: "YYYY-MM-DDThh:mm:ss±zz:zz".
    #:
    #: With timezone, if available.
    datePublished: Optional[str] = None

    #: Same date as
    #: :attr:`~zyte_common_items.Post.datePublished`, but
    #: :before parsing/normalization, i.e. as it appears on the website.
    datePublishedRaw: Optional[str] = None

    #: Text of the post.
    text: Optional[str] = None


@attrs.define(kw_only=True)
class Topic(Item):
    """Topic that is discussed on the page."""

    #: Name of the topic.
    name: str
