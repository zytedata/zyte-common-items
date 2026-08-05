from web_poet import Returns

from zyte_common_items.items import SearchRequestTemplate, SearchRequestTemplateMetadata

from .base import BasePage, Page
from .mixins import HasMetadata


class _SearchRequestTemplateProcessors:
    # Whitespace is part of the request body, so it must be preserved.
    body: list = []


class BaseSearchRequestTemplatePage(
    BasePage, Returns[SearchRequestTemplate], HasMetadata[SearchRequestTemplateMetadata]
):
    """:class:`BasePage` subclass for :class:`SearchRequestTemplate`."""

    class Processors(_SearchRequestTemplateProcessors, BasePage.Processors):
        pass


class SearchRequestTemplatePage(
    Page, Returns[SearchRequestTemplate], HasMetadata[SearchRequestTemplateMetadata]
):
    """:class:`Page` subclass for :class:`SearchRequestTemplate`."""

    class Processors(_SearchRequestTemplateProcessors, Page.Processors):
        pass
