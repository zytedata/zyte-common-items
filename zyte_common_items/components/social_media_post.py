"""
Components specific to :class:`~SocialMediaPost` item.
"""

from typing import Optional

import attrs

from zyte_common_items.base import Item


@attrs.define(kw_only=True)
class Reactions(Item):
    """Details of reactions to a post."""

    #: Number of times the post has been shared.
    reposts: Optional[int] = None

    #: Number of likes or other positive reactions to the post.
    likes: Optional[int] = None

    #: Number of dislikes or other negative reactions to the post.
    dislikes: Optional[int] = None


@attrs.define(kw_only=True)
class SocialMediaPostAuthor(Item):
    """Details of the author of a social media post."""

    #: The number of the followers that observe the author.
    numberOfFollowers: Optional[int] = None

    #: The number of the users that the author follows.
    numberOfFollowing: Optional[int] = None

    #: The date of the creation of the author's account.
    dateAccountCreated: Optional[str] = None

    #: The location of the author, if it's available in the author profile. Country or city location only.
    location: Optional[str] = None

    #: Indication if the author's account is verified.
    isVerified: Optional[bool] = None
