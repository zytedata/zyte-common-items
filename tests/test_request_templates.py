import json
from base64 import b64encode
from copy import copy
from importlib.metadata import version

import attrs
import pytest
from itemadapter import ItemAdapter
from packaging.version import Version
from w3lib.url import add_or_replace_parameters
from web_poet import RequestUrl, field

from zyte_common_items import Header, Request, SearchRequestTemplatePage


@pytest.mark.skipif(
    Version(version("jinja2")) < Version("2.9"),
    reason="The tojson filter was added in Jinja 2.9",
)
@pytest.mark.asyncio
async def test_all():
    class HolisticSearchRequestTemplatePage(SearchRequestTemplatePage):
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
                    https://example.com/search
                {%- endif -%}
            """

        @field
        def method(self):
            return """
                {%-
                    if keyword|length > 1
                    and keyword[0]|lower == 'p'
                    and keyword[1:]|int(-1) != -1
                -%}
                    GET
                {%- else -%}
                    POST
                {%- endif -%}
            """

        @field
        def body(self):
            return """
                {%-
                    if keyword|length > 1
                    and keyword[0]|lower == 'p'
                    and keyword[1:]|int(-1) != -1
                -%}
                {%- else -%}
                    {"query": {{ keyword|tojson }}}
                {%- endif -%}
            """

        @field
        def headers(self):
            return [
                Header(
                    name=(
                        """
                            {%-
                                if keyword|length > 1
                                and keyword[0]|lower == 'p'
                                and keyword[1:]|int(-1) != -1
                            -%}
                            {%- else -%}
                                Query
                            {%- endif -%}
                        """
                    ),
                    value="{{ keyword }}",
                ),
            ]

    search_request_template = await HolisticSearchRequestTemplatePage().to_item()

    search_request = search_request_template.request(keyword="p250")
    expected_request = Request("https://example.com/p/P250")
    assert search_request == expected_request

    search_request = search_request_template.request(keyword="foo bar")
    expected_request = Request(
        "https://example.com/search",
        method="POST",
        body=b64encode(json.dumps({"query": "foo bar"}).encode()).decode(),
        headers=[
            Header(name="Query", value="foo bar"),
        ],
    )
    assert search_request == expected_request


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


# Defines way more of what the corresponding test scenario uses to give an idea
# of the future possibilities of this approach.
def edit_request_url(expression, page):
    if isinstance(expression, str):
        return expression
    if not isinstance(expression, dict):
        raise ValueError(
            f"The edit_request_url processor expected a dict, got " f"{expression!r}"
        )
    if "url" in expression:
        url = expression["url"]
    else:
        adapter = ItemAdapter(page)
        for v in adapter.values():
            if isinstance(v, RequestUrl):
                url = str(v)
                break
        else:
            raise ValueError(
                f"Cannot determine the base URL. Expression {expression!r} "
                f"for the edit_request_url processor has no 'url' key, and "
                f"the parent page object class does not define any RequestUrl "
                f"dependency."
            )
    url_safe_keyword_placeholder = "7dnKEYWORD2Ua"
    if "add_query_params" in expression:
        params = copy(expression["add_query_params"])
        for k in list(params):
            v = params.pop(k)
            k = k.format(keyword=url_safe_keyword_placeholder)
            v = v.format(keyword=url_safe_keyword_placeholder)
            params[k] = v
        url = add_or_replace_parameters(url, params)
    url = url.replace(url_safe_keyword_placeholder, "{{ keyword|urlencode }}")
    return url


@attrs.define
class DSLSearchRequestTemplatePage(SearchRequestTemplatePage):
    request_url: RequestUrl

    class Processors:
        url = [edit_request_url]

    @field
    def url(self):
        return {"add_query_params": {"search": "{keyword}"}}


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
            DSLSearchRequestTemplatePage,
            {"request_url": RequestUrl("https://example.com/")},
            "foo bar",
            "https://example.com/?search=foo%20bar",
        ),
    ),
)
@pytest.mark.asyncio
async def test_url(page, inputs, keyword, url):
    search_request_template = await page(**inputs).to_item()
    search_request = search_request_template.request(keyword=keyword)
    assert search_request.url == url


@pytest.mark.asyncio
async def test_body_space():
    class BodySpaceSearchRequestTemplatePage(SearchRequestTemplatePage):
        @field
        def url(self):
            return "https://example.com"

        @field
        def body(self):
            return " "

    search_request_template = await BodySpaceSearchRequestTemplatePage().to_item()
    search_request = search_request_template.request(keyword="foo bar")
    assert search_request.body == b64encode(b" ").decode()


@pytest.mark.asyncio
async def test_header_empty_value():
    class BodySpaceSearchRequestTemplatePage(SearchRequestTemplatePage):
        @field
        def url(self):
            return "https://example.com"

        @field
        def headers(self):
            return [Header(name="Foo", value="")]

    search_request_template = await BodySpaceSearchRequestTemplatePage().to_item()
    search_request = search_request_template.request(keyword="foo bar")
    assert search_request.headers == [Header(name="Foo", value="")]
