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
    def headline(self) -> str | None:
        return self.article.headline

    @auto_field
    def datePublished(self) -> str | None:
        return self.article.datePublished

    @auto_field
    def datePublishedRaw(self) -> str | None:
        return self.article.datePublishedRaw

    @auto_field
    def dateModified(self) -> str | None:
        return self.article.dateModified

    @auto_field
    def dateModifiedRaw(self) -> str | None:
        return self.article.dateModifiedRaw

    @auto_field
    def authors(self) -> list[Author] | None:
        return self.article.authors

    @auto_field
    def breadcrumbs(self) -> list[Breadcrumb] | None:
        return self.article.breadcrumbs

    @auto_field
    def inLanguage(self) -> str | None:
        return self.article.inLanguage

    @auto_field
    def mainImage(self) -> Image | None:
        return self.article.mainImage

    @auto_field
    def images(self) -> list[Image] | None:
        return self.article.images

    @auto_field
    def description(self) -> str | None:
        return self.article.description

    @auto_field
    def articleBody(self) -> str | None:
        return self.article.articleBody

    @auto_field
    def articleBodyHtml(self) -> str | None:
        return self.article.articleBodyHtml

    @auto_field
    def videos(self) -> list[Video] | None:
        return self.article.videos

    @auto_field
    def audios(self) -> list[Audio] | None:
        return self.article.audios

    @auto_field
    def canonicalUrl(self) -> str | None:
        return self.article.canonicalUrl

    @auto_field
    def url(self) -> str | None:
        return self.article.url

    @auto_field
    def metadata(self) -> ArticleMetadata | None:
        return self.article.metadata
