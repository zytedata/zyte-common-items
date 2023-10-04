from copy import copy

import attrs
import pytest
from web_poet import RequestUrl, Returns, field

from zyte_common_items import AutoProductPage, Product

from .test_items import _PRODUCT_ALL_KWARGS


@pytest.mark.asyncio
async def test_product_unmodified():
    input_product = Product(**_PRODUCT_ALL_KWARGS)
    page = AutoProductPage(
        product=input_product,
        request_url=RequestUrl("https://example.com"),
    )
    assert await page.to_item() == input_product


@pytest.mark.asyncio
async def test_product_modified():
    class CustomProductPage(AutoProductPage):
        @field
        async def name(self):
            return f"{self.product.brand.name} {self.product.name}"

    input_product = Product(**_PRODUCT_ALL_KWARGS)
    page = CustomProductPage(
        product=input_product,
        request_url=RequestUrl("https://example.com"),
    )
    expected_product = copy(input_product)
    expected_product.name = f"{input_product.brand.name} {input_product.name}"
    assert await page.to_item() == expected_product


@pytest.mark.asyncio
async def test_product_extended():
    @attrs.define
    class ExtendedProduct(Product):
        foo: str

    class CustomProductPage(AutoProductPage, Returns[ExtendedProduct]):
        @field
        async def foo(self):
            return "bar"

    input_product = Product(**_PRODUCT_ALL_KWARGS)
    page = CustomProductPage(
        product=input_product,
        request_url=RequestUrl("https://example.com"),
    )
    expected_product = ExtendedProduct(**_PRODUCT_ALL_KWARGS, foo="bar")
    assert await page.to_item() == expected_product
