from collections.abc import Iterable
from functools import wraps
from typing import Any, Callable, List, Optional, Union

from clear_html import clean_node, cleaned_node_to_html, cleaned_node_to_text
from lxml.html import HtmlElement
from parsel import Selector, SelectorList
from price_parser import Price
from web_poet.mixins import ResponseShortcutsMixin
from zyte_parsers import Breadcrumb as zp_Breadcrumb
from zyte_parsers import Gtin as zp_Gtin
from zyte_parsers import (
    extract_brand_name,
    extract_breadcrumbs,
    extract_gtin,
    extract_price,
    extract_rating,
    extract_review_count,
)

from . import AggregateRating, Gtin
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


def _format_price(price: Price) -> Optional[str]:
    """Return the price amount as a string, with a minimum of 2 decimal
    places."""
    if price.amount is None:
        return None
    *_, exponent = price.amount.as_tuple()
    if not isinstance(exponent, int):
        return None  # NaN, Infinity, etc.
    if exponent <= -2:
        return str(price.amount)
    return f"{price.amount:.2f}"


def only_handle_nodes(
    f: Callable[[Union[Selector, HtmlElement], Any], Any]
) -> Callable[[Any, Any], Any]:
    """Decorator for processors that only runs a decorated processor if the
    input is of type :class:`Selector` or :class:`HtmlElement`."""

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
    return _format_price(price)


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
    return _format_price(price)


@only_handle_nodes
def description_html_processor(value: Union[Selector, HtmlElement], page: Any) -> Any:
    """Convert the data into a cleaned up HTML if possible.

    Uses the clear-html_ library.

    Supported inputs are :class:`~parsel.selector.Selector`,
    :class:`~parsel.selector.SelectorList` and :class:`~lxml.html.HtmlElement`.
    Other inputs are returned as is.

    Puts the cleaned HtmlElement object into ``page._descriptionHtml_node``.

    .. _clear-html: https://github.com/zytedata/clear-html
    """
    if isinstance(value, Selector):
        value = value.root
    if value is None:
        return None
    assert isinstance(value, HtmlElement)
    cleaned_node = clean_node(value, _get_base_url(page))
    page._descriptionHtml_node = cleaned_node
    return cleaned_node_to_html(cleaned_node)


def description_processor(value: Any, page: Any) -> Any:
    """Convert the data into a cleaned up text if possible.

    Uses the clear-html_ library.

    Supported inputs are :class:`~parsel.selector.Selector`,
    :class:`~parsel.selector.SelectorList` and :class:`~lxml.html.HtmlElement`.
    Other inputs are returned as is.

    Puts the cleaned HtmlElement object into ``page._description_node`` and the
    cleaned text into ``page._description_str``.

    .. _clear-html: https://github.com/zytedata/clear-html
    """
    value = _handle_selectorlist(value)
    if isinstance(value, str):
        page._description_str = value
        return value
    if isinstance(value, Selector):
        value = value.root
    if value is None:
        return None
    assert isinstance(value, HtmlElement)
    cleaned_node = clean_node(value, _get_base_url(page))
    cleaned_text = cleaned_node_to_text(cleaned_node)
    page._description_node = cleaned_node
    page._description_str = cleaned_text
    return cleaned_text


def gtin_processor(
    value: Union[SelectorList, Selector, HtmlElement, str], page: Any
) -> Any:
    """Convert the data into a list of :class:`~zyte_common_items.Gtin` objects if possible.

    Supported inputs are :class:`str`, :class:`~parsel.selector.Selector`,
    :class:`~parsel.selector.SelectorList`, :class:`~lxml.html.HtmlElement`, an
    iterable of :class:`str` and an iterable of :class:`zyte_parsers.Gtin`
    objects.
    Other inputs are returned as is.
    """

    def _from_zp_gtin(zp_value: zp_Gtin) -> Gtin:
        return Gtin(type=zp_value.type, value=zp_value.value)

    results = []
    if isinstance(value, SelectorList):
        for sel in value:
            if result := extract_gtin(sel):
                results.append(_from_zp_gtin(result))
    elif isinstance(value, (Selector, HtmlElement, str)):
        if result := extract_gtin(value):
            results.append(_from_zp_gtin(result))
    elif isinstance(value, Iterable):
        for item in value:
            if isinstance(item, zp_Gtin):
                results.append(_from_zp_gtin(item))
            elif isinstance(item, str):
                results.append(_from_zp_gtin(extract_gtin(item)))
            else:
                results.append(item)
    else:
        return value
    return results or None


def rating_processor(value: Any, page: Any) -> Any:
    """Convert the data into an :class:`~zyte_common_items.AggregateRating`
    object if possible.

    Supported inputs are selector-like objects
    (:class:`~parsel.selector.Selector`,
    :class:`~parsel.selector.SelectorList`, or
    :class:`~lxml.html.HtmlElement`).

    The input can also be a dictionary with one or more of the
    :class:`~zyte_common_items.AggregateRating` fields as keys. The values for
    those keys can be either final values, to be assigned to the corresponding
    fields, or selector-like objects.

    If a returning dictionary is missing the ``bestRating`` field and
    ``ratingValue`` is a selector-like object, ``bestRating`` may be extracted.

    For example, for the following input HTML:

    .. code-block:: html

        <span class="rating">3.8 out of 5 stars</span>
        <a class="reviews">See all 7 reviews</a>

    You can use:

    .. code-block:: python

        @field
        def aggregateRating(self):
            return {
                "ratingValue": self.css(".rating"),
                "reviewCount": self.css(".reviews"),
            }

    To get:

    .. code-block:: python

        AggregateRating(
            bestRating=5.0,
            ratingValue=3.8,
            reviewCount=7,
        )
    """
    value = _handle_selectorlist(value)
    if isinstance(value, (Selector, HtmlElement)):
        zp_rating = extract_rating(value)
        result = AggregateRating(
            reviewCount=extract_review_count(value),
            bestRating=zp_rating.bestRating,
            ratingValue=zp_rating.ratingValue,
        )
        if result.reviewCount or result.bestRating or result.ratingValue:
            return result
        return None
    elif isinstance(value, dict):
        result = AggregateRating()

        review_count = _handle_selectorlist(value.get("reviewCount"))
        if isinstance(review_count, (Selector, HtmlElement)):
            result.reviewCount = extract_review_count(review_count)
        elif review_count is not None:
            result.reviewCount = int(review_count)

        rating_value = _handle_selectorlist(value.get("ratingValue"))
        if isinstance(rating_value, (Selector, HtmlElement)):
            zp_rating = extract_rating(rating_value)
            result.ratingValue = zp_rating.ratingValue
            result.bestRating = zp_rating.bestRating
        elif rating_value is not None:
            result.ratingValue = float(rating_value)

        if (best_rating := value.get("bestRating")) is not None:
            result.bestRating = float(best_rating)

        if result.reviewCount or result.bestRating or result.ratingValue:
            return result
        return None
    return value
