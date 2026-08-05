from typing import List, Optional

import attrs
from web_poet import Returns

from zyte_common_items.components import ProbabilityRequest, Request
from zyte_common_items.fields import auto_field
from zyte_common_items.items import ProductNavigation, ProductNavigationMetadata
from zyte_common_items.processors import probability_request_list_processor

from .base import BasePage, Page
from .mixins import HasMetadata


class BaseProductNavigationPage(
    BasePage, Returns[ProductNavigation], HasMetadata[ProductNavigationMetadata]
):
    """:class:`BasePage` subclass for :class:`ProductNavigation`."""

    class Processors(BasePage.Processors):
        subCategories = [probability_request_list_processor]
        items = [probability_request_list_processor]


class ProductNavigationPage(
    Page, Returns[ProductNavigation], HasMetadata[ProductNavigationMetadata]
):
    """:class:`Page` subclass for :class:`ProductNavigation`."""


@attrs.define
class AutoProductNavigationPage(BaseProductNavigationPage):
    product_navigation: ProductNavigation

    @auto_field
    def categoryName(self) -> Optional[str]:
        return self.product_navigation.categoryName

    @auto_field
    def items(self) -> Optional[List[ProbabilityRequest]]:
        return self.product_navigation.items

    @auto_field
    def metadata(self) -> Optional[ProductNavigationMetadata]:
        return self.product_navigation.metadata

    @auto_field
    def nextPage(self) -> Optional[Request]:
        return self.product_navigation.nextPage

    @auto_field
    def pageNumber(self) -> Optional[int]:
        return self.product_navigation.pageNumber

    @auto_field
    def subCategories(self) -> Optional[List[ProbabilityRequest]]:
        return self.product_navigation.subCategories

    @auto_field
    def url(self) -> Optional[str]:
        return self.product_navigation.url
