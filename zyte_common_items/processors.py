from collections.abc import Iterable
from typing import Any, List, Optional

from lxml.html import HtmlElement
from parsel import Selector, SelectorList
from web_poet.mixins import ResponseShortcutsMixin
from zyte_parsers import Breadcrumb as zp_Breadcrumb
from zyte_parsers import extract_breadcrumbs

from .items import Breadcrumb


def _get_base_url(page: Any) -> Optional[str]:
    if isinstance(page, ResponseShortcutsMixin):
        return page.base_url
    return getattr(page, "url", None)


def breadcrumbs_processor(value: Any, page: Any) -> Any:
    """Convert the data into a list of :class:`~zyte_common_items.Breadcrumb` objects if possible.

    Supported inputs are :class:`~parsel.selector.Selector`,
    :class:`~parsel.selector.SelectorList`, :class:`~lxml.html.HtmlElement` and
    an iterable of :class:`zyte_parsers.Breadcrumb` objects. Other inputs are
    returned as is.
    """

    def _from_zp_breadcrumb(value: zp_Breadcrumb) -> Breadcrumb:
        return Breadcrumb(name=value.name, url=value.url)

    if isinstance(value, SelectorList):
        if len(value) == 0:
            return None
        value = value[0]

    if isinstance(value, (Selector, HtmlElement)):
        zp_breadcrumbs = extract_breadcrumbs(value, base_url=_get_base_url(page))
        return (
            [_from_zp_breadcrumb(b) for b in zp_breadcrumbs] if zp_breadcrumbs else None
        )

    if not isinstance(value, Iterable) or isinstance(value, str):
        return value

    results: List[Any] = []
    for item in value:
        if isinstance(item, zp_Breadcrumb):
            results.append(_from_zp_breadcrumb(item))
        else:
            results.append(item)
    return results
