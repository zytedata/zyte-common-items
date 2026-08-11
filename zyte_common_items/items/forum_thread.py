import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import ListMetadata, Topic
from zyte_common_items.converters import to_metadata_optional, url_to_str_optional

from .social_media_post import SocialMediaPost


@attrs.define(kw_only=True)
class ForumThreadMetadata(ListMetadata):
    """Metadata class for :data:`zyte_common_items.ForumThread.metadata`."""


@attrs.define(kw_only=True)
class ForumThread(Item):
    """Represents a forum thread page."""

    url: str = attrs.field(converter=url_to_str_optional)
    """The URL of the final response, after any redirects."""

    topic: Topic | None = None
    """Topic discussed on the page."""

    threadId: str | None = None
    """Thread ID."""

    posts: list[SocialMediaPost] | None = None
    """List of posts available on the page, including the first or top post."""

    metadata: ForumThreadMetadata | None = attrs.field(
        default=None,
        converter=to_metadata_optional(ForumThreadMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Contains metadata about the data extraction process."""
