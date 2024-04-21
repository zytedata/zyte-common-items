from typing import List, Optional

import attrs
from web_poet import Returns, field

from zyte_common_items.components import ProbabilityRequest, Request
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

    @field
    def categoryName(self) -> Optional[str]:
        return self.product_navigation.categoryName

    @field
    def items(self) -> Optional[List[ProbabilityRequest]]:
        return self.product_navigation.items

    @field
    def metadata(self) -> Optional[ProductNavigationMetadata]:
        return self.product_navigation.metadata

    @field
    def nextPage(self) -> Optional[Request]:
        return self.product_navigation.nextPage

    @field
    def pageNumber(self) -> Optional[int]:
        return self.product_navigation.pageNumber

    @field
    def subCategories(self) -> Optional[List[ProbabilityRequest]]:
        return self.product_navigation.subCategories

    @field
    def url(self) -> Optional[str]:
        return self.product_navigation.url
