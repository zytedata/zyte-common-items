"""
A module with common attrs converters
"""

from typing import Type

import attrs

from zyte_common_items.components import MetadataT, ProbabilityRequest


class RequestListCaster:
    """attrs converter to turn lists of :class:`Request` instances into lists
    of ``target`` instances."""

    def __init__(self, target):
        self._target = target

    def __call__(self, value):
        return [item.cast(self._target) for item in value]


class MetadataCaster:
    """attrs converter that converts an input metadata object into the metadata
    class declared by the container page object class."""

    def __init__(self, target: Type[MetadataT]):
        self._target = target

    def __call__(self, value: MetadataT) -> MetadataT:
        return value.cast(self._target)


to_probability_request_list = RequestListCaster(ProbabilityRequest)
to_probability_request_list_optional = attrs.converters.optional(
    to_probability_request_list
)


def to_metadata(metadata_cls: Type[MetadataT]):
    return MetadataCaster(metadata_cls)


def to_metadata_optional(metadata_cls: Type[MetadataT]):
    return attrs.converters.optional(MetadataCaster(metadata_cls))
