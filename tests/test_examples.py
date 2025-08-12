from typing import Any

import pytest
from web_poet import HttpResponse, WebPage

from zyte_common_items._examples import (
    _BREADCRUMBS_EXAMPLE_1,
    _BREADCRUMBS_EXAMPLE_2,
    _DESCRIPTION_HTML_EXAMPLE,
    _GTIN_EXAMPLE_1,
    _GTIN_EXAMPLE_2,
    _GTIN_EXAMPLE_3,
    PageObjectMethodExample,
)


@pytest.mark.parametrize(
    "example",
    (
        _BREADCRUMBS_EXAMPLE_1,
        _BREADCRUMBS_EXAMPLE_2,
        _DESCRIPTION_HTML_EXAMPLE,
        _GTIN_EXAMPLE_1,
        _GTIN_EXAMPLE_2,
        _GTIN_EXAMPLE_3,
    ),
)
def test(example: PageObjectMethodExample):
    response = HttpResponse(url="http://example.com", body=example.html.encode())
    page: WebPage = WebPage(response=response)

    global_ns: dict[str, Any] = {}
    for imp in example.imports:
        exec(imp, global_ns)
    exec(example.source_code, global_ns)

    method = global_ns["extract"]
    output = method(page)

    assert output == example.expected
