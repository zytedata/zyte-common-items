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

    postId: str | None = None
    """The identifier of the post."""

    reactions: Reactions | None = None
    """Details of reactions to the post."""

    text: str | None = None
    """The text content of the post."""

    datePublished: str | None = None
    """The timestamp at which the post was created.

    Format: Timezone: UTC. ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"
    """

    hashtags: list[str] | None = None
    """The list of hashtags contained in the post."""

    mediaUrls: list[Url] | None = None
    """The list of URLs of media files (images, videos, etc.) linked from the
    post."""

    author: SocialMediaPostAuthor | None = None
    """Details of the author of the post.

    No easily identifiable information can be contained in here, such as
    usernames.
    """

    metadata: SocialMediaPostMetadata | None = attrs.field(
        default=None,
        converter=to_metadata_optional(SocialMediaPostMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Contains metadata about the data extraction process."""
