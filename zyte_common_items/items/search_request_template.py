from __future__ import annotations

from base64 import b64encode
from typing import Any, List, Optional
from urllib.parse import quote_plus
from warnings import warn

import attrs
import jinja2
from jinja2 import StrictUndefined
from jinja2.exceptions import UndefinedError

from zyte_common_items.base import Item
from zyte_common_items.components import DetailsMetadata, Header, Request
from zyte_common_items.converters import to_metadata_optional

_TEMPLATE_ENVIRONMENT = jinja2.Environment(undefined=StrictUndefined)
_TEMPLATE_ENVIRONMENT.filters["quote_plus"] = quote_plus
_UNSET = object()


def _render_query(template: str, query: str) -> str:
    parsed_template = _TEMPLATE_ENVIRONMENT.from_string(template)
    try:
        return parsed_template.render(query=query)
    except UndefinedError:
        warn(
            f"Replace the 'keyword' variable with 'query' on template {template!r}",
            DeprecationWarning,
            stacklevel=3,
        )
        return parsed_template.render(query=query, keyword=query)


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

    def request(
        self, *, query: str | Any = _UNSET, keyword: str | Any = _UNSET
    ) -> Request:
        """Return a :class:`~zyte_common_items.Request` to search for
        *keyword*."""
        if query is _UNSET:
            if keyword is _UNSET:
                raise TypeError(
                    "request() missing 1 required keyword-only argument: " "'query'"
                )
            else:
                query = keyword
                warn(
                    (
                        "The 'keyword' parameter of request() is deprecated, "
                        "use 'query' instead."
                    ),
                    DeprecationWarning,
                    stacklevel=2,
                )
        elif keyword is not _UNSET:
            if keyword == query:
                warn(
                    (
                        "The 'keyword' parameter of request() is deprecated, "
                        "use 'query' instead."
                    ),
                    DeprecationWarning,
                    stacklevel=2,
                )
            else:
                warn(
                    (
                        f"The 'keyword' parameter of request() is deprecated. "
                        f"The value of the 'query' parameter ({query!r}) "
                        f"overrides the value of the 'keyword' parameter "
                        f"({keyword!r})."
                    ),
                    DeprecationWarning,
                    stacklevel=2,
                )

        body = _render_query(self.body or "", query).encode()

        headers = []
        for header in self.headers or []:
            name = _render_query(header.name, query).strip()
            if not name:
                continue
            value = _render_query(header.value, query)
            headers.append(Header(name=name, value=value))

        return Request(
            url=_render_query(self.url, query),
            method=_render_query(self.method, query),
            body=b64encode(body).decode() if body else None,
            headers=headers or None,
        )
