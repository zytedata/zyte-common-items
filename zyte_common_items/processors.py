from collections.abc import Iterable
from functools import wraps
from typing import Any, Callable, List, Optional, Union

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


def _handle_selectorlist(value: Any) -> Any:
    if not isinstance(value, SelectorList):
        return value
    if len(value) == 0:
        return None
    return value[0]


def only_handle_nodes(
    f: Callable[[Union[Selector, HtmlElement], Any], Any]
) -> Callable[[Any, Any], Any]:
    @wraps(f)
    def wrapper(value: Any, page: Any) -> Any:
        value = _handle_selectorlist(value)
        if not isinstance(value, (Selector, HtmlElement)):
            return value
        result = f(value, page)
        return result

    return wrapper


def breadcrumbs_processor(value: Any, page: Any) -> Any:
    """Convert the data into a list of :class:`~zyte_common_items.Breadcrumb` objects if possible.

    Supported inputs are :class:`~parsel.selector.Selector`,
    :class:`~parsel.selector.SelectorList`, :class:`~lxml.html.HtmlElement` and
    an iterable of :class:`zyte_parsers.Breadcrumb` objects. Other inputs are
    returned as is.
    """

    def _from_zp_breadcrumb(value: zp_Breadcrumb) -> Breadcrumb:
        return Breadcrumb(name=value.name, url=value.url)

    value = _handle_selectorlist(value)

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


@only_handle_nodes
def brand_processor(value: Union[Selector, HtmlElement], page: Any) -> Any:
    """Convert the data into a brand name if possible.

    Supported inputs are :class:`~parsel.selector.Selector`,
    :class:`~parsel.selector.SelectorList` and :class:`~lxml.html.HtmlElement`.
    Other inputs are returned as is.
    """
    return extract_brand_name(value, search_depth=2)


@only_handle_nodes
def price_processor(value: Union[Selector, HtmlElement], page: Any) -> Any:
    """Convert the data into a price string if possible.

    Uses the price-parser_ library.

    Supported inputs are :class:`~parsel.selector.Selector`,
    :class:`~parsel.selector.SelectorList` and :class:`~lxml.html.HtmlElement`.
    Other inputs are returned as is.

    Puts the parsed Price object into ``page._parsed_price``.

    .. _price-parser: https://github.com/scrapinghub/price-parser
    """
    price = extract_price(value)
    page._parsed_price = price
    if price.amount is None:
        return None
    return str(price.amount)


@only_handle_nodes
def simple_price_processor(value: Union[Selector, HtmlElement], page: Any) -> Any:
    """Convert the data into a price string if possible.

    Uses the price-parser_ library.

    Supported inputs are :class:`~parsel.selector.Selector`,
    :class:`~parsel.selector.SelectorList` and :class:`~lxml.html.HtmlElement`.
    Other inputs are returned as is.

    .. _price-parser: https://github.com/scrapinghub/price-parser
    """
    price = extract_price(value)
    if price.amount is None:
        return None
    return str(price.amount)
