from typing import List, Optional

import attrs
from web_poet import Returns, field

from zyte_common_items.components import Reactions, SocialMediaPostAuthor, Url
from zyte_common_items.items import SocialMediaPost, SocialMediaPostMetadata

from .base import BasePage, Page
from .mixins import HasMetadata


class BaseSocialMediaPostPage(
    BasePage, Returns[SocialMediaPost], HasMetadata[SocialMediaPostMetadata]
):
    pass


class SocialMediaPostPage(
    Page, Returns[SocialMediaPost], HasMetadata[SocialMediaPostMetadata]
):
    pass


@attrs.define
class AutoSocialMediaPostPage(BaseSocialMediaPostPage):
    social_media_post: SocialMediaPost

    @field
    def url(self) -> Optional[str]:
        return self.social_media_post.url

    @field
    def postId(self) -> Optional[str]:
        return self.social_media_post.postId

    @field
    def reactions(self) -> Optional[Reactions]:
        return self.social_media_post.reactions

    @field
    def text(self) -> Optional[str]:
        return self.social_media_post.text

    @field
    def datePublished(self) -> Optional[str]:
        return self.social_media_post.datePublished

    @field
    def hashtags(self) -> Optional[List[str]]:
        return self.social_media_post.hashtags

    @field
    def mediaUrls(self) -> Optional[List[Url]]:
        return self.social_media_post.mediaUrls

    @field
    def author(self) -> Optional[SocialMediaPostAuthor]:
        return self.social_media_post.author

    @field
    def metadata(self) -> Optional[SocialMediaPostMetadata]:
        return self.social_media_post.metadata
