import warnings
from typing import Any, Callable, Dict, Optional, Tuple, Type, TypeVar
from warnings import warn
from weakref import WeakKeyDictionary

import attrs

# backwards compatibility imports
from ._dateutils import format_datetime  # noqa: F401
from .converters import MetadataCaster, url_to_str  # noqa: F401

# Caches the attribute names for attr.s classes.
_CLASS_ATTRS: WeakKeyDictionary = WeakKeyDictionary()


def split_in_unknown_and_known_fields(
    data: Optional[dict], item_cls: Type
) -> Tuple[Dict, Dict]:
    """
    Return a pair of dicts. The first one contains those elements not belonging to the
    attr class ``item_cls``. The second one contains the rest. That is, those
    attributes not belonging to ``item_cls`` class
    """
    data = data or {}
    if not attrs.has(item_cls):
        raise ValueError(f"The cls {item_cls} is not attrs class")
    if item_cls not in _CLASS_ATTRS:
        _CLASS_ATTRS[item_cls] = {field.name for field in attrs.fields(item_cls)}
    unknown, known = split_dict(data, lambda k: k in _CLASS_ATTRS[item_cls])
    return unknown, known


def split_dict(dict: Dict, key_pred: Callable[[Any], Any]) -> Tuple[Dict, Dict]:
    """Splits the dictionary in two.

    The first dict contains the records for which the key predicate is False
    and the second dict contains the rest.

    >>> split_dict({}, lambda k: False)
    ({}, {})
    >>> split_dict(dict(a=1, b=2, c=3), lambda k: k != 'a')
    ({'a': 1}, {'b': 2, 'c': 3})
    """  # noqa
    yes, no = {}, {}
    for k, v in dict.items():
        if key_pred(k):
            yes[k] = v
        else:
            no[k] = v
    return (no, yes)


NewClassT = TypeVar("NewClassT", bound=attrs.AttrsInstance)


def convert_to_class(value: Any, new_cls: Type[NewClassT]) -> NewClassT:
    """Convert *value* into *type* keeping all shared attributes, and
    triggering a run-time warning if any attribute is removed."""
    if type(value) is new_cls:
        return value
    input_attributes = {attribute.name for attribute in attrs.fields(value.__class__)}
    output_attributes = {attribute.name for attribute in attrs.fields(new_cls)}
    shared_attributes = input_attributes & output_attributes
    new_value = new_cls(
        **{attribute: getattr(value, attribute) for attribute in shared_attributes}
    )
    removed_nonempty_attributes = {
        attribute
        for attribute in (input_attributes - output_attributes)
        if getattr(value, attribute)
        != attrs.fields_dict(value.__class__)[attribute].default
    }
    if removed_nonempty_attributes:
        warn(
            (
                f"Conversion of {value} into {new_cls} is dropping the non-default "
                f"values of the following attributes: "
                f"{removed_nonempty_attributes}."
            ),
            RuntimeWarning,
        )
    return new_value


def metadata_processor(metadata, page):
    from zyte_common_items.processors import metadata_processor

    warnings.warn(
        "zyte_common_items.util.metadata_processor is moved to"
        "zyte_common_items.processors.metadata_processor",
        DeprecationWarning,
        stacklevel=2,
    )
    return metadata_processor(metadata, page)
