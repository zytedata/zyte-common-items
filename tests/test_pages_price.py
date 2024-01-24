import pytest
from web_poet import HttpResponse, field

from zyte_common_items import ProductPage


@pytest.mark.asyncio
async def test_price_selector():
    class CustomProductPage(ProductPage):
        call_count = 0

        @field
        def price(self):
            self.call_count += 1
            return self.css("div::text")

    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <div>$13.2</div>
        </body>
    </html>
    """
    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.call_count == 0
    assert page.price == "13.20"
    assert page.call_count == 1
    assert page.currency is None
    assert await page.currencyRaw == "$"
    assert page.call_count == 1

    # access currency fields before the price field
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.call_count == 0
    assert page.currency is None
    assert await page.currencyRaw == "$"
    assert page.call_count == 1
    assert page.price == "13.20"
    assert page.call_count == 2  # we want this to be 1


@pytest.mark.asyncio
async def test_price_explicit():
    class CustomProductPage(ProductPage):
        call_count = 0

        @field
        def price(self):
            self.call_count += 1
            return self.css("div::text").get()

    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <div>$13.2</div>
        </body>
    </html>
    """
    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.call_count == 0
    assert page.price == "$13.2"
    assert page.call_count == 1
    assert page.currency is None
    assert await page.currencyRaw is None
    assert page.call_count == 2  # we want this to be 1
    assert await page.currencyRaw is None
    assert page.call_count == 2  # we want this to be 1

    # access currency fields before the price field
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.call_count == 0
    assert page.currency is None
    assert await page.currencyRaw is None
    assert page.call_count == 1
    assert page.price == "$13.2"
    assert page.call_count == 2  # we want this to be 1


@pytest.mark.asyncio
async def test_price_async():
    class CustomProductPage(ProductPage):
        @field
        async def price(self):
            return self.css("div::text")

    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <div>$13.2</div>
        </body>
    </html>
    """
    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert await page.price == "13.20"
    assert page.currency is None
    assert await page.currencyRaw == "$"

    # access currency fields before the price field
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.currency is None
    assert await page.currencyRaw == "$"
    assert await page.price == "13.20"


@pytest.mark.asyncio
async def test_currency_hardcoded():
    class CustomProductPage(ProductPage):
        CURRENCY = "USD"

        @field
        def price(self):
            return self.css("div::text")

    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <div>$13.2</div>
        </body>
    </html>
    """
    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.price == "13.20"
    assert page.currency == "USD"
    assert await page.currencyRaw == "$"

    # access currency fields before the price field
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.currency == "USD"
    assert await page.currencyRaw == "$"
    assert page.price == "13.20"


@pytest.mark.asyncio
async def test_currency_no_price():
    class CustomProductPage(ProductPage):
        CURRENCY = "USD"

    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <div>$13.2</div>
        </body>
    </html>
    """
    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.currency == "USD"
    assert await page.currencyRaw is None


@pytest.mark.asyncio
async def test_currency_none_price():
    class CustomProductPage(ProductPage):
        CURRENCY = "USD"
        call_count = 0

        @field
        def price(self):
            self.call_count += 1
            return None

    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <div>$13.2</div>
        </body>
    </html>
    """
    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.call_count == 0
    assert page.currency == "USD"
    assert await page.currencyRaw is None
    assert page.call_count == 1
    assert await page.currencyRaw is None
    assert page.call_count == 1
    assert page.price is None
    assert page.call_count == 2  # we want this to be 1


@pytest.mark.asyncio
async def test_regularPrice():
    class CustomProductPage(ProductPage):
        CURRENCY = "USD"

        @field
        def price(self):
            return self.css("b::text")

        @field
        def regularPrice(self):
            return self.css("div::text")

    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <div>$13.2</div>
            <b>$10.2</b>
        </body>
    </html>
    """
    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.regularPrice == "13.20"
    assert page.price == "10.20"
    assert page.currency == "USD"
    assert await page.currencyRaw == "$"

    # access currency fields before the price field
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.currency == "USD"
    assert await page.currencyRaw == "$"
    assert page.price == "10.20"
    assert page.regularPrice == "13.20"


@pytest.mark.asyncio
async def test_price_invalid():
    class CustomProductPage(ProductPage):
        CURRENCY = "USD"

        @field
        def price(self):
            return self.css("div::text")

    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <div>Out of stock</div>
        </body>
    </html>
    """
    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.price is None
    assert page.currency == "USD"
    assert await page.currencyRaw is None

    # access currency fields before the price field
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.currency == "USD"
    assert await page.currencyRaw is None
    assert page.price is None


def test_currencyRaw_explicit():
    class CustomProductPage(ProductPage):
        @field
        def price(self):
            return self.css("div::text")

        @field
        def currencyRaw(self):
            return "US$"

    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <div>$13.2</div>
        </body>
    </html>
    """
    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.price == "13.20"
    assert page.currency is None
    assert page.currencyRaw == "US$"

    # access currency fields before the price field
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.currency is None
    assert page.currencyRaw == "US$"
    assert page.price == "13.20"
