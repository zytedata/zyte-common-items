from datetime import datetime

import attrs
import pytest
from web_poet import HttpResponse, RequestUrl, ResponseUrl, field

from zyte_common_items import (
    BaseProductListPage,
    BaseProductPage,
    ProductListPage,
    ProductPage,
)


@pytest.mark.parametrize(
    "page_class",
    (
        BaseProductPage,
        BaseProductListPage,
    ),
)
def test_base_pages_default(page_class):
    datetime_before = datetime.utcnow().replace(microsecond=0)

    page = page_class(request_url=RequestUrl("https://example.com"))

    assert page.metadata.probability == 1.0
    assert page.url == "https://example.com"
    assert isinstance(page.url, str)

    page_datetime_string = page.metadata.dateDownloaded
    assert page_datetime_string.endswith("Z")
    page_datetime = datetime.fromisoformat(page_datetime_string[:-1])
    datetime_after = datetime.utcnow().replace(microsecond=0)
    assert datetime_before <= page_datetime <= datetime_after


@pytest.mark.parametrize(
    "page_class",
    (
        ProductPage,
        ProductListPage,
    ),
)
def test_pages_default(page_class):
    datetime_before = datetime.utcnow().replace(microsecond=0)

    url = ResponseUrl("https://example.com")
    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <h1>Foo</h1>
        </body>
    </html>
    """
    response = HttpResponse(url=url, body=html)

    page = page_class(response=response)

    assert page.metadata.probability == 1.0
    assert page.url == "https://example.com"
    assert isinstance(page.url, str)

    page_datetime_string = page.metadata.dateDownloaded
    assert page_datetime_string.endswith("Z")
    page_datetime = datetime.fromisoformat(page_datetime_string[:-1])
    datetime_after = datetime.utcnow().replace(microsecond=0)
    assert datetime_before <= page_datetime <= datetime_after


@pytest.mark.asyncio
async def test_example():
    datetime_before = datetime.utcnow().replace(microsecond=0)

    @attrs.define
    class BookPage(ProductPage):
        @field
        def name(self):
            return self.css("h1::text").get()

    url = ResponseUrl("https://example.com/books/1")
    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <h1>Foo</h1>
        </body>
    </html>
    """
    response = HttpResponse(url=url, body=html)

    item = await BookPage(response=response).to_item()

    assert item.url == str(url)
    assert item.name == "Foo"
    assert item.metadata.probability == 1.0

    item_datetime_string = item.metadata.dateDownloaded
    assert item_datetime_string.endswith("Z")
    item_datetime = datetime.fromisoformat(item_datetime_string[:-1])
    datetime_after = datetime.utcnow().replace(microsecond=0)
    assert datetime_before <= item_datetime <= datetime_after


@pytest.mark.asyncio
async def test_mixin_leak():
    """https://github.com/zytedata/zyte-common-items/pull/29"""

    class MyProductListPage(ProductListPage):
        @field
        def products(self):
            return [{"name": "foo"}, {"name": "bar"}]

    class MyProductPage(ProductPage):
        @field
        def brand(self):
            return "baz"

    from web_poet.fields import get_fields_dict

    assert set(get_fields_dict(MyProductListPage)) == {"metadata", "products", "url"}
    assert set(get_fields_dict(MyProductPage)) == {"brand", "metadata", "url"}


@pytest.mark.asyncio
async def test_no_item_found_Page():

    class MyProductPage(ProductPage):
        def validate_input(self):
            return self.no_item_found()

    response = HttpResponse(url="http://example.com", body=b"<html></html>")
    page = MyProductPage(response=response)

    item = await page.to_item()
    assert item.metadata.probability == 0
    assert item.url == "http://example.com"


@pytest.mark.asyncio
async def test_no_item_found_BasePage():

    class MyProductPage(BaseProductPage):
        def validate_input(self):
            return self.no_item_found()

    page = MyProductPage(request_url=RequestUrl("http://example.com"))

    item = await page.to_item()
    assert item.metadata.probability == 0
    assert item.url == "http://example.com"
