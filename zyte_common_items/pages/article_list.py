from typing import List, Optional

import attrs
from web_poet import Returns, field

from zyte_common_items.components import Breadcrumb
from zyte_common_items.items import ArticleFromList, ArticleList, ArticleListMetadata
from zyte_common_items.processors import breadcrumbs_processor

from .base import BasePage, Page
from .mixins import HasMetadata


class BaseArticleListPage(
    BasePage, Returns[ArticleList], HasMetadata[ArticleListMetadata]
):
    """:class:`BasePage` subclass for :class:`ArticleList`."""

    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]


class ArticleListPage(Page, Returns[ArticleList], HasMetadata[ArticleListMetadata]):
    """:class:`Page` subclass for :class:`ArticleList`."""

    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]


@attrs.define
class AutoArticleListPage(BaseArticleListPage):
    article_list: ArticleList

    @field
    def articles(self) -> Optional[List[ArticleFromList]]:
        return self.article_list.articles

    @field
    def breadcrumbs(self) -> Optional[List[Breadcrumb]]:
        return self.article_list.breadcrumbs

    @field
    def canonicalUrl(self) -> Optional[str]:
        return self.article_list.canonicalUrl

    @field
    def metadata(self) -> Optional[ArticleListMetadata]:
        return self.article_list.metadata

    @field
    def url(self) -> Optional[str]:
        return self.article_list.url
