"""The ``Item`` class should be used as the parent class for data containers."""

from collections import ChainMap

try:
    from typing import get_args
except ImportError:
    # Compliance with python 3.7
    from .util import get_args

try:
    from typing import get_origin
except ImportError:
    # Compliance with python 3.7
    from .util import get_origin

from typing import Dict, List, Optional, Union

import attrs

from .util import split_in_unknown_and_known_fields

Breadcrumbs = Optional[str]


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


def _get_import_path(obj: type):
    return f"{obj.__module__}.{obj.__qualname__}"


def _extend_breadcrumbs(breadcrumbs: Optional[str], key: Union[int, str]):
    if isinstance(key, str):
        if not breadcrumbs:
            breadcrumbs = key
        else:
            breadcrumbs += f".{key}"
    else:
        assert isinstance(key, int)
        item = f"[{key}]"
        if not breadcrumbs:
            breadcrumbs = item
        else:
            breadcrumbs += item
    return breadcrumbs


@attrs.define
class Item(_ItemBase):
    def __attrs_post_init__(self):
        self._unknown_fields_dict = {}

    @classmethod
    def from_dict(cls, item: Optional[Dict], *, breadcrumbs: Breadcrumbs = None):
        """Read an item from a dictionary."""
        if not item:
            return None

        if not isinstance(item, dict):
            path = _get_import_path(cls)
            if not breadcrumbs:
                prefix = "Expected"
            else:
                prefix = f"Expected {breadcrumbs} to be"
            raise ValueError(f"{prefix} a dict with fields from {path}, got {item!r}.")

        item = cls._apply_field_types_to_sub_fields(item, breadcrumbs=breadcrumbs)
        unknown_fields, known_fields = split_in_unknown_and_known_fields(item, cls)
        obj = cls(**known_fields)  # type: ignore
        obj._unknown_fields_dict = unknown_fields
        return obj

    @classmethod
    def from_list(
        cls, items: Optional[List[Dict]], *, breadcrumbs: Breadcrumbs = None
    ) -> List:
        """Read items from a list."""
        result = []
        for index, item in enumerate(items or []):
            index_breadcrumbs = _extend_breadcrumbs(breadcrumbs, index)
            result.append(cls.from_dict(item, breadcrumbs=index_breadcrumbs))
        return result

    @classmethod
    def _apply_field_types_to_sub_fields(
        cls, item: Dict, breadcrumbs: Breadcrumbs = None
    ):
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

        annotations = ChainMap(
            *(c.__annotations__ for c in cls.__mro__ if "__annotations__" in c.__dict__)
        )
        for field, type_annotation in annotations.items():
            origin = get_origin(type_annotation)
            is_optional = False
            if origin == Union:
                field_classes = get_args(type_annotation)
                if len(field_classes) != 2 or not isinstance(None, field_classes[1]):
                    field_breadcrumbs = f"{_get_import_path(cls)}.{field}"
                    raise ValueError(
                        f"{field_breadcrumbs} is annotated with "
                        f"{type_annotation}. Fields should only be annotated "
                        f"with one type (or optional)."
                    )
                if len(field_classes) == 2 and isinstance(None, field_classes[1]):
                    is_optional = True
                type_annotation = field_classes[0]
                origin = get_origin(type_annotation)

            if origin is list:
                value = item.get(field)
                if not isinstance(value, list) and not (is_optional and value is None):
                    field_breadcrumbs = _extend_breadcrumbs(breadcrumbs, field)
                    raise ValueError(
                        f"Expected {field_breadcrumbs} to be a list, got " f"{value!r}."
                    )
                type_annotation = get_args(type_annotation)[0]
                if is_data_container(type_annotation):
                    from_list[field] = type_annotation
            elif is_data_container(type_annotation):
                from_dict[field] = type_annotation

        if from_dict or from_list:
            item = dict(**item)
            for key, cls in (from_dict or {}).items():
                key_breadcrumbs = _extend_breadcrumbs(breadcrumbs, key)
                value = item.get(key)
                if value is not None and not isinstance(value, dict):
                    path = _get_import_path(cls)
                    raise ValueError(
                        f"Expected {key_breadcrumbs} to be a dict with fields "
                        f"from {path}, got {value!r}."
                    )
                item[key] = cls.from_dict(value, breadcrumbs=key_breadcrumbs)
            for key, cls in (from_list or {}).items():
                key_breadcrumbs = _extend_breadcrumbs(breadcrumbs, key)
                value = item.get(key)
                if value is not None and not isinstance(value, list):
                    path = _get_import_path(cls)
                    raise ValueError(
                        f"Expected {key_breadcrumbs} to be a list of dicts "
                        f"with fields from {path}, got {value!r}."
                    )
                item[key] = cls.from_list(value, breadcrumbs=key_breadcrumbs)

        return item
