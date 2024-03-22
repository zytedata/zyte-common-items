from copy import copy
from typing import Any, Dict, Type

import attrs
import pytest
from itemadapter import ItemAdapter
from web_poet import RequestUrl, Returns, field

from zyte_common_items import (
    Article,
    ArticleList,
    ArticleNavigation,
    AutoArticleListPage,
    AutoArticleNavigationPage,
    AutoArticlePage,
    AutoBusinessPlacePage,
    AutoJobPostingPage,
    AutoProductListPage,
    AutoProductNavigationPage,
    AutoProductPage,
    AutoRealEstatePage,
    BusinessPlace,
    JobPosting,
    Product,
    ProductList,
    ProductNavigation,
    RealEstate,
)

from .test_items import (
    _ARTICLE_ALL_KWARGS,
    _ARTICLE_LIST_ALL_KWARGS,
    _ARTICLE_NAVIGATION_ALL_KWARGS,
    _BUSINESS_PLACE_ALL_KWARGS,
    _JOB_POSTING_ALL_KWARGS,
    _PRODUCT_ALL_KWARGS,
    _PRODUCT_LIST_ALL_KWARGS,
    _PRODUCT_NAVIGATION_ALL_KWARGS,
    _REAL_ESTATE_ALL_KWARGS,
)

PARAMS = (
    "item_cls,item_kwargs,cls,param",
    (
        (Article, _ARTICLE_ALL_KWARGS, AutoArticlePage, "article"),
        (ArticleList, _ARTICLE_LIST_ALL_KWARGS, AutoArticleListPage, "article_list"),
        (
            ArticleNavigation,
            _ARTICLE_NAVIGATION_ALL_KWARGS,
            AutoArticleNavigationPage,
            "article_navigation",
        ),
        (
            BusinessPlace,
            _BUSINESS_PLACE_ALL_KWARGS,
            AutoBusinessPlacePage,
            "business_place",
        ),
        (
            JobPosting,
            _JOB_POSTING_ALL_KWARGS,
            AutoJobPostingPage,
            "job_posting",
        ),
        (Product, _PRODUCT_ALL_KWARGS, AutoProductPage, "product"),
        (ProductList, _PRODUCT_LIST_ALL_KWARGS, AutoProductListPage, "product_list"),
        (
            ProductNavigation,
            _PRODUCT_NAVIGATION_ALL_KWARGS,
            AutoProductNavigationPage,
            "product_navigation",
        ),
        (
            RealEstate,
            _REAL_ESTATE_ALL_KWARGS,
            AutoRealEstatePage,
            "real_estate",
        ),
    ),
)


async def assert_expected_item(page, item):
    assert await page.to_item() == item
    # Ensure that all fields are sync.
    for k, v in ItemAdapter(item).items():
        assert getattr(page, k) == v


@pytest.mark.parametrize(*PARAMS)
@pytest.mark.asyncio
async def test_unmodified(
    item_cls: Type, item_kwargs: Dict[str, Any], cls: Type, param: str
) -> None:
    item = item_cls(**item_kwargs)
    kwargs = {
        param: item,
        "request_url": RequestUrl("https://example.com"),
    }
    page = cls(**kwargs)
    await assert_expected_item(page, item)


@pytest.mark.parametrize(*PARAMS)
@pytest.mark.asyncio
async def test_modified(
    item_cls: Type, item_kwargs: Dict[str, Any], cls: Type, param: str
) -> None:
    modified_url = "https://custom.example"

    class CustomPage(cls):
        @field
        def url(self):
            return modified_url

    item = item_cls(**item_kwargs)
    kwargs = {
        param: item,
        "request_url": RequestUrl("https://example.com"),
    }
    page = CustomPage(**kwargs)
    expected_item = copy(item)
    expected_item.url = modified_url
    await assert_expected_item(page, expected_item)


@pytest.mark.parametrize(*PARAMS)
@pytest.mark.asyncio
async def test_extended(
    item_cls: Type, item_kwargs: Dict[str, Any], cls: Type, param: str
) -> None:
    @attrs.define
    class ExtendedItem(item_cls):
        foo: str

    class ExtendedPage(cls, Returns[ExtendedItem]):
        @field
        def foo(self):
            return "bar"

    kwargs = {
        param: item_cls(**item_kwargs),
        "request_url": RequestUrl("https://example.com"),
    }
    page = ExtendedPage(**kwargs)
    expected_item = ExtendedItem(**item_kwargs, foo="bar")
    await assert_expected_item(page, expected_item)
