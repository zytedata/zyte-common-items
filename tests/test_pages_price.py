from web_poet import HttpResponse, field

from zyte_common_items import ProductPage


def test_price_selector():
    class CustomProductPage(ProductPage):
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
    assert page.price == "13.2"
    assert page.currency is None
    assert page.currencyRaw == "$"

    # access currency fields before the price field
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.currency is None
    assert page.currencyRaw == "$"
    assert page.price == "13.2"


def test_price_explicit():
    class CustomProductPage(ProductPage):
        @field
        def price(self):
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
    assert page.price == "$13.2"
    assert page.currency is None
    assert page.currencyRaw is None

    # access currency fields before the price field
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.currency is None
    assert page.currencyRaw is None
    assert page.price == "$13.2"


def test_currency_hardcoded():
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
    assert page.price == "13.2"
    assert page.currency == "USD"
    assert page.currencyRaw == "$"

    # access currency fields before the price field
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.currency == "USD"
    assert page.currencyRaw == "$"
    assert page.price == "13.2"


def test_currency_no_price():
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
    assert page.currencyRaw is None


def test_regularPrice():
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
    assert page.regularPrice == "13.2"
    assert page.price == "10.2"
    assert page.currency == "USD"
    assert page.currencyRaw == "$"

    # access currency fields before the price field
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.currency == "USD"
    assert page.currencyRaw == "$"
    assert page.price == "10.2"
    assert page.regularPrice == "13.2"


def test_price_invalid():
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
    assert page.currencyRaw is None

    # access currency fields before the price field
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.currency == "USD"
    assert page.currencyRaw is None
    assert page.price is None


def test_currencyRaw_explicit():
    class CustomProductPage(ProductPage):
        @field
        def price(self):
            return self.css("div::text")

        @field
        def currencyRaw(self):
            return "$"

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
    assert page.price == "13.2"
    assert page.currency is None
    assert page.currencyRaw == "$"

    # access currency fields before the price field
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    assert page.currency is None
    assert page.currencyRaw == "$"
    assert page.price == "13.2"
