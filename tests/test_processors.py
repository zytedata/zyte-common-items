import pytest
from lxml.html import fromstring
from parsel import Selector, SelectorList
from web_poet import HttpResponse, field
from zyte_parsers import Breadcrumb as zp_Breadcrumb
from zyte_parsers import extract_breadcrumbs

from zyte_common_items import BasePage, Breadcrumb, ProductPage
from zyte_common_items.processors import breadcrumbs_processor

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
    base_url = "http://www.example.com/blog/"

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
