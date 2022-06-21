"""The ``Item`` class should be used as the parent class for data containers."""

from datetime import datetime
from typing import Optional

import attrs

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

from zyte_common_items.util import export, split_in_unknown_and_known_fields


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


@export
@attrs.define(slots=True)
class Item(_ItemBase):
    def __attrs_post_init__(self):
        self._unknown_fields_dict = {}

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        """
        Read an item from a dictionary.

        Unknown attributes are kept in the dict ``_unknown_fields_dict``
        so that other item adapters later on can include them in the resultant
        item. This ensures it can support new fields from other sources even
        though this item library is not in sync.
        """
        if not item:
            return None

        item = cls._apply_field_types_to_sub_fields(item)
        unknown_fields, known_fields = split_in_unknown_and_known_fields(item, cls)
        obj = cls(**known_fields)  # type: ignore
        obj._unknown_fields_dict = unknown_fields
        return obj

    @classmethod
    def from_list(cls, items: Optional[List[Dict]]) -> List:
        """
        Read items from a list, invoking ``from_dict`` for each item in the list
        """
        return [cls.from_dict(item) for item in items or []]

    @classmethod
    def _apply_field_types_to_sub_fields(cls, item: Optional[Dict]):
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
        if not item:
            return None

        from_dict, from_list = {}, {}

        annotations = getattr(cls, "__annotations__", {})

        for field, type_annotation in annotations.items():
            origin = get_origin(type_annotation)

            if origin == list:
                from_list[field] = get_args(type_annotation)[0]

            elif origin == Union:
                field_classes = get_args(type_annotation)
                if len(field_classes) != 2 or not isinstance(None, field_classes[1]):
                    raise ValueError("Field should only be annotated with one type (or optional).")

                field_class = field_classes[0]

                # ignore classes like str, float, int etc
                if not is_data_container(field_class):
                    continue

                from_dict[field] = field_class

        if from_dict or from_list:
            item = dict(**item)
            item.update({key: cls.from_dict(item.get(key)) for key, cls in (from_dict or {}).items()})
            item.update({key: cls.from_list(item.get(key, [])) for key, cls in (from_list or {}).items()})

        return item


@export
@attrs.define(slots=True)
class AdditionalProperty:
    name: str
    value: str


@export
@attrs.define(slots=True, kw_only=True)
class AggregateRating:
    best_rating: Optional[float] = None
    rating_value: Optional[float] = None
    review_count: Optional[int] = None


@export
@attrs.define(slots=True)
class Brand:
    name: str


@export
@attrs.define(slots=True)
class Breadcrumb:
    name: str
    link: str


@export
@attrs.define(slots=True)
class Gtin:
    type: str
    value: str


@export
@attrs.define(slots=True)
class Image:
    data_url: Optional[str] = None
    url: Optional[str] = None


@export
@attrs.define(slots=True)
class Metadata:
    date_downloaded: datetime
    probability: Optional[float] = None
