from web_poet import Returns

from zyte_common_items.items import SearchRequestTemplate, SearchRequestTemplateMetadata

from .base import BasePage, Page
from .mixins import HasMetadata


class BaseSearchRequestTemplatePage(
    BasePage, Returns[SearchRequestTemplate], HasMetadata[SearchRequestTemplateMetadata]
):
    """:class:`BasePage` subclass for :class:`SearchRequestTemplate`."""


class SearchRequestTemplatePage(
    Page, Returns[SearchRequestTemplate], HasMetadata[SearchRequestTemplateMetadata]
):
    """:class:`Page` subclass for :class:`SearchRequestTemplate`."""
