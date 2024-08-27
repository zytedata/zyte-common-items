from typing import List, Optional

import attrs
from web_poet import Returns

from zyte_common_items.components import Audio, Author, Breadcrumb, Image, Video
from zyte_common_items.fields import auto_field
from zyte_common_items.items import Article, ArticleMetadata
from zyte_common_items.processors import breadcrumbs_processor, images_processor

from .base import BasePage, Page
from .mixins import HasMetadata


class BaseArticlePage(BasePage, Returns[Article], HasMetadata[ArticleMetadata]):
    """:class:`BasePage` subclass for :class:`Article`."""

    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]
        images = [images_processor]


class ArticlePage(Page, Returns[Article], HasMetadata[ArticleMetadata]):
    """:class:`Page` subclass for :class:`Article`."""

    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]
        images = [images_processor]


@attrs.define
class AutoArticlePage(BaseArticlePage):
    article: Article

    @auto_field
    def headline(self) -> Optional[str]:
        return self.article.headline

    @auto_field
    def datePublished(self) -> Optional[str]:
        return self.article.datePublished

    @auto_field
    def datePublishedRaw(self) -> Optional[str]:
        return self.article.datePublishedRaw

    @auto_field
    def dateModified(self) -> Optional[str]:
        return self.article.dateModified

    @auto_field
    def dateModifiedRaw(self) -> Optional[str]:
        return self.article.dateModifiedRaw

    @auto_field
    def authors(self) -> Optional[List[Author]]:
        return self.article.authors

    @auto_field
    def breadcrumbs(self) -> Optional[List[Breadcrumb]]:
        return self.article.breadcrumbs

    @auto_field
    def inLanguage(self) -> Optional[str]:
        return self.article.inLanguage

    @auto_field
    def mainImage(self) -> Optional[Image]:
        return self.article.mainImage

    @auto_field
    def images(self) -> Optional[List[Image]]:
        return self.article.images

    @auto_field
    def description(self) -> Optional[str]:
        return self.article.description

    @auto_field
    def articleBody(self) -> Optional[str]:
        return self.article.articleBody

    @auto_field
    def articleBodyHtml(self) -> Optional[str]:
        return self.article.articleBodyHtml

    @auto_field
    def videos(self) -> Optional[List[Video]]:
        return self.article.videos

    @auto_field
    def audios(self) -> Optional[List[Audio]]:
        return self.article.audios

    @auto_field
    def canonicalUrl(self) -> Optional[str]:
        return self.article.canonicalUrl

    @auto_field
    def url(self) -> Optional[str]:
        return self.article.url

    @auto_field
    def metadata(self) -> Optional[ArticleMetadata]:
        return self.article.metadata
