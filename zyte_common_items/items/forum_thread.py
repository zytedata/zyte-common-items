from typing import List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import ListMetadata, Topic
from zyte_common_items.converters import to_metadata_optional, url_to_str

from .social_media_post import SocialMediaPost


@attrs.define(kw_only=True)
class ForumThreadMetadata(ListMetadata):
    """Metadata class for :data:`zyte_common_items.ForumThread.metadata`."""


@attrs.define(kw_only=True)
class ForumThread(Item):
    """Represents a forum thread page."""

    url: str = attrs.field(converter=url_to_str)
    """The URL of the final response, after any redirects."""

    topic: Optional[Topic] = None
    """Topic discussed on the page."""

    threadId: Optional[str] = None
    """Thread ID."""

    posts: Optional[List[SocialMediaPost]] = None
    """List of posts available on the page, including the first or top post."""

    metadata: Optional[ForumThreadMetadata] = attrs.field(
        default=None,
        converter=to_metadata_optional(ForumThreadMetadata),
        kw_only=True,  # type: ignore[misc]
    )
    """Contains metadata about the data extraction process."""
