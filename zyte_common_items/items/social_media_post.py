from typing import List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    Reactions,
    SearchMetadata,
    SocialMediaPostAuthor,
    Url,
)
from zyte_common_items.converters import to_metadata_optional, url_to_str_optional


@attrs.define(kw_only=True)
class SocialMediaPostMetadata(SearchMetadata):
    """Metadata class for :data:`zyte_common_items.SocialMediaPost.metadata`."""


@attrs.define(kw_only=True)
class SocialMediaPost(Item):
    """Represents a single social media post."""

    url: str = attrs.field(converter=url_to_str_optional)
    """The URL of the final response, after any redirects."""

    postId: Optional[str] = None
    """The identifier of the post."""

    reactions: Optional[Reactions] = None
    """Details of reactions to the post."""

    text: Optional[str] = None
    """The text content of the post."""

    datePublished: Optional[str] = None
    """The timestamp at which the post was created.

    Format: Timezone: UTC. ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"
    """

    hashtags: Optional[List[str]] = None
    """The list of hashtags contained in the post."""

    mediaUrls: Optional[List[Url]] = None
    """The list of URLs of media files (images, videos, etc.) linked from the
    post."""

    author: Optional[SocialMediaPostAuthor] = None
    """Details of the author of the post.

    No easily identifiable information can be contained in here, such as
    usernames.
    """

    metadata: Optional[SocialMediaPostMetadata] = attrs.field(
        default=None,
        converter=to_metadata_optional(SocialMediaPostMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Contains metadata about the data extraction process."""
