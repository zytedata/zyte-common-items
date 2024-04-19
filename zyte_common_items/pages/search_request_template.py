from web_poet import ItemPage

from zyte_common_items.items import SearchRequestTemplate, SearchRequestTemplateMetadata

from .mixins import HasMetadata


class SearchRequestTemplatePage(
    ItemPage[SearchRequestTemplate], HasMetadata[SearchRequestTemplateMetadata]
):
    pass
