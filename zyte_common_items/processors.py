from collections.abc import Iterable
from typing import Any, List, Optional

from lxml.html import HtmlElement
from parsel import Selector, SelectorList
from web_poet.mixins import ResponseShortcutsMixin
from zyte_parsers import Breadcrumb as zp_Breadcrumb
from zyte_parsers import extract_brand_name, extract_breadcrumbs, extract_price

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


def brand_processor(value: Any) -> Any:
    """Convert the data into a brand name if possible.

    Supported inputs are :class:`~parsel.selector.Selector`,
    :class:`~parsel.selector.SelectorList` and :class:`~lxml.html.HtmlElement`.
    Other inputs are returned as is.
    """

    if isinstance(value, SelectorList):
        if len(value) == 0:
            return None
        value = value[0]

    if isinstance(value, (Selector, HtmlElement)):
        return extract_brand_name(value, search_depth=2)

    return value


def price_processor(value: Any, page: Any) -> Any:
    """Convert the data into a price string if possible.

    Supported inputs are :class:`~parsel.selector.Selector`,
    :class:`~parsel.selector.SelectorList` and :class:`~lxml.html.HtmlElement`.
    Other inputs are returned as is.

    Puts the parsed Price object into ``page._parsed_price``.
    """

    if isinstance(value, SelectorList):
        if len(value) == 0:
            return None
        value = value[0]

    if isinstance(value, (Selector, HtmlElement)):
        price = extract_price(value)
        page._parsed_price = price
        if price.amount is None:
            return None
        return str(price.amount)

    return value


def simple_price_processor(value: Any) -> Any:
    """Convert the data into a price string if possible.

    Supported inputs are :class:`~parsel.selector.Selector`,
    :class:`~parsel.selector.SelectorList` and :class:`~lxml.html.HtmlElement`.
    Other inputs are returned as is.
    """

    if isinstance(value, SelectorList):
        if len(value) == 0:
            return None
        value = value[0]

    if isinstance(value, (Selector, HtmlElement)):
        price = extract_price(value)
        if price.amount is None:
            return None
        return str(price.amount)

    return value
