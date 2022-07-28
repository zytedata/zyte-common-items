"""The ``Item`` class should be used as the parent class for data containers."""

from collections import ChainMap

try:
    from typing import get_args
except ImportError:
    # Compliance with python 3.7
    from zyte_common_items.util import get_args

try:
    from typing import get_origin
except ImportError:
    # Compliance with python 3.7
    from zyte_common_items.util import get_origin

from typing import Dict, List, Optional, Union

import attrs

from zyte_common_items.util import split_in_unknown_and_known_fields


def is_data_container(cls_or_obj):
    """Used for discerning classes/instances if they are part of the Zyte Common
    Item definitions.
    """
    try:
        return issubclass(cls_or_obj, Item)
    except TypeError:
        # must be an instance rather than a class
        return isinstance(cls_or_obj, Item)


class _ItemBase:
    # Reserving an slot for _unknown_fields_dict.
    # This is done in a base class because otherwise attr.s won't pick it up
    __slots__ = ("_unknown_fields_dict",)


@attrs.define
class Item(_ItemBase):
    def __attrs_post_init__(self):
        self._unknown_fields_dict = {}

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        """Read an item from a dictionary."""
        if not item:
            return None

        item = cls._apply_field_types_to_sub_fields(item)
        unknown_fields, known_fields = split_in_unknown_and_known_fields(item, cls)
        obj = cls(**known_fields)  # type: ignore
        obj._unknown_fields_dict = unknown_fields
        return obj

    @classmethod
    def from_list(cls, items: Optional[List[Dict]]) -> List:
        """Read items from a list."""
        return [cls.from_dict(item) for item in items or []]

    @classmethod
    def _apply_field_types_to_sub_fields(cls, item: Dict):
        """This applies the correct data container class for some of the fields
        that need them.

        Specifically, this traverses recursively each field to determine the proper
        data container class based on the type annotations. This could handle both
        ``list`` and ``object`` type requirements. For example:

            * Article having ``breadcrumbs: List[Breadcrumb]``
            * Product having ``brand: Optional[Brand]``

        Moreover, fields that are not defined to be part of data container
        classes will be ignored. For example:

            * Article having ``headline: Optional[str]``
            * Product having ``name: Optional[str]``
        """
        from_dict, from_list = {}, {}

        annotations = ChainMap(*(c.__annotations__ for c in cls.__mro__ if "__annotations__" in c.__dict__))

        for field, type_annotation in annotations.items():
            origin = get_origin(type_annotation)
            if origin == Union:
                field_classes = get_args(type_annotation)
                if len(field_classes) != 2 or not isinstance(None, field_classes[1]):
                    raise ValueError("Field should only be annotated with one type (or optional).")
                type_annotation = field_classes[0]
                origin = get_origin(type_annotation)

            if origin is list:
                type_annotation = get_args(type_annotation)[0]
                if is_data_container(type_annotation):
                    from_list[field] = type_annotation
            elif is_data_container(type_annotation):
                from_dict[field] = type_annotation

        if from_dict or from_list:
            item = dict(**item)
            item.update({key: cls.from_dict(item.get(key)) for key, cls in (from_dict or {}).items()})
            item.update({key: cls.from_list(item.get(key, [])) for key, cls in (from_list or {}).items()})

        return item
