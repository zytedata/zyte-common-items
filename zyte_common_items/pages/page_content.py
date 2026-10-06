import attrs
from web_poet import Returns

from zyte_common_items.components import Breadcrumb, NamedLink, Request
from zyte_common_items.fields import auto_field
from zyte_common_items.items import PageContent, PageContentMetadata

from .base import BasePage, Page
from .mixins import HasMetadata


class BasePageContentPage(
    BasePage, Returns[PageContent], HasMetadata[PageContentMetadata]
):
    """:class:`BasePage` subclass for :class:`PageContent`."""


class PageContentPage(Page, Returns[PageContent], HasMetadata[PageContentMetadata]):
    """:class:`Page` subclass for :class:`PageContent`."""


@attrs.define
class AutoPageContentPage(BasePageContentPage):
    page_content: PageContent

    @auto_field
    def breadcrumbs(self) -> list[Breadcrumb] | None:
        return self.page_content.breadcrumbs

    @auto_field
    def canonicalUrl(self) -> str | None:
        return self.page_content.canonicalUrl

    @auto_field
    def headline(self) -> str | None:
        return self.page_content.headline

    @auto_field
    def itemMain(self) -> str | None:
        return self.page_content.itemMain

    @auto_field
    def itemMainXPath(self) -> str | None:
        return self.page_content.itemMainXPath

    @auto_field
    def metadata(self) -> PageContentMetadata | None:
        return self.page_content.metadata

    @auto_field
    def navigationFooter(self) -> list[NamedLink] | None:
        return self.page_content.navigationFooter

    @auto_field
    def navigationHeader(self) -> list[NamedLink] | None:
        return self.page_content.navigationHeader

    @auto_field
    def navigationSidebar(self) -> list[NamedLink] | None:
        return self.page_content.navigationSidebar

    @auto_field
    def nextPage(self) -> Request | None:
        return self.page_content.nextPage

    @auto_field
    def pagination(self) -> list[NamedLink] | None:
        return self.page_content.pagination

    @auto_field
    def title(self) -> str | None:
        return self.page_content.title

    @auto_field
    def url(self) -> str | None:
        return self.page_content.url
