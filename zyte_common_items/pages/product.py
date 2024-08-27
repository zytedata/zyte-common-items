from typing import List, Optional

import attrs
from web_poet import Returns

from zyte_common_items.components import (
    AdditionalProperty,
    AggregateRating,
    Brand,
    Breadcrumb,
    Gtin,
    Image,
)
from zyte_common_items.fields import auto_field
from zyte_common_items.items import Product, ProductMetadata, ProductVariant
from zyte_common_items.processors import (
    brand_processor,
    breadcrumbs_processor,
    description_html_processor,
    description_processor,
    gtin_processor,
    images_processor,
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
        images = [images_processor]


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
        images = [images_processor]


@attrs.define
class AutoProductPage(BaseProductPage):
    product: Product

    @auto_field
    def additionalProperties(self) -> Optional[List[AdditionalProperty]]:
        return self.product.additionalProperties

    @auto_field
    def aggregateRating(self) -> Optional[AggregateRating]:
        return self.product.aggregateRating

    @auto_field
    def availability(self) -> Optional[str]:
        return self.product.availability

    @auto_field
    def brand(self) -> Optional[Brand]:
        return self.product.brand

    @auto_field
    def breadcrumbs(self) -> Optional[List[Breadcrumb]]:
        return self.product.breadcrumbs

    @auto_field
    def canonicalUrl(self) -> Optional[str]:
        return self.product.canonicalUrl

    @auto_field
    def color(self) -> Optional[str]:
        return self.product.color

    @auto_field
    def currency(self) -> Optional[str]:
        return self.product.currency

    @auto_field
    def currencyRaw(self) -> Optional[str]:
        return self.product.currencyRaw

    @auto_field
    def description(self) -> Optional[str]:
        return self.product.description

    @auto_field
    def descriptionHtml(self) -> Optional[str]:
        return self.product.descriptionHtml

    @auto_field
    def features(self) -> Optional[List[str]]:
        return self.product.features

    @auto_field
    def gtin(self) -> Optional[List[Gtin]]:
        return self.product.gtin

    @auto_field
    def images(self) -> Optional[List[Image]]:
        return self.product.images

    @auto_field
    def mainImage(self) -> Optional[Image]:
        return self.product.mainImage

    @auto_field
    def metadata(self) -> Optional[ProductMetadata]:
        return self.product.metadata

    @auto_field
    def mpn(self) -> Optional[str]:
        return self.product.mpn

    @auto_field
    def name(self) -> Optional[str]:
        return self.product.name

    @auto_field
    def price(self) -> Optional[str]:
        return self.product.price

    @auto_field
    def productId(self) -> Optional[str]:
        return self.product.productId

    @auto_field
    def regularPrice(self) -> Optional[str]:
        return self.product.regularPrice

    @auto_field
    def size(self) -> Optional[str]:
        return self.product.size

    @auto_field
    def sku(self) -> Optional[str]:
        return self.product.sku

    @auto_field
    def style(self) -> Optional[str]:
        return self.product.style

    @auto_field
    def url(self) -> str:
        return self.product.url

    @auto_field
    def variants(self) -> Optional[List[ProductVariant]]:
        return self.product.variants
