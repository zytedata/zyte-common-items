import pytest
from lxml.html import fromstring
from parsel import Selector
from web_poet import HttpResponse, field
from zyte_parsers import Breadcrumb as zp_Breadcrumb

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
    "input_value",
    (
        breadcrumbs_expected,
        fromstring(breadcrumbs_html),
        Selector(text=breadcrumbs_html),
        [
            zp_Breadcrumb(name="Home", url="http://www.example.com/blog/"),
            zp_Breadcrumb(name="About", url="http://www.example.com/blog/about/"),
        ],
    ),
)
def test_breadcrumbs(input_value):
    base_url = "http://www.example.com/blog/"

    class BreadcrumbsPage(BasePage):
        @field(out=[breadcrumbs_processor])
        def breadcrumbs(self):
            return input_value

    page = BreadcrumbsPage(base_url)  # type: ignore[arg-type]
    assert page.breadcrumbs == breadcrumbs_expected


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
