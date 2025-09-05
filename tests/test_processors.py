from typing import Type

import pytest
from lxml.html import fromstring
from parsel import Selector, SelectorList
from price_parser import Price
from web_poet import HttpResponse, field
from zyte_parsers import Breadcrumb as zp_Breadcrumb
from zyte_parsers import Gtin as zp_Gtin
from zyte_parsers import extract_breadcrumbs

from zyte_common_items import (
    AggregateRating,
    BasePage,
    Brand,
    Breadcrumb,
    Gtin,
    Image,
    ProductPage,
)
from zyte_common_items.components.metadata import Metadata
from zyte_common_items.items.product import ProductMetadata
from zyte_common_items.processors import (
    _format_price,
    brand_processor,
    breadcrumbs_processor,
    gtin_processor,
    images_processor,
    metadata_processor,
    price_processor,
    rating_processor,
)

base_url = "http://www.example.com/blog/"

breadcrumbs_html = """
<div class="pagesbar">
  <ul>
    <li><a href="/blog/">Home</a></li>
    <li><a href="/blog/about/">About</a></li>
  </ul>
</div>
"""

breadcrumbs_expected = [
    Breadcrumb(name="Home", url="http://www.example.com/blog/"),
    Breadcrumb(name="About", url="http://www.example.com/blog/about/"),
]


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        (None, None),
        ([], []),
        ("foo", "foo"),
        (Selector(text="<html></html>"), None),
        (SelectorList([]), None),
        (breadcrumbs_expected, breadcrumbs_expected),
        (fromstring(breadcrumbs_html), breadcrumbs_expected),
        (Selector(text=breadcrumbs_html), breadcrumbs_expected),
        (
            [
                zp_Breadcrumb(name="Home", url="http://www.example.com/blog/"),
                zp_Breadcrumb(name="About", url="http://www.example.com/blog/about/"),
            ],
            breadcrumbs_expected,
        ),
    ],
)
def test_breadcrumbs(input_value, expected_value):
    class BreadcrumbsPage(BasePage):
        @field(out=[breadcrumbs_processor])
        def breadcrumbs(self):
            return input_value

    page = BreadcrumbsPage(base_url)  # type: ignore[arg-type]
    assert page.breadcrumbs == expected_value


def test_breadcrumbs_page():
    class MyProductPage(ProductPage):
        @field
        def breadcrumbs(self):
            return self.css(".pagesbar")

    response = HttpResponse(
        url="http://www.example.com/blog/",
        body=f"<html><body>{breadcrumbs_html}</body></html>".encode(),
    )
    page = MyProductPage(response=response)
    assert page.breadcrumbs == breadcrumbs_expected


def test_breadcrumbs_page_zyte_parsers():
    class MyProductPage(ProductPage):
        @field
        def breadcrumbs(self):
            return extract_breadcrumbs(self.css(".pagesbar")[0], base_url=self.url)

    response = HttpResponse(
        url="http://www.example.com/blog/",
        body=f"<html><body>{breadcrumbs_html}</body></html>".encode(),
    )
    page = MyProductPage(response=response)
    assert page.breadcrumbs == breadcrumbs_expected


def test_breadcrumbs_base_url():
    class MyProductPage(ProductPage):
        @field
        def breadcrumbs(self):
            return self.css(".pagesbar")

    breadcrumbs_html_base = """
    <html>
    <head>
        <base href="http://www.example.com/blog/">
    </head>
    <body>
    <div class="pagesbar">
      <ul>
        <li><a href=".">Home</a></li>
        <li><a href="about/">About</a></li>
      </ul>
    </div>
    </body>
    </html>
    """

    response = HttpResponse(
        url="http://www.example.com/",
        body=breadcrumbs_html_base.encode(),
    )
    page = MyProductPage(response=response)
    assert page.breadcrumbs == breadcrumbs_expected


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        (None, None),
        ("", None),
        (" ", None),
        ("foo", Brand(name="foo")),
        (" foo ", Brand(name="foo")),
        (Selector(text="<html></html>"), None),
        (SelectorList([]), None),
        (fromstring("<p>foo</p>"), Brand(name="foo")),
        (fromstring("<img alt='foo'>"), Brand(name="foo")),
        (fromstring("<p><img alt='foo'></p>"), Brand(name="foo")),
        (fromstring("<p><p><img alt='foo'></p></p>"), Brand(name="foo")),
        (Selector(text="<p>foo</p>"), Brand(name="foo")),
        (SelectorList([Selector(text="<p>foo</p>")]), Brand(name="foo")),
    ],
)
def test_brand(input_value, expected_value):
    class BrandPage(BasePage):
        @field(out=[brand_processor])
        def brand(self):
            return input_value

    page = BrandPage("http://www.example.com/")  # type: ignore[arg-type]
    assert page.brand == expected_value


def test_brand_page():
    class MyProductPage(ProductPage):
        @field
        def brand(self):
            return self.css("body")

    response = HttpResponse(
        url="http://www.example.com/",
        body="<html><body><img alt='foo'></body></html>".encode(),
    )
    page = MyProductPage(response=response)
    assert page.brand == Brand(name="foo")


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        ("", None),
        ("NaN", None),
        ("Infinity", None),
        ("1", "1.00"),
        ("1.2", "1.20"),
        ("1.23", "1.23"),
        # Fails due to . being considered a thousands separator in this case.
        # ("1.234", "1.234"),
        ("1.2345", "1.2345"),
    ],
)
def test_format_price(input_value, expected_value):
    assert _format_price(Price.fromstring(input_value)) == expected_value


gtin_str = "978-1-933624-34-1"
gtin_html = f"<span>{gtin_str}</span>"
gtin_expected = [Gtin("isbn13", "9781933624341")]


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        (None, None),
        ([], None),
        ("foo", None),
        (Selector(text="<html></html>"), None),
        (SelectorList([]), None),
        (gtin_expected, gtin_expected),
        (fromstring(gtin_html), gtin_expected),
        (Selector(text=gtin_html), gtin_expected),
        (
            [
                zp_Gtin("isbn13", "9781933624341"),
                zp_Gtin("isbn13", "9780525555360"),
            ],
            [
                Gtin("isbn13", "9781933624341"),
                Gtin("isbn13", "9780525555360"),
            ],
        ),
        (gtin_str, gtin_expected),
        (
            [
                "978-1-933624-34-1",
                "97-805-25555-360",
            ],
            [
                Gtin("isbn13", "9781933624341"),
                Gtin("isbn13", "9780525555360"),
            ],
        ),
    ],
)
def test_gtin(input_value, expected_value):
    class GtinPage(BasePage):
        @field(out=[gtin_processor])
        def gtin(self):
            return input_value

    page = GtinPage(base_url)  # type: ignore[arg-type]
    assert page.gtin == expected_value


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        (None, None),
        ([], []),
        ("foo", "foo"),
        (Selector(text="<html></html>"), None),
        (SelectorList([]), None),
        (Selector(text="<html>3.8</html>"), AggregateRating(ratingValue=3.8)),
        (
            Selector(text="<html>3.8 out of 10</html>"),
            AggregateRating(ratingValue=3.8, bestRating=10.0),
        ),
        (
            Selector(text="<html>3.8 (7 reviews)</html>"),
            AggregateRating(ratingValue=3.8, reviewCount=7),
        ),
        # provided as a separate xfail test
        # (
        #     Selector(text="<html>3.8 out of 10 (5 reviews)</html>"),
        #     AggregateRating(ratingValue=3.8, reviewCount=5),
        # ),
        (
            AggregateRating(ratingValue=3.8, bestRating=5.0, reviewCount=3),
            AggregateRating(ratingValue=3.8, bestRating=5.0, reviewCount=3),
        ),
        (
            {"ratingValue": 3.8, "bestRating": 5.0, "reviewCount": 3},
            AggregateRating(ratingValue=3.8, bestRating=5.0, reviewCount=3),
        ),
        (
            {"ratingValue": 3.8, "reviewCount": 3},
            AggregateRating(ratingValue=3.8, reviewCount=3),
        ),
        (
            {"ratingValue": 3.8},
            AggregateRating(ratingValue=3.8),
        ),
        (
            {"ratingValue": 3.8, "reviewCount": "3"},
            AggregateRating(ratingValue=3.8, reviewCount=3),
        ),
        (
            {"ratingValue": 3.8, "bestRating": 10, "reviewCount": 3},
            AggregateRating(ratingValue=3.8, bestRating=10.0, reviewCount=3),
        ),
        (
            {
                "ratingValue": Selector(text="<html>3.8 out of 10</html>"),
                "reviewCount": 3,
            },
            AggregateRating(ratingValue=3.8, bestRating=10.0, reviewCount=3),
        ),
        (
            {
                "ratingValue": Selector(text="<html>3.8 out of 10</html>"),
                "bestRating": 5.0,
                "reviewCount": 3,
            },
            AggregateRating(ratingValue=3.8, bestRating=5.0, reviewCount=3),
        ),
        (
            {
                "ratingValue": Selector(text="<html>3.8 out of 10</html>"),
                "reviewCount": Selector(text="<html>3 reviews</html>"),
            },
            AggregateRating(ratingValue=3.8, bestRating=10.0, reviewCount=3),
        ),
        (
            {
                "ratingValue": "2.12",
                "bestRating": "5.0",
                "reviewCount": "12",
            },
            AggregateRating(ratingValue=2.12, bestRating=5.0, reviewCount=12),
        ),
        (
            {
                "ratingValue": "2,12",
                "bestRating": "5,0",
                "reviewCount": "12",
            },
            AggregateRating(ratingValue=2.12, bestRating=5.0, reviewCount=12),
        ),
        (
            {
                "ratingValue": "2.12",
                "bestRating": "5.0",
                "reviewCount": "12,123",
            },
            AggregateRating(ratingValue=2.12, bestRating=5.0, reviewCount=12123),
        ),
    ],
)
def test_rating(input_value, expected_value):
    class RatingPage(BasePage):
        @field(out=[rating_processor])
        def aggregateRating(self):
            return input_value

    page = RatingPage(base_url)  # type: ignore[arg-type]
    assert page.aggregateRating == expected_value


@pytest.mark.xfail(
    reason="When more than 2 numbers are found bestRating is not extracted"
)
def test_rating_3_values():
    class RatingPage(BasePage):
        @field(out=[rating_processor])
        def aggregateRating(self):
            return Selector(text="<html>3.8 out of 10 (5 reviews)</html>")

    page = RatingPage(base_url)  # type: ignore[arg-type]
    assert page.aggregateRating == AggregateRating(
        ratingValue=3.8, bestRating=10, reviewCount=5
    )


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        (None, None),
        ([], []),
        ("https://www.url.com/img.jpg", [Image(url="https://www.url.com/img.jpg")]),
        (
            [
                Image("https://www.url.com/img1.jpg"),
                Image("https://www.url.com/img2.jpg"),
            ],
            [
                Image("https://www.url.com/img1.jpg"),
                Image("https://www.url.com/img2.jpg"),
            ],
        ),
        (
            ["https://www.url.com/img1.jpg", "https://www.url.com/img2.jpg"],
            [
                Image("https://www.url.com/img1.jpg"),
                Image("https://www.url.com/img2.jpg"),
            ],
        ),
        (
            [
                {"url": "https://www.url.com/img1.jpg"},
                {"url": "https://www.url.com/img2.jpg"},
            ],
            [
                Image("https://www.url.com/img1.jpg"),
                Image("https://www.url.com/img2.jpg"),
            ],
        ),
    ],
)
def test_images(input_value, expected_value):
    class ImagesPage(BasePage):
        @field(out=[images_processor])
        def images(self):
            return input_value

    page = ImagesPage(base_url)  # type: ignore[arg-type]
    assert page.images == expected_value


def test_images_page():
    class MyProductPage(ProductPage):
        @field
        def images(self):
            return self.css("img::attr(href)").getall()

    response = HttpResponse(
        url="http://www.example.com/",
        body="<html><body><img href='https://www.url.com/img.jpg'></body></html>".encode(),
    )
    page = MyProductPage(response=response)
    assert page.images == [Image(url="https://www.url.com/img.jpg")]


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        (100, "100.00"),
        (None, None),
        ([], []),
        ({}, {}),
        (22.9, "22.90"),
        (22.0, "22.00"),
        ("22.9", "22.9"),
        ("Do not apply to strings...", "Do not apply to strings..."),
    ],
)
def test_prices(input_value, expected_value):
    class PricePage(BasePage):
        @field(out=[price_processor])
        def price(self):
            return input_value

    page = PricePage(base_url)  # type: ignore[arg-type]
    assert page.price == expected_value


@pytest.mark.parametrize(
    "input_value,BasePage,expected_value",
    [
        (None, ProductPage, None),
        (Metadata(), ProductPage, ProductMetadata()),
    ],
)
def test_metadata(input_value, BasePage: Type, expected_value):
    class CustomPage(BasePage):
        @field(out=[metadata_processor])
        def metadata(self):
            return input_value

    page = CustomPage(base_url)  # type: ignore[arg-type]
    assert page.metadata == expected_value
