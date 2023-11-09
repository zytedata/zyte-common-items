"""The ``Item`` class should be used as the parent class for data containers."""

from collections import ChainMap
from typing import Dict, List, Optional, Union, get_args, get_origin

import attrs

from .util import split_in_unknown_and_known_fields

_Trail = Optional[str]


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


def _extend_trail(trail: _Trail, key: Union[int, str]):
    if isinstance(key, str):
        if not trail:
            trail = key
        else:
            trail += f".{key}"
    else:
        assert isinstance(key, int)
        item = f"[{key}]"
        if not trail:
            trail = item
        else:
            trail += item
    return trail


@attrs.define
class ProbabilityMixin:
    """Provides :meth:`get_probability` to make it easier to access the
    probability of an item or item component that is nested under its metadata
    attribute."""

    def get_probability(self) -> Optional[float]:
        """Returns the item probability if available, otherwise ``None``."""
        if metadata := getattr(self, "metadata", None):
            return getattr(metadata, "probability", None)
        return None


@attrs.define
class Item(ProbabilityMixin, _ItemBase):
    """Base class for :ref:`items <items>`."""

    def __attrs_post_init__(self):
        self._unknown_fields_dict = {}

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        """Read an item from a dictionary."""
        return cls._from_dict(item)

    @classmethod
    def _from_dict(cls, item: Optional[Dict], *, trail: _Trail = None):
        """Read an item from a dictionary."""
        if not item:
            return None

        if not isinstance(item, dict):
            path = _get_import_path(cls)
            if not trail:
                prefix = "Expected"
            else:
                prefix = f"Expected {trail} to be"
            raise ValueError(f"{prefix} a dict with fields from {path}, got {item!r}.")

        item = cls._apply_field_types_to_sub_fields(item, trail=trail)
        unknown_fields, known_fields = split_in_unknown_and_known_fields(item, cls)
        obj = cls(**known_fields)  # type: ignore
        obj._unknown_fields_dict = unknown_fields
        return obj

    @classmethod
    def from_list(cls, items: Optional[List[Dict]], *, trail: _Trail = None) -> List:
        """Read items from a list."""
        return cls._from_list(items)

    @classmethod
    def _from_list(cls, items: Optional[List[Dict]], *, trail: _Trail = None) -> List:
        """Read items from a list."""
        result = []
        for index, item in enumerate(items or []):
            index_trail = _extend_trail(trail, index)
            result.append(cls._from_dict(item, trail=index_trail))
        return result

    @classmethod
    def _apply_field_types_to_sub_fields(cls, item: Dict, trail: _Trail = None):
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
                    path = f"{_get_import_path(cls)}.{field}"
                    raise ValueError(
                        f"{path} is annotated with {type_annotation}. Fields "
                        f"should only be annotated with one type (or "
                        f"optional)."
                    )
                is_optional = len(field_classes) == 2 and isinstance(
                    None, field_classes[1]
                )
                type_annotation = field_classes[0]
                origin = get_origin(type_annotation)

            if origin is list:
                value = item.get(field)
                if not isinstance(value, list) and not (is_optional and value is None):
                    field_trail = _extend_trail(trail, field)
                    raise ValueError(
                        f"Expected {field_trail} to be a list, got " f"{value!r}."
                    )
                type_annotation = get_args(type_annotation)[0]
                if is_data_container(type_annotation):
                    from_list[field] = type_annotation
            elif is_data_container(type_annotation):
                from_dict[field] = type_annotation

        if from_dict or from_list:
            item = dict(**item)
            for key, cls in (from_dict or {}).items():
                key_trail = _extend_trail(trail, key)
                value = item.get(key)
                if value is not None and not isinstance(value, dict):
                    path = _get_import_path(cls)
                    raise ValueError(
                        f"Expected {key_trail} to be a dict with fields "
                        f"from {path}, got {value!r}."
                    )
                item[key] = cls._from_dict(value, trail=key_trail)
            for key, cls in (from_list or {}).items():
                key_trail = _extend_trail(trail, key)
                value = item.get(key)
                if value is not None and not isinstance(value, list):
                    path = _get_import_path(cls)
                    raise ValueError(
                        f"Expected {key_trail} to be a list of dicts "
                        f"with fields from {path}, got {value!r}."
                    )
                item[key] = cls._from_list(value, trail=key_trail)

        return item
