"""Components specific to :class:`~SocialMediaPost` item."""

import attrs

from zyte_common_items.base import Item


@attrs.define(kw_only=True)
class Reactions(Item):
    """Details of reactions to a post."""

    replies: int | None = None
    """Number of times the post received a reply."""

    reposts: int | None = None
    """Number of times the post has been shared."""

    likes: int | None = None
    """Number of likes or other positive reactions to the post."""

    dislikes: int | None = None
    """Number of dislikes or other negative reactions to the post."""


@attrs.define(kw_only=True)
class SocialMediaPostAuthor(Item):
    """Details of the author of a social media post."""

    numberOfFollowers: int | None = None
    """The number of the followers that observe the author."""

    numberOfFollowing: int | None = None
    """The number of the users that the author follows."""

    dateAccountCreated: str | None = None
    """The date of the creation of the author's account."""

    location: str | None = None
    """The location of the author, if it's available in the author profile.

    Country or city location only.
    """

    isVerified: bool | None = None
    """Indication if the author's account is verified."""
