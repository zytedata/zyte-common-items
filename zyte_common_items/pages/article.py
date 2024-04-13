from typing import List, Optional

import attrs
from web_poet import Returns, field

from zyte_common_items.components import Audio, Author, Breadcrumb, Image, Video
from zyte_common_items.items import Article, ArticleMetadata
from zyte_common_items.processors import breadcrumbs_processor

from .base import BasePage, Page
from .mixins import HasMetadata


class BaseArticlePage(BasePage, Returns[Article], HasMetadata[ArticleMetadata]):
    """:class:`BasePage` subclass for :class:`Article`."""

    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]


class ArticlePage(Page, Returns[Article], HasMetadata[ArticleMetadata]):
    """:class:`Page` subclass for :class:`Article`."""

    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]


@attrs.define
class AutoArticlePage(BaseArticlePage):
    article: Article

    @field
    def headline(self) -> Optional[str]:
        return self.article.headline

    @field
    def datePublished(self) -> Optional[str]:
        return self.article.datePublished

    @field
    def datePublishedRaw(self) -> Optional[str]:
        return self.article.datePublishedRaw

    @field
    def dateModified(self) -> Optional[str]:
        return self.article.dateModified

    @field
    def dateModifiedRaw(self) -> Optional[str]:
        return self.article.dateModifiedRaw

    @field
    def authors(self) -> Optional[List[Author]]:
        return self.article.authors

    @field
    def breadcrumbs(self) -> Optional[List[Breadcrumb]]:
        return self.article.breadcrumbs

    @field
    def inLanguage(self) -> Optional[str]:
        return self.article.inLanguage

    @field
    def mainImage(self) -> Optional[Image]:
        return self.article.mainImage

    @field
    def images(self) -> Optional[List[Image]]:
        return self.article.images

    @field
    def description(self) -> Optional[str]:
        return self.article.description

    @field
    def articleBody(self) -> Optional[str]:
        return self.article.articleBody

    @field
    def articleBodyHtml(self) -> Optional[str]:
        return self.article.articleBodyHtml

    @field
    def videos(self) -> Optional[List[Video]]:
        return self.article.videos

    @field
    def audios(self) -> Optional[List[Audio]]:
        return self.article.audios

    @field
    def canonicalUrl(self) -> Optional[str]:
        return self.article.canonicalUrl

    @field
    def url(self) -> Optional[str]:
        return self.article.url

    @field
    def metadata(self) -> Optional[ArticleMetadata]:
        return self.article.metadata
