from typing import List, Optional

import attrs
from web_poet import Returns, field

from zyte_common_items.components import (
    AdditionalProperty,
    AggregateRating,
    Brand,
    Breadcrumb,
    Gtin,
    Image,
)
from zyte_common_items.items import Product, ProductMetadata, ProductVariant
from zyte_common_items.processors import (
    brand_processor,
    breadcrumbs_processor,
    description_html_processor,
    description_processor,
    gtin_processor,
    price_processor,
    rating_processor,
    simple_price_processor,
)

from .base import BasePage, Page
from .mixins import DescriptionMixin, HasMetadata, PriceMixin


class BaseProductPage(
    BasePage,
    DescriptionMixin,
    PriceMixin,
    Returns[Product],
    HasMetadata[ProductMetadata],
):
    """:class:`BasePage` subclass for :class:`Product`."""

    class Processors(BasePage.Processors):
        aggregateRating = [rating_processor]
        brand = [brand_processor]
        breadcrumbs = [breadcrumbs_processor]
        description = [description_processor]
        descriptionHtml = [description_html_processor]
        gtin = [gtin_processor]
        price = [price_processor]
        regularPrice = [simple_price_processor]


class ProductPage(
    Page, DescriptionMixin, PriceMixin, Returns[Product], HasMetadata[ProductMetadata]
):
    """:class:`Page` subclass for :class:`Product`."""

    class Processors(Page.Processors):
        aggregateRating = [rating_processor]
        brand = [brand_processor]
        breadcrumbs = [breadcrumbs_processor]
        description = [description_processor]
        descriptionHtml = [description_html_processor]
        gtin = [gtin_processor]
        price = [price_processor]
        regularPrice = [simple_price_processor]


@attrs.define
class AutoProductPage(BaseProductPage):
    product: Product

    @field
    def additionalProperties(self) -> Optional[List[AdditionalProperty]]:
        return self.product.additionalProperties

    @field
    def aggregateRating(self) -> Optional[AggregateRating]:
        return self.product.aggregateRating

    @field
    def availability(self) -> Optional[str]:
        return self.product.availability

    @field
    def brand(self) -> Optional[Brand]:
        return self.product.brand

    @field
    def breadcrumbs(self) -> Optional[List[Breadcrumb]]:
        return self.product.breadcrumbs

    @field
    def canonicalUrl(self) -> Optional[str]:
        return self.product.canonicalUrl

    @field
    def color(self) -> Optional[str]:
        return self.product.color

    @field
    def currency(self) -> Optional[str]:
        return self.product.currency

    @field
    def currencyRaw(self) -> Optional[str]:
        return self.product.currencyRaw

    @field
    def description(self) -> Optional[str]:
        return self.product.description

    @field
    def descriptionHtml(self) -> Optional[str]:
        return self.product.descriptionHtml

    @field
    def features(self) -> Optional[List[str]]:
        return self.product.features

    @field
    def gtin(self) -> Optional[List[Gtin]]:
        return self.product.gtin

    @field
    def images(self) -> Optional[List[Image]]:
        return self.product.images

    @field
    def mainImage(self) -> Optional[Image]:
        return self.product.mainImage

    @field
    def metadata(self) -> Optional[ProductMetadata]:
        return self.product.metadata

    @field
    def mpn(self) -> Optional[str]:
        return self.product.mpn

    @field
    def name(self) -> Optional[str]:
        return self.product.name

    @field
    def price(self) -> Optional[str]:
        return self.product.price

    @field
    def productId(self) -> Optional[str]:
        return self.product.productId

    @field
    def regularPrice(self) -> Optional[str]:
        return self.product.regularPrice

    @field
    def size(self) -> Optional[str]:
        return self.product.size

    @field
    def sku(self) -> Optional[str]:
        return self.product.sku

    @field
    def style(self) -> Optional[str]:
        return self.product.style

    @field
    def url(self) -> str:
        return self.product.url

    @field
    def variants(self) -> Optional[List[ProductVariant]]:
        return self.product.variants
