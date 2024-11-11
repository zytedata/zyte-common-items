from typing import List, Optional

import attrs
from web_poet import Returns

from zyte_common_items.components import Topic
from zyte_common_items.fields import auto_field
from zyte_common_items.items import ForumThread, ForumThreadMetadata, SocialMediaPost

from .base import BasePage, Page
from .mixins import HasMetadata


class BaseForumThreadPage(
    BasePage, Returns[ForumThread], HasMetadata[ForumThreadMetadata]
):
    """:class:`BasePage` subclass for :class:`ForumThread`."""


class ForumThreadPage(Page, Returns[ForumThread], HasMetadata[ForumThreadMetadata]):
    """:class:`Page` subclass for :class:`ForumThread`."""


@attrs.define
class AutoForumThreadPage(BaseForumThreadPage):
    forum_thread: ForumThread

    @auto_field
    def url(self) -> Optional[str]:
        return self.forum_thread.url

    @auto_field
    def threadId(self) -> Optional[str]:
        return self.forum_thread.threadId

    @auto_field
    def topic(self) -> Optional[Topic]:
        return self.forum_thread.topic

    @auto_field
    def posts(self) -> Optional[List[SocialMediaPost]]:
        return self.forum_thread.posts

    @auto_field
    def metadata(self) -> Optional[ForumThreadMetadata]:
        return self.forum_thread.metadata
