from datetime import datetime

import attrs
import pytest
from web_poet import HttpResponse, ResponseUrl, field

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

    page = page_class(url=ResponseUrl("https://example.com"))

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
