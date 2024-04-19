from typing import List, Optional

import attrs
from web_poet import Returns, field

from zyte_common_items.components import ProbabilityRequest, Request
from zyte_common_items.items import ArticleNavigation, ArticleNavigationMetadata

from .base import BasePage, Page
from .mixins import HasMetadata


class BaseArticleNavigationPage(
    BasePage, Returns[ArticleNavigation], HasMetadata[ArticleNavigationMetadata]
):
    """:class:`BasePage` subclass for :class:`ArticleNavigation`."""


class ArticleNavigationPage(
    Page, Returns[ArticleNavigation], HasMetadata[ArticleNavigationMetadata]
):
    """:class:`Page` subclass for :class:`ArticleNavigation`."""


@attrs.define
class AutoArticleNavigationPage(BaseArticleNavigationPage):
    article_navigation: ArticleNavigation

    @field
    def categoryName(self) -> Optional[str]:
        return self.article_navigation.categoryName

    @field
    def items(self) -> Optional[List[ProbabilityRequest]]:
        return self.article_navigation.items

    @field
    def metadata(self) -> Optional[ArticleNavigationMetadata]:
        return self.article_navigation.metadata

    @field
    def nextPage(self) -> Optional[Request]:
        return self.article_navigation.nextPage

    @field
    def pageNumber(self) -> Optional[int]:
        return self.article_navigation.pageNumber

    @field
    def subCategories(self) -> Optional[List[ProbabilityRequest]]:
        return self.article_navigation.subCategories

    @field
    def url(self) -> Optional[str]:
        return self.article_navigation.url
