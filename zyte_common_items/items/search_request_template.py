from base64 import b64encode
from typing import List, Optional
from urllib.parse import quote_plus

import attrs
import jinja2

from zyte_common_items.base import Item
from zyte_common_items.components import DetailsMetadata, Header, Request
from zyte_common_items.converters import to_metadata_optional

_TEMPLATE_ENVIRONMENT = jinja2.Environment()
_TEMPLATE_ENVIRONMENT.filters["quote_plus"] = quote_plus


def _render(string: str, **kwargs) -> str:
    return _TEMPLATE_ENVIRONMENT.from_string(string).render(**kwargs)


@attrs.define(kw_only=True)
class SearchRequestTemplateMetadata(DetailsMetadata):
    """Metadata class for :data:`zyte_common_items.SearchRequestTemplate.metadata`."""


@attrs.define(kw_only=True)
class SearchRequestTemplate(Item):
    """:ref:`Request template <request-templates>` to build a search
    :class:`~zyte_common_items.Request`."""

    #: :doc:`Jinja template <jinja:templates>` for :class:`Request.url
    #: <zyte_common_items.Request.url>`.
    url: str

    #: :doc:`Jinja template <jinja:templates>` for :class:`Request.method
    #: <zyte_common_items.Request.method>`.
    method: str = "GET"

    #: :doc:`Jinja template <jinja:templates>` for :class:`Request.body
    #: <zyte_common_items.Request.body>`.
    #:
    #: It must be a plain :class:`str`, not :class:`bytes` or a Base64-encoded
    #: :class:`str`. Base64-encoding is done by :meth:`request` after rendering
    #: this value as a Jinja template.
    #:
    #: Defining a non-UTF-8 body is not supported.
    body: Optional[str] = None

    #: List of :class:`Header`, for :class:`Request.headers
    #: <zyte_common_items.Request.headers>`, where every :attr:`~Header.name`
    #: and :attr:`~Header.value` is a :doc:`Jinja template <jinja:templates>`.
    #:
    #: When a header name template renders into an empty string (after
    #: stripping spacing), that header is removed from the resulting list of
    #: headers.
    headers: Optional[List[Header]] = None

    #: Data extraction process metadata.
    metadata: Optional[SearchRequestTemplateMetadata] = attrs.field(
        default=None, converter=to_metadata_optional(SearchRequestTemplateMetadata), kw_only=True  # type: ignore[misc]
    )

    def request(self, *, keyword: str) -> Request:
        """Return a :class:`~zyte_common_items.Request` to search for
        *keyword*."""
        body = _render(self.body or "", keyword=keyword).encode()

        headers = []
        for header in self.headers or []:
            name = _render(header.name, keyword=keyword).strip()
            if not name:
                continue
            value = _render(header.value, keyword=keyword)
            headers.append(Header(name=name, value=value))

        return Request(
            url=_render(self.url, keyword=keyword),
            method=_render(self.method, keyword=keyword),
            body=b64encode(body).decode() if body else None,
            headers=headers or None,
        )
