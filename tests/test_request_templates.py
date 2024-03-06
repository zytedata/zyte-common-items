import attrs
import pytest
from web_poet import RequestUrl, field

from zyte_common_items.pages import SearchRequestTemplatePage


class VerbatimSearchRequestTemplatePage(SearchRequestTemplatePage):
    @field
    def url(self):
        return "https://example.com/?search={{ keyword }}"


class QuoteSearchRequestTemplatePage(SearchRequestTemplatePage):
    @field
    def url(self):
        return "https://example.com/?search={{ keyword|urlencode }}"


class QuotePlusSearchRequestTemplatePage(SearchRequestTemplatePage):
    @field
    def url(self):
        return "https://example.com/?search={{ keyword|quote_plus }}"


class ReplaceSearchRequestTemplatePage(SearchRequestTemplatePage):
    @field
    def url(self):
        return "https://example.com/search/{{ keyword|replace(' ', '/') }}"


@attrs.define
class UrlBasedSearchRequestTemplatePage(SearchRequestTemplatePage):
    request_url: RequestUrl

    @field
    def url(self):
        return f"{self.request_url}?search={{{{ keyword|urlencode }}}}"


@attrs.define
class DynamicSearchRequestTemplatePage(SearchRequestTemplatePage):
    @field
    def url(self):
        return """
            {%-
                if keyword|length > 1
                and keyword[0]|lower == 'p'
                and keyword[1:]|int(-1) != -1
            -%}
                https://example.com/p/{{ keyword|upper }}
            {%- else -%}
                https://example.com/?search={{ keyword|urlencode }}
            {%- endif -%}
        """


@pytest.mark.parametrize(
    ("page", "inputs", "keyword", "url"),
    (
        (
            VerbatimSearchRequestTemplatePage,
            {},
            "foo bar",
            "https://example.com/?search=foo bar",
        ),
        (
            QuoteSearchRequestTemplatePage,
            {},
            "foo bar",
            "https://example.com/?search=foo%20bar",
        ),
        (
            QuotePlusSearchRequestTemplatePage,
            {},
            "foo bar",
            "https://example.com/?search=foo+bar",
        ),
        (
            ReplaceSearchRequestTemplatePage,
            {},
            "foo bar",
            "https://example.com/search/foo/bar",
        ),
        (
            UrlBasedSearchRequestTemplatePage,
            {"request_url": RequestUrl("https://foo.example/")},
            "foo bar",
            "https://foo.example/?search=foo%20bar",
        ),
        (
            DynamicSearchRequestTemplatePage,
            {},
            "foo bar",
            "https://example.com/?search=foo%20bar",
        ),
        (
            DynamicSearchRequestTemplatePage,
            {},
            "p250",
            "https://example.com/p/P250",
        ),
    ),
)
@pytest.mark.asyncio
async def test_url(page, inputs, keyword, url):
    search_request_template = await page(**inputs).to_item()
    search_request = search_request_template.request(keyword=keyword)
    assert search_request.url == url
