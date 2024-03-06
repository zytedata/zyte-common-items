from urllib.parse import quote, quote_plus

import attrs
import pytest
from web_poet import PageParams, RequestUrl, field

from zyte_common_items.pages import SearchRequestPage


@attrs.define
class UnquotedSearchRequestPage(SearchRequestPage):
    page_params: PageParams

    @field
    def url(self):
        return f"https://example.com/?search={self.page_params['keyword']}"


@attrs.define
class QuoteSearchRequestPage(SearchRequestPage):
    page_params: PageParams

    @field
    def url(self):
        return f"https://example.com/?search={quote(self.page_params['keyword'])}"


@attrs.define
class QuotePlusSearchRequestPage(SearchRequestPage):
    page_params: PageParams

    @field
    def url(self):
        return f"https://example.com/?search={quote_plus(self.page_params['keyword'])}"


@attrs.define
class CustomFilterSearchRequestPage(SearchRequestPage):
    page_params: PageParams

    @field
    def url(self):
        return f"https://example.com/?search={self.page_params['keyword']} baz"


@attrs.define
class UrlBasedSearchRequestPage(SearchRequestPage):
    page_params: PageParams
    request_url: RequestUrl

    @field
    def url(self):
        return f"{self.request_url}?search={quote(self.page_params['keyword'])}"


@attrs.define
class DynamicSearchRequestPage(SearchRequestPage):
    page_params: PageParams

    @field
    def url(self):
        keyword = self.page_params["keyword"]
        if len(keyword) >= 2 and keyword[0].lower() == "p" and keyword[1:].isdigit():
            return f"https://example.com/p/{self.page_params['keyword'].upper()}"
        else:
            return f"https://example.com/?search={quote(self.page_params['keyword'])}"


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
        (
            DynamicSearchRequestPage,
            {},
            "foo bar",
            "https://example.com/?search=foo%20bar",
        ),
        (
            DynamicSearchRequestPage,
            {},
            "p250",
            "https://example.com/p/P250",
        ),
    ),
)
@pytest.mark.asyncio
async def test_url(page, inputs, keyword, url):
    search_request = await page(**inputs, page_params={"keyword": keyword}).to_item()
    assert search_request.url == url
