import base64
from typing import Optional, TypeVar

import attrs

from zyte_common_items.base import Item, ProbabilityMixin
from zyte_common_items.components.metadata import ProbabilityMetadata
from zyte_common_items.util import convert_to_class, url_to_str


@attrs.define(kw_only=True)
class Header(Item):
    """An HTTP header"""

    name: str
    """Name of the header."""

    value: str
    """Value of the header."""


RequestT = TypeVar("RequestT", bound="Request")
""":class:`~typing.TypeVar` for :class:`Request`."""


@attrs.define(slots=False)
class Request(Item):
    """Describe a web request to load a page"""

    url: str = attrs.field(converter=url_to_str)
    """HTTP URL."""

    method: str = "GET"
    """HTTP method."""

    body: Optional[str] = None
    """HTTP request body, Base64-encoded."""

    headers: Optional[list[Header]] = None
    """HTTP headers."""

    name: Optional[str] = None
    """Name of the page being requested."""

    _body_bytes = None

    @property
    def body_bytes(self) -> Optional[bytes]:
        """Request.body as bytes"""
        # todo: allow to set body bytes in __init__, to avoid encoding/decoding.
        if self._body_bytes is None and self.body is not None:
            self._body_bytes = base64.b64decode(self.body)
        return self._body_bytes

    def to_scrapy(self, callback, **kwargs):
        """Convert a request to scrapy.Request.
        All kwargs are passed to scrapy.Request as-is.
        """
        import scrapy  # noqa: PLC0415

        header_list = [(header.name, header.value) for header in self.headers or []]

        return scrapy.Request(
            url=self.url,
            callback=callback,
            method=self.method or "GET",
            headers=header_list,
            body=self.body_bytes,
            **kwargs,
        )

    def cast(self, cls: type[RequestT]) -> RequestT:
        """Convert *value*, an instance of :class:`~.Request` or a subclass, into
        *cls*, a different class that is also either :class:`~.Request` or a
        subclass."""
        new_value = convert_to_class(self, cls)
        if type(self) is Request and cls is ProbabilityRequest:
            new_value.metadata = ProbabilityMetadata(probability=1.0)  # type: ignore[attr-defined]
        return new_value


@attrs.define(kw_only=True)
class ProbabilityRequest(Request, ProbabilityMixin):
    """A :class:`Request` that includes a probability value."""

    metadata: Optional[ProbabilityMetadata] = None
    """Data extraction process metadata."""
