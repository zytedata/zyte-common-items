"""
A module with common attrs converters
"""

from typing import Optional, Union

import attrs
from web_poet.page_inputs.url import _Url


def url_to_str(url: Union[str, _Url]) -> str:
    """Return the input :class:`~web_poet.page_inputs.http.RequestUrl` or
    :class:`~web_poet.page_inputs.http.ResponseUrl` object as a string."""

    if not isinstance(url, (str, _Url)):
        raise ValueError(
            f"{url!r} is neither a string nor an instance of RequestUrl or ResponseUrl."
        )
    return str(url)


def url_to_str_optional(url: Union[str, _Url, None]) -> Optional[str]:
    """Return the input :class:`~web_poet.page_inputs.http.RequestUrl` or
    :class:`~web_poet.page_inputs.http.ResponseUrl` object as a string, or
    None if url is None."""
    if url is None:
        return None
    return url_to_str(url)


class MetadataCaster:
    """attrs converter that converts an input metadata object into the metadata
    class declared by the container page object class."""

    def __init__(self, target):
        self._target = target

    def __call__(self, value):
        return value.cast(self._target)


def to_probability_request_list(request_list):
    """attrs converter to turn lists of :class:`~scrapy.http.Request` instances into
    lists of :class:`~.ProbabilityRequest` instances."""
    from zyte_common_items.components import ProbabilityRequest

    return [request.cast(ProbabilityRequest) for request in request_list]


def to_probability_request_list_optional(request_list):
    """attrs converter to turn lists of :class:`~scrapy.http.Request` instances into
    lists of :class:`~.ProbabilityRequest` instances. If None is passed, None is
    returned."""
    if request_list is None:
        return None
    return to_probability_request_list(request_list)


def to_metadata(metadata_cls: type):
    return MetadataCaster(metadata_cls)


def to_metadata_optional(metadata_cls: type):
    return attrs.converters.optional(MetadataCaster(metadata_cls))
