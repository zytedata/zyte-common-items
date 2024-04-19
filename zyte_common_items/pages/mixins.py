import html
from typing import Any, Generic, Optional, Type, Union

import html_text
from clear_html import cleaned_node_to_text
from lxml.html import HtmlElement
from price_parser import Price
from web_poet.fields import FieldsMixin, field
from web_poet.utils import ensure_awaitable, get_generic_param

from zyte_common_items.components import MetadataT


class HasMetadata(Generic[MetadataT]):
    """Inherit from this generic mixin to set the metadata class used by a page
    class."""

    @property
    def metadata_cls(self) -> Optional[Type[MetadataT]]:
        """Metadata class."""
        return _get_metadata_class(type(self))


def _get_metadata_class(cls: type) -> Optional[Type[MetadataT]]:
    return get_generic_param(cls, HasMetadata)


class PriceMixin(FieldsMixin):
    """Provides price-related field implementations."""

    _parsed_price: Optional[Price] = None

    async def _get_parsed_price(self) -> Optional[Price]:
        if self._parsed_price is None:
            # the price field wasn't executed or doesn't write _parsed_price
            price = getattr(self, "price", None)
            price = await ensure_awaitable(price)
            if self._parsed_price is None:
                # the price field doesn't write _parsed_price (or doesn't exist)
                self._parsed_price = Price(
                    amount=None, currency=None, amount_text=price
                )
        return self._parsed_price

    @field
    def currency(self) -> Optional[str]:
        return getattr(self, "CURRENCY", None)

    @field
    async def currencyRaw(self) -> Optional[str]:
        parsed_price = await self._get_parsed_price()
        if parsed_price:
            return parsed_price.currency
        return None


class DescriptionMixin(FieldsMixin):
    """Provides description and descriptionHtml field implementations."""

    UNSET = object()

    _descriptionHtml_node: Any = UNSET
    _description_node: Any = UNSET
    _description_str: Any = UNSET

    _description_default = False
    _descriptionHtml_default = False

    @staticmethod
    def wrap_description_into_html(description: str) -> str:
        r"""Convert plain text into an article HTML.

        The format tries to match clear_html.cleaned_node_to_html().

        >>> DescriptionMixin.wrap_description_into_html('')
        '<article>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('foo')
        '<article>\n\n<p>foo</p>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('foo\nbar')
        '<article>\n\n<p>foo</p>\n\n<p>bar</p>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('foo\n\nbar')
        '<article>\n\n<p>foo</p>\n\n<p>bar</p>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('\nfoo\n\nbar\n')
        '<article>\n\n<p>foo</p>\n\n<p>bar</p>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('foo\nbar\n\nbaz\n')
        '<article>\n\n<p>foo</p>\n\n<p>bar</p>\n\n<p>baz</p>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('2>1')
        '<article>\n\n<p>2&gt;1</p>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('<p>')
        '<article>\n\n<p>&lt;p&gt;</p>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('&lt;p&gt;')
        '<article>\n\n<p>&amp;lt;p&amp;gt;</p>\n\n</article>'
        """
        paras_wrapped = [
            f"\n<p>{html.escape(para)}</p>\n"
            for para in description.split("\n")
            if para
        ]
        return f"<article>\n{''.join(paras_wrapped)}\n</article>"

    async def _get_description(self) -> Optional[str]:
        if self._description_default:
            return None
        if self._description_str == self.UNSET:
            description = await ensure_awaitable(self.description)
            if self._description_str == self.UNSET:
                # the description field doesn't write _description_str
                self._description_str = description
        return self._description_str

    async def _get_description_html(self) -> Optional[HtmlElement]:
        if self._descriptionHtml_default:
            return None
        if self._descriptionHtml_node == self.UNSET:
            descriptionHtml = await ensure_awaitable(self.descriptionHtml)
            if self._descriptionHtml_node == self.UNSET:
                # the descriptionHtml field doesn't write _descriptionHtml_node
                self._descriptionHtml_node = descriptionHtml
        return self._descriptionHtml_node

    @field
    async def description(self) -> Optional[str]:
        self._description_default = True
        description_html = await self._get_description_html()
        if isinstance(description_html, HtmlElement):
            return cleaned_node_to_text(description_html)
        if isinstance(description_html, str):
            return html_text.extract_text(description_html)
        return None

    @field
    async def descriptionHtml(self) -> Union[HtmlElement, str, None]:
        self._descriptionHtml_default = True
        description = await self._get_description()
        if self._description_node not in {self.UNSET, None}:
            # we can use the element provided by the description field
            return self._description_node
        if isinstance(description, str):
            return self.wrap_description_into_html(description)
        return None
