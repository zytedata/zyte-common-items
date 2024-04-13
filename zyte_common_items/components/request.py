import base64
from typing import List, Optional, Type, TypeVar

import attrs

from zyte_common_items.base import Item, ProbabilityMixin
from zyte_common_items.components.metadata import ProbabilityMetadata
from zyte_common_items.util import convert_to_class, url_to_str


@attrs.define(kw_only=True)
class Header(Item):
    """An HTTP header"""

    #: Name of the header
    name: str

    #: Value of the header
    value: str


@attrs.define(slots=False)
class Request(Item):
    """Describe a web request to load a page"""

    #: HTTP URL
    url: str = attrs.field(converter=url_to_str)

    #: HTTP method
    method: str = "GET"

    #: HTTP request body, Base64-encoded
    body: Optional[str] = None

    #: HTTP headers
    headers: Optional[List[Header]] = None

    #: Name of the page being requested.
    name: Optional[str] = None

    _body_bytes = None

    @property
    def body_bytes(self) -> Optional[bytes]:
        """Request.body as bytes"""
        # todo: allow to set body bytes in __init__, to avoid encoding/decoding.
        if self._body_bytes is None:
            if self.body is not None:
                self._body_bytes = base64.b64decode(self.body)
        return self._body_bytes

    def to_scrapy(self, callback, **kwargs):
        """
        Convert a request to scrapy.Request.
        All kwargs are passed to scrapy.Request as-is.
        """
        import scrapy

        header_list = [(header.name, header.value) for header in self.headers or []]

        return scrapy.Request(
            url=self.url,
            callback=callback,
            method=self.method or "GET",
            headers=header_list,
            body=self.body_bytes,
            **kwargs,
        )


@attrs.define(kw_only=True)
class ProbabilityRequest(Request, ProbabilityMixin):
    """A :class:`Request` that includes a probability value."""

    #: Data extraction process metadata.
    metadata: Optional[ProbabilityMetadata] = None


RequestT = TypeVar("RequestT", bound=Request)


def cast_request(value: Request, cls: Type[RequestT]) -> RequestT:
    """Convert *value*, an instance of :class:`Request` or a subclass, into
    *cls*, a different class that is also either :class:`Request` or a
    subclass."""
    new_value = convert_to_class(value, cls)
    if type(value) is Request and cls is ProbabilityRequest:
        new_value.metadata = ProbabilityMetadata(probability=1.0)
    return new_value


def request_list_processor(request_list: List[Request]) -> List[ProbabilityRequest]:
    """Convert all objects in *request_list*, which are instances of
    :class:`Request` or a subclass, into instances of
    :class:`ProbabilityRequest`."""
    return [cast_request(request, ProbabilityRequest) for request in request_list]


class RequestListCaster:
    """attrs converter to turn lists of :class:`Request` instances into lists
    of :class:`ProbabilityRequest` instances."""

    def __init__(self, target):
        self._target = target

    def __call__(self, value):
        return [cast_request(item, self._target) for item in value]
