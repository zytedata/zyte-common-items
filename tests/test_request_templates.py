from urllib.parse import quote, quote_plus

import attrs
import pytest
from web_poet import ItemPage, PageParams, RequestUrl, field

from zyte_common_items.items import SearchRequest


@attrs.define
class UnquotedSearchRequestPage(ItemPage[SearchRequest]):
    page_params: PageParams

    @field
    def url(self):
        return f"https://example.com/?search={self.page_params['keyword']}"


@attrs.define
class QuoteSearchRequestPage(ItemPage[SearchRequest]):
    page_params: PageParams

    @field
    def url(self):
        return f"https://example.com/?search={quote(self.page_params['keyword'])}"


@attrs.define
class QuotePlusSearchRequestPage(ItemPage[SearchRequest]):
    page_params: PageParams

    @field
    def url(self):
        return f"https://example.com/?search={quote_plus(self.page_params['keyword'])}"


@attrs.define
class CustomFilterSearchRequestPage(ItemPage[SearchRequest]):
    page_params: PageParams

    @field
    def url(self):
        return f"https://example.com/?search={self.page_params['keyword']} baz"


@attrs.define
class UrlBasedSearchRequestPage(ItemPage[SearchRequest]):
    page_params: PageParams
    request_url: RequestUrl

    @field
    def url(self):
        return f"{self.request_url}?search={quote(self.page_params['keyword'])}"


@pytest.mark.parametrize(
    ("page", "inputs", "keyword", "url"),
    (
        (
            UnquotedSearchRequestPage,
            {},
            "foo bar",
            "https://example.com/?search=foo bar",
        ),
        (
            QuoteSearchRequestPage,
            {},
            "foo bar",
            "https://example.com/?search=foo%20bar",
        ),
        (
            QuotePlusSearchRequestPage,
            {},
            "foo bar",
            "https://example.com/?search=foo+bar",
        ),
        (
            CustomFilterSearchRequestPage,
            {},
            "foo bar",
            "https://example.com/?search=foo bar baz",
        ),
        (
            UrlBasedSearchRequestPage,
            {"request_url": RequestUrl("https://foo.example/")},
            "foo bar",
            "https://foo.example/?search=foo%20bar",
        ),
    ),
)
@pytest.mark.asyncio
async def test_url(page, inputs, keyword, url):
    search_request = await page(**inputs, page_params={"keyword": keyword}).to_item()
    assert search_request.url == url
