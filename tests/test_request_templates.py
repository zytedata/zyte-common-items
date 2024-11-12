import json
from base64 import b64encode
from copy import copy
from importlib.metadata import version

import pytest
from itemadapter import ItemAdapter
from packaging.version import Version
from w3lib.url import add_or_replace_parameters
from web_poet import RequestUrl, field

from zyte_common_items import BaseSearchRequestTemplatePage, Header, Request


@pytest.mark.skipif(
    Version(version("jinja2")) < Version("2.9"),
    reason="The tojson filter was added in Jinja 2.9",
)
@pytest.mark.asyncio
async def test_all():
    class HolisticSearchRequestTemplatePage(BaseSearchRequestTemplatePage):
        @field
        def url(self):
            return """
                {%-
                    if query|length > 1
                    and query[0]|lower == 'p'
                    and query[1:]|int(-1) != -1
                -%}
                    https://example.com/p/{{ query|upper }}
                {%- else -%}
                    https://example.com/search
                {%- endif -%}
            """

        @field
        def method(self):
            return """
                {%-
                    if query|length > 1
                    and query[0]|lower == 'p'
                    and query[1:]|int(-1) != -1
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
                    if query|length > 1
                    and query[0]|lower == 'p'
                    and query[1:]|int(-1) != -1
                -%}
                {%- else -%}
                    {"query": {{ query|tojson }}}
                {%- endif -%}
            """

        @field
        def headers(self):
            return [
                Header(
                    name=(
                        """
                            {%-
                                if query|length > 1
                                and query[0]|lower == 'p'
                                and query[1:]|int(-1) != -1
                            -%}
                            {%- else -%}
                                Query
                            {%- endif -%}
                        """
                    ),
                    value="{{ query }}",
                ),
            ]

    page = HolisticSearchRequestTemplatePage(
        request_url=RequestUrl("https://example.com")
    )
    search_request_template = await page.to_item()

    search_request = search_request_template.request(query="p250")
    expected_request = Request("https://example.com/p/P250")
    assert search_request == expected_request

    search_request = search_request_template.request(query="foo bar")
    expected_request = Request(
        "https://example.com/search",
        method="POST",
        body=b64encode(json.dumps({"query": "foo bar"}).encode()).decode(),
        headers=[
            Header(name="Query", value="foo bar"),
        ],
    )
    assert search_request == expected_request


class VerbatimSearchRequestTemplatePage(BaseSearchRequestTemplatePage):
    @field
    def url(self):
        return "https://example.com/?search={{ query }}"


class QuoteSearchRequestTemplatePage(BaseSearchRequestTemplatePage):
    @field
    def url(self):
        return "https://example.com/?search={{ query|urlencode }}"


class QuotePlusSearchRequestTemplatePage(BaseSearchRequestTemplatePage):
    @field
    def url(self):
        return "https://example.com/?search={{ query|quote_plus }}"


class ReplaceSearchRequestTemplatePage(BaseSearchRequestTemplatePage):
    @field
    def url(self):
        return "https://example.com/search/{{ query|replace(' ', '/') }}"


class UrlBasedSearchRequestTemplatePage(BaseSearchRequestTemplatePage):

    @field
    def url(self):
        return f"{self.request_url}?search={{{{ query|urlencode }}}}"


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
    url_safe_query_placeholder = "7dnQUERY2Ua"
    if "add_query_params" in expression:
        params = copy(expression["add_query_params"])
        for k in list(params):
            v = params.pop(k)
            k = k.format(query=url_safe_query_placeholder)
            v = v.format(query=url_safe_query_placeholder)
            params[k] = v
        url = add_or_replace_parameters(url, params)
    url = url.replace(url_safe_query_placeholder, "{{ query|urlencode }}")
    return url


class DSLSearchRequestTemplatePage(BaseSearchRequestTemplatePage):

    class Processors:
        url = [edit_request_url]

    @field
    def url(self):
        return {"add_query_params": {"search": "{query}"}}


@pytest.mark.parametrize(
    ("page_cls", "inputs", "query", "url"),
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
            {},
            "foo bar",
            "https://example.com/?search=foo%20bar",
        ),
    ),
)
@pytest.mark.asyncio
async def test_url(page_cls, inputs, query, url):
    inputs.setdefault("request_url", RequestUrl("https://example.com/"))
    search_request_template = await page_cls(**inputs).to_item()
    search_request = search_request_template.request(query=query)
    assert search_request.url == url


@pytest.mark.asyncio
async def test_body_space():
    class BodySpaceSearchRequestTemplatePage(BaseSearchRequestTemplatePage):
        @field
        def url(self):
            return "https://example.com"

        @field
        def body(self):
            return " "

    page = BodySpaceSearchRequestTemplatePage(RequestUrl("https://example.com"))
    search_request_template = await page.to_item()
    search_request = search_request_template.request(query="foo bar")
    assert search_request.body == b64encode(b" ").decode()


@pytest.mark.asyncio
async def test_header_empty_value():
    class BodySpaceSearchRequestTemplatePage(BaseSearchRequestTemplatePage):
        @field
        def url(self):
            return "https://example.com"

        @field
        def headers(self):
            return [Header(name="Foo", value="")]

    page = BodySpaceSearchRequestTemplatePage(RequestUrl("https://example.com"))
    search_request_template = await page.to_item()
    search_request = search_request_template.request(query="foo bar")
    assert search_request.headers == [Header(name="Foo", value="")]


class KeywordSearchRequestTemplatePage(BaseSearchRequestTemplatePage):
    @field
    def url(self):
        return "https://example.com/?search={{ keyword }}"


@pytest.mark.asyncio
async def test_request_no_parameters():
    page = VerbatimSearchRequestTemplatePage(RequestUrl("https://example.com"))
    search_request_template = await page.to_item()
    with pytest.raises(TypeError):
        search_request_template.request()


@pytest.mark.asyncio
async def test_request_template_keyword_call_keyword():
    page = KeywordSearchRequestTemplatePage(RequestUrl("https://example.com"))
    search_request_template = await page.to_item()
    with (
        pytest.warns(
            DeprecationWarning, match=r"Replace the 'keyword' variable with 'query'"
        ),
        pytest.warns(
            DeprecationWarning,
            match=r"The 'keyword' parameter of request\(\) is deprecated",
        ),
    ):
        search_request = search_request_template.request(keyword="foo")
    assert search_request.url == "https://example.com/?search=foo"


@pytest.mark.asyncio
async def test_request_template_keyword_call_query():
    page = KeywordSearchRequestTemplatePage(RequestUrl("https://example.com"))
    search_request_template = await page.to_item()
    with pytest.warns(
        DeprecationWarning, match=r"Replace the 'keyword' variable with 'query'"
    ):
        search_request = search_request_template.request(query="foo")
    assert search_request.url == "https://example.com/?search=foo"


@pytest.mark.asyncio
async def test_request_template_query_call_keyword():
    page = VerbatimSearchRequestTemplatePage(RequestUrl("https://example.com"))
    search_request_template = await page.to_item()
    with pytest.warns(
        DeprecationWarning,
        match=r"The 'keyword' parameter of request\(\) is deprecated",
    ):
        search_request = search_request_template.request(keyword="foo")
    assert search_request.url == "https://example.com/?search=foo"


@pytest.mark.asyncio
async def test_request_keyword_and_query_same():
    page = VerbatimSearchRequestTemplatePage(RequestUrl("https://example.com"))
    search_request_template = await page.to_item()
    with pytest.warns(
        DeprecationWarning,
        match=r"The 'keyword' parameter of request\(\) is deprecated",
    ):
        search_request = search_request_template.request(query="foo", keyword="foo")
    assert search_request.url == "https://example.com/?search=foo"


@pytest.mark.asyncio
async def test_request_keyword_and_query_different():
    page = VerbatimSearchRequestTemplatePage(RequestUrl("https://example.com"))
    search_request_template = await page.to_item()
    with pytest.warns(DeprecationWarning, match=r"overrides the value of"):
        search_request = search_request_template.request(query="foo", keyword="bar")
    assert search_request.url == "https://example.com/?search=foo"
