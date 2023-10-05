from copy import copy

import attrs
import pytest
from web_poet import RequestUrl, Returns, field

from zyte_common_items import (
    Article,
    AutoArticlePage,
    AutoProductListPage,
    AutoProductNavigationPage,
    AutoProductPage,
    Product,
    ProductList,
    ProductNavigation,
)

from .test_items import (
    _ARTICLE_ALL_KWARGS,
    _PRODUCT_ALL_KWARGS,
    _PRODUCT_LIST_ALL_KWARGS,
    _PRODUCT_NAVIGATION_ALL_KWARGS,
)

PARAMS = (
    "item_cls,item_kwargs,cls,param",
    (
        (Product, _PRODUCT_ALL_KWARGS, AutoProductPage, "product"),
        (ProductList, _PRODUCT_LIST_ALL_KWARGS, AutoProductListPage, "product_list"),
        (
            ProductNavigation,
            _PRODUCT_NAVIGATION_ALL_KWARGS,
            AutoProductNavigationPage,
            "product_navigation",
        ),
        (Article, _ARTICLE_ALL_KWARGS, AutoArticlePage, "article"),
    ),
)


@pytest.mark.parametrize(*PARAMS)
@pytest.mark.asyncio
async def test_unmodified(item_cls, item_kwargs, cls, param):
    item = item_cls(**item_kwargs)
    kwargs = {
        param: item,
        "request_url": RequestUrl("https://example.com"),
    }
    page = cls(**kwargs)
    assert await page.to_item() == item


@pytest.mark.parametrize(*PARAMS)
@pytest.mark.asyncio
async def test_modified(item_cls, item_kwargs, cls, param):
    modified_url = "https://custom.example"

    class CustomPage(cls):
        @field
        async def url(self):
            return modified_url

    item = item_cls(**item_kwargs)
    kwargs = {
        param: item,
        "request_url": RequestUrl("https://example.com"),
    }
    page = CustomPage(**kwargs)
    expected_item = copy(item)
    expected_item.url = modified_url
    assert await page.to_item() == expected_item


@pytest.mark.parametrize(*PARAMS)
@pytest.mark.asyncio
async def test_extended(item_cls, item_kwargs, cls, param):
    @attrs.define
    class ExtendedItem(item_cls):
        foo: str

    class ExtendedPage(cls, Returns[ExtendedItem]):
        @field
        async def foo(self):
            return "bar"

    kwargs = {
        param: item_cls(**item_kwargs),
        "request_url": RequestUrl("https://example.com"),
    }
    page = ExtendedPage(**kwargs)
    expected_item = ExtendedItem(**item_kwargs, foo="bar")
    assert await page.to_item() == expected_item
