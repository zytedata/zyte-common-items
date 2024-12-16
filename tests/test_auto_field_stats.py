from collections import defaultdict
from copy import copy
from typing import Any, Callable, Optional, Sequence, Set

import pytest

pytest.importorskip("scrapy_poet")

import attrs
from itemadapter import ItemAdapter
from pytest_twisted import ensureDeferred
from scrapy import Request, Spider
from scrapy.crawler import Crawler
from scrapy.statscollectors import MemoryStatsCollector
from scrapy.utils.test import get_crawler
from scrapy_poet import DummyResponse, PageObjectInputProvider
from web_poet import ItemPage, default_registry, field, handle_urls

from zyte_common_items import AutoProductPage, BaseProductPage, Item, Product
from zyte_common_items.fields import auto_field


class Provider(PageObjectInputProvider):
    name = "test"

    provided_classes = {
        Product,
    }

    async def __call__(
        self, to_provide: Set[Callable], request: Request, crawler: Crawler
    ) -> Sequence[Any]:
        return [Product(url=request.url)]


class TestSpider(Spider):
    name = "test_spider"
    start_urls = ["https://a.example"]

    def parse(self, response: DummyResponse, product: Product):
        yield product


_SETTINGS = {
    # scrapy-poet
    "DOWNLOADER_MIDDLEWARES": {
        "scrapy_poet.InjectionMiddleware": 543,
        "scrapy.downloadermiddlewares.stats.DownloaderStats": None,
        "scrapy_poet.DownloaderStatsMiddleware": 850,
    },
    "SPIDER_MIDDLEWARES": {
        "scrapy_poet.RetryMiddleware": 275,
    },
    "REQUEST_FINGERPRINTER_CLASS": "scrapy_poet.ScrapyPoetRequestFingerprinter",
    # zyte-common-items
    "ADDONS": {"zyte_common_items.Addon": 400},
    "ZYTE_COMMON_ITEMS_AUTO_FIELD_STATS": True,
    # tests
    "SCRAPY_POET_PROVIDERS": {Provider: 0},
}


async def get_auto_field_stats(settings=_SETTINGS, spider_cls=TestSpider):
    try:
        crawler = get_crawler(settings_dict=settings, spidercls=spider_cls)
        await crawler.crawl()
    finally:
        # Reset rules
        default_registry.__init__()  # type: ignore[misc]

        # Reverse add-on effects.
        ItemAdapter.ADAPTER_CLASSES = tuple(ItemAdapter.ADAPTER_CLASSES)[1:]

    return {
        k: v
        for k, v in crawler.stats.get_stats().items()
        if k.startswith("zyte_common_items/auto_fields")
    }


@ensureDeferred
async def test_not_enabled():
    settings = copy(_SETTINGS)
    del settings["ZYTE_COMMON_ITEMS_AUTO_FIELD_STATS"]
    auto_field_stats = await get_auto_field_stats(settings)
    assert auto_field_stats == {}


@ensureDeferred
async def test_no_override():
    """When requesting an item directly from a provider, without an override to
    change fields, stats reflect the entire list of item fields."""

    duplicate_stat_calls: defaultdict[str, int] = defaultdict(int)

    class OnlyOnceStatsCollector(MemoryStatsCollector):

        def track_duplicate_stat_calls(self, key):
            if key.startswith("zyte_common_items/auto_fields/") and key in self._stats:
                duplicate_stat_calls[key] += 1

        def set_value(self, key, value, spider=None):
            self.track_duplicate_stat_calls(key)
            super().set_value(key, value, spider)

        def inc_value(self, key, count=1, start=1, spider=None):
            self.track_duplicate_stat_calls(key)
            super().inc_value(key, count, start, spider)

        def max_value(self, key, value, spider=None):
            self.track_duplicate_stat_calls(key)
            super().max_value(key, value, spider)

        def min_value(self, key, value, spider=None):
            self.track_duplicate_stat_calls(key)
            super().min_value(key, value, spider)

    class TwoUrlsSpider(Spider):
        name = "test_spider"
        start_urls = ["https://a.example", "https://b.example"]

        def parse(self, response: DummyResponse, product: Product):
            yield product

    settings = {
        **_SETTINGS,
        "STATS_CLASS": OnlyOnceStatsCollector,
    }
    auto_field_stats = await get_auto_field_stats(settings, TwoUrlsSpider)
    assert auto_field_stats == {
        "zyte_common_items/auto_fields/zyte_common_items.items.product.Product": (
            "(all fields)"
        ),
    }
    assert all(value == 0 for value in duplicate_stat_calls.values())


@ensureDeferred
async def test_partial_override():
    """When requesting an item and having an Auto…Page subclass to change
    fields, stats reflect the list of item fields not defined in the
    subclass. Defined field methods are not listed, even if they return the
    original item field, directly or as a fallback."""

    class MyProductPage(AutoProductPage):

        @field
        def brand(self):
            return "foo"

        @field
        def name(self):
            return self.product.name

    handle_urls("a.example")(MyProductPage)
    auto_field_stats = await get_auto_field_stats()
    assert auto_field_stats == {
        "zyte_common_items/auto_fields/tests.test_auto_field_stats.test_partial_override.<locals>.MyProductPage": (
            "additionalProperties aggregateRating availability breadcrumbs "
            "canonicalUrl color currency currencyRaw description descriptionHtml "
            "features gtin images mainImage metadata mpn price productId "
            "regularPrice size sku style url variants"
        ),
    }


@ensureDeferred
async def test_full_override():
    """When requesting an item and having an Auto…Page subclass to change
    all fields, stats reflect the list of non-overriden item fields as an empty
    string."""

    # Copy-paste of fields from the AutoProductPage implementation, with type
    # hints removed.
    class MyProductPage(AutoProductPage):

        @field
        def additionalProperties(self):
            return self.product.additionalProperties

        @field
        def aggregateRating(self):
            return self.product.aggregateRating

        @field
        def availability(self):
            return self.product.availability

        @field
        def brand(self):
            return self.product.brand

        @field
        def breadcrumbs(self):
            return self.product.breadcrumbs

        @field
        def canonicalUrl(self):
            return self.product.canonicalUrl

        @field
        def color(self):
            return self.product.color

        @field
        def currency(self):
            return self.product.currency

        @field
        def currencyRaw(self):
            return self.product.currencyRaw

        @field
        def description(self):
            return self.product.description

        @field
        def descriptionHtml(self):
            return self.product.descriptionHtml

        @field
        def features(self):
            return self.product.features

        @field
        def gtin(self):
            return self.product.gtin

        @field
        def images(self):
            return self.product.images

        @field
        def mainImage(self):
            return self.product.mainImage

        @field
        def metadata(self):
            return self.product.metadata

        @field
        def mpn(self):
            return self.product.mpn

        @field
        def name(self):
            return self.product.name

        @field
        def price(self):
            return self.product.price

        @field
        def productId(self):
            return self.product.productId

        @field
        def regularPrice(self):
            return self.product.regularPrice

        @field
        def size(self):
            return self.product.size

        @field
        def sku(self):
            return self.product.sku

        @field
        def style(self):
            return self.product.style

        @field
        def url(self):
            return self.product.url

        @field
        def variants(self):
            return self.product.variants

    handle_urls("a.example")(MyProductPage)
    auto_field_stats = await get_auto_field_stats()
    assert auto_field_stats == {
        "zyte_common_items/auto_fields/tests.test_auto_field_stats.test_full_override.<locals>.MyProductPage": "",
    }


@ensureDeferred
async def test_callback_override():
    """Fields overridden in callbacks, instead of using a page object, are not
    taken into account."""

    class CallbackOverrideSpider(TestSpider):
        def parse(self, response: DummyResponse, product: Product):
            product.name = "foo"
            yield product

    auto_field_stats = await get_auto_field_stats(spider_cls=CallbackOverrideSpider)
    assert auto_field_stats == {
        "zyte_common_items/auto_fields/zyte_common_items.items.product.Product": (
            "(all fields)"
        ),
    }


@ensureDeferred
async def test_item_page_override():
    """The stat accounts for the configured page for a given item, so if you
    request that page directly, things work the same as if you request the item
    itself."""

    class MyProductPage(AutoProductPage):

        @field
        def brand(self):
            return "foo"

        @field
        def name(self):
            return self.product.name

    handle_urls("a.example")(MyProductPage)

    class PageSpider(TestSpider):
        async def parse(self, response: DummyResponse, page: MyProductPage):  # type: ignore[override]
            yield await page.to_item()

    auto_field_stats = await get_auto_field_stats(spider_cls=PageSpider)
    assert auto_field_stats == {
        "zyte_common_items/auto_fields/tests.test_auto_field_stats.test_item_page_override.<locals>.MyProductPage": (
            "additionalProperties aggregateRating availability breadcrumbs "
            "canonicalUrl color currency currencyRaw description descriptionHtml "
            "features gtin images mainImage metadata mpn price productId "
            "regularPrice size sku style url variants"
        ),
    }


@ensureDeferred
async def test_alt_page_override():
    """The stat does not account for alternatives pages, so if you request a
    page that provides an item, the page that counts for stats is the
    configured page for that item, not the actual page requested."""

    class MyProductPage(AutoProductPage):

        @field
        def brand(self):
            return "foo"

        @field
        def name(self):
            return self.product.name

    handle_urls("a.example")(MyProductPage)

    class AltProductPage(AutoProductPage):

        @field
        def sku(self):
            return "foo"

        @field
        def currencyRaw(self):
            return self.product.currencyRaw

    handle_urls("a.example", priority=0)(AltProductPage)

    class AltSpider(TestSpider):
        async def parse(self, response: DummyResponse, page: AltProductPage):  # type: ignore[override]
            yield await page.to_item()

    auto_field_stats = await get_auto_field_stats(spider_cls=AltSpider)
    assert auto_field_stats == {
        "zyte_common_items/auto_fields/tests.test_auto_field_stats.test_alt_page_override.<locals>.MyProductPage": (
            "additionalProperties aggregateRating availability breadcrumbs "
            "canonicalUrl color currency currencyRaw description descriptionHtml "
            "features gtin images mainImage metadata mpn price productId "
            "regularPrice size sku style url variants"
        ),
    }


@ensureDeferred
async def test_non_auto_override():
    """If instead of using an Auto…Page class you use a custom class, all
    fields are assumed to be overridden."""

    @attrs.define
    class MyProductPage(BaseProductPage):
        product: Product

        @field
        def additionalProperties(self):
            return self.product.additionalProperties

    handle_urls("a.example")(MyProductPage)

    auto_field_stats = await get_auto_field_stats()
    assert auto_field_stats == {
        "zyte_common_items/auto_fields/tests.test_auto_field_stats.test_non_auto_override.<locals>.MyProductPage": "",
    }


@ensureDeferred
async def test_auto_field_decorator():
    """Using @auto_field forces a field to not be considered overridden."""

    @attrs.define
    class MyProductPage(BaseProductPage):
        product: Product

        @auto_field
        def additionalProperties(self):
            return self.product.additionalProperties

    handle_urls("a.example")(MyProductPage)

    auto_field_stats = await get_auto_field_stats()
    assert auto_field_stats == {
        "zyte_common_items/auto_fields/tests.test_auto_field_stats.test_auto_field_decorator.<locals>.MyProductPage": "additionalProperties",
    }


@ensureDeferred
async def test_auto_field_meta():
    """Using @field(meta={"auto_field": True}) has the same effect as using
    @auto_field."""

    @attrs.define
    class MyProductPage(BaseProductPage):
        product: Product

        @field(meta={"auto_field": True})
        def additionalProperties(self):
            return self.product.additionalProperties

    handle_urls("a.example")(MyProductPage)

    auto_field_stats = await get_auto_field_stats()
    assert auto_field_stats == {
        "zyte_common_items/auto_fields/tests.test_auto_field_stats.test_auto_field_meta.<locals>.MyProductPage": "additionalProperties",
    }


@ensureDeferred
async def test_custom_item():
    @attrs.define
    class CustomProduct(Item):
        url: str
        product_title: Optional[str] = None

    @attrs.define
    class MyProductPage(ItemPage[CustomProduct]):
        product: Product

        @field
        def url(self) -> str:
            return "https://a.example/"

        @field(meta={"auto_field": True})
        def product_title(self) -> Optional[str]:
            return self.product.name

    handle_urls("a.example")(MyProductPage)

    class CustomProductSpider(TestSpider):
        def parse(self, response: DummyResponse, product: CustomProduct):  # type: ignore[override]
            yield product

    auto_field_stats = await get_auto_field_stats(spider_cls=CustomProductSpider)
    assert auto_field_stats == {
        "zyte_common_items/auto_fields/tests.test_auto_field_stats.test_custom_item.<locals>.MyProductPage": "product_title",
    }


@ensureDeferred
async def test_custom_item_missing_url(caplog):
    @attrs.define
    class CustomProduct(Item):
        weight: Optional[float] = None
        product_title: Optional[str] = None

    @attrs.define
    class MyProductPage(ItemPage[CustomProduct]):
        product: Product

        @field
        def weight(self) -> Optional[float]:
            return None

        @field(meta={"auto_field": True})
        def product_title(self) -> Optional[str]:
            return self.product.name

    handle_urls("a.example")(MyProductPage)

    class CustomProductSpider(TestSpider):
        def parse(self, response: DummyResponse, product: CustomProduct):  # type: ignore[override]
            yield product

    caplog.clear()
    auto_field_stats = await get_auto_field_stats(spider_cls=CustomProductSpider)
    assert auto_field_stats == {}

    assert len(caplog.records) == 1
    assert "was missing a non-empty URL" in caplog.records[0].msg


@ensureDeferred
async def test_custom_item_custom_url_field():
    @attrs.define
    class CustomProduct(Item):
        product_url: str
        product_title: Optional[str] = None

    @attrs.define
    class MyProductPage(ItemPage[CustomProduct]):
        product: Product

        @field(meta={"auto_field": True})
        def product_url(self) -> str:
            return self.product.url

        @field(meta={"auto_field": True})
        def product_title(self) -> Optional[str]:
            return self.product.name

    handle_urls("a.example")(MyProductPage)

    class CustomProductSpider(TestSpider):
        def parse(self, response: DummyResponse, product: CustomProduct):  # type: ignore[override]
            yield product

    settings = {
        **_SETTINGS,
        "ZYTE_COMMON_ITEMS_AUTO_FIELD_URL_FIELDS": {
            CustomProduct: "product_url",
        },
    }
    auto_field_stats = await get_auto_field_stats(settings, CustomProductSpider)
    assert auto_field_stats == {
        "zyte_common_items/auto_fields/tests.test_auto_field_stats.test_custom_item_custom_url_field.<locals>.MyProductPage": "(all fields)",
    }


@ensureDeferred
async def test_missing_injection_middleware():
    settings = copy(_SETTINGS)
    assert isinstance(settings["DOWNLOADER_MIDDLEWARES"], dict)
    del settings["DOWNLOADER_MIDDLEWARES"]["scrapy_poet.InjectionMiddleware"]
    with pytest.raises(RuntimeError):
        await get_auto_field_stats()
