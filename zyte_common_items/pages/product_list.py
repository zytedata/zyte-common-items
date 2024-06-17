from typing import List, Optional

import attrs
from web_poet import Returns

from zyte_common_items.components import Breadcrumb, Link
from zyte_common_items.fields import auto_field
from zyte_common_items.items import ProductFromList, ProductList, ProductListMetadata
from zyte_common_items.processors import breadcrumbs_processor

from .base import BasePage, Page
from .mixins import HasMetadata


class BaseProductListPage(
    BasePage, Returns[ProductList], HasMetadata[ProductListMetadata]
):
    """:class:`BasePage` subclass for :class:`ProductList`."""

    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]


class ProductListPage(Page, Returns[ProductList], HasMetadata[ProductListMetadata]):
    """:class:`Page` subclass for :class:`ProductList`."""

    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]


@attrs.define
class AutoProductListPage(BaseProductListPage):
    product_list: ProductList

    @auto_field
    def breadcrumbs(self) -> Optional[List[Breadcrumb]]:
        return self.product_list.breadcrumbs

    @auto_field
    def canonicalUrl(self) -> Optional[str]:
        return self.product_list.canonicalUrl

    @auto_field
    def categoryName(self) -> Optional[str]:
        return self.product_list.categoryName

    @auto_field
    def metadata(self) -> Optional[ProductListMetadata]:
        return self.product_list.metadata

    @auto_field
    def pageNumber(self) -> Optional[int]:
        return self.product_list.pageNumber

    @auto_field
    def paginationNext(self) -> Optional[Link]:
        return self.product_list.paginationNext

    @auto_field
    def products(self) -> Optional[List[ProductFromList]]:
        return self.product_list.products

    @auto_field
    def url(self) -> Optional[str]:
        return self.product_list.url
