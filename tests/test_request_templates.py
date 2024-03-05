import attrs
import pytest
from web_poet import RequestUrl, field

from zyte_common_items.pages import SearchRequestTemplatePage


class NoFilterSearchRequestTemplatePage(SearchRequestTemplatePage):
    @field
    def url(self):
        return "https://example.com/?search={{ keyword }}"


class JinjaBuiltInFilterSearchRequestTemplatePage(SearchRequestTemplatePage):
    @field
    def url(self):
        return "https://example.com/?search={{ keyword|urlencode }}"


class OurBuiltInFilterSearchRequestTemplatePage(SearchRequestTemplatePage):
    @field
    def url(self):
        return "https://example.com/?search={{ keyword|quote_plus }}"


class CustomFilterSearchRequestTemplatePage(SearchRequestTemplatePage):
    @field
    def filters(self):
        return {**super().filters, "foo": lambda v: f"{v} baz"}

    @field
    def url(self):
        return "https://example.com/?search={{ keyword|foo }}"


@attrs.define
class UrlBasedSearchRequestTemplatePage(SearchRequestTemplatePage):
    request_url: RequestUrl

    @field
    def url(self):
        return f"{self.request_url}?search={{{{ keyword|urlencode }}}}"


@pytest.mark.parametrize(
    ("page", "inputs", "keyword", "url"),
    (
        (
            NoFilterSearchRequestTemplatePage,
            {},
            "foo bar",
            "https://example.com/?search=foo bar",
        ),
        (
            JinjaBuiltInFilterSearchRequestTemplatePage,
            {},
            "foo bar",
            "https://example.com/?search=foo%20bar",
        ),
        (
            OurBuiltInFilterSearchRequestTemplatePage,
            {},
            "foo bar",
            "https://example.com/?search=foo+bar",
        ),
        (
            CustomFilterSearchRequestTemplatePage,
            {},
            "foo bar",
            "https://example.com/?search=foo bar baz",
        ),
        (
            UrlBasedSearchRequestTemplatePage,
            {"request_url": RequestUrl("https://foo.example/")},
            "foo bar",
            "https://foo.example/?search=foo%20bar",
        ),
    ),
)
@pytest.mark.asyncio
async def test_url(page, inputs, keyword, url):
    search_request_template = await page(**inputs).to_item()
    search_request = search_request_template.request(keyword=keyword)
    assert search_request.url == url