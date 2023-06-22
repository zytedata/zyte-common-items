from typing import Any, List

from lxml.html import HtmlElement
from parsel import Selector
from zyte_parsers import Breadcrumb as zp_Breadcrumb
from zyte_parsers import extract_breadcrumbs

from .items import Breadcrumb


def breadcrumbs_processor(value: Any, page: Any) -> Any:
    def _from_zp_breadcrumb(value: zp_Breadcrumb) -> Breadcrumb:
        return Breadcrumb(name=value.name, url=value.url)

    if isinstance(value, (Selector, HtmlElement)):
        base_url = getattr(page, "url", None)
        zp_breadcrumbs = extract_breadcrumbs(value, base_url=base_url)
        return (
            [_from_zp_breadcrumb(b) for b in zp_breadcrumbs] if zp_breadcrumbs else None
        )

    if not isinstance(value, list):
        return value

    results: List[Any] = []
    for item in value:
        if isinstance(item, zp_Breadcrumb):
            results.append(_from_zp_breadcrumb(item))
        else:
            results.append(item)
    return results
