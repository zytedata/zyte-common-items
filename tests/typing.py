from typing import List, Optional, Tuple, Union, get_args  # noqa

import attrs


def optional_type(cls):
    """If cls is Optional[X] it returns X else returns None.

    >>> optional_type(Optional[str])
    <class 'str'>
    >>> optional_type(Union[str, int])
    >>> optional_type(str)
    """
    types = [t for t in get_args(cls) if not issubclass(t, type(None))]
    if len(types) == 1:
        return types[0]


def get_generic_type(cls):
    """Return the type of generics (e.g. Offer for List[Offer]).

    >>> get_generic_type(list)
    >>> get_generic_type(List[str])
    <class 'str'>
    >>> get_generic_type(Tuple[int])
    <class 'int'>
    """
    args = get_args(cls)
    if args and len(args) == 1:
        return args[0]


def assert_type_compliance(item, cls=None, attrib=None):
    """
    Assert recursively that the values of the attributes of an attrs
    item are as defined
    """
    item_cls = cls or type(item)
    if cls and not isinstance(item, cls):
        raise AssertionError(
            f"Expecting an instance of type {cls} in attribute {attrib} "
            f"but {type(item)} were received instead"
        )
    if not attrs.has(item_cls):
        return
    for name, field in attrs.fields_dict(item_cls).items():
        value = getattr(item, name)
        if isinstance(value, (list, tuple)):
            expected_cls = get_generic_type(field.type)
            for v in value:
                assert_type_compliance(v, expected_cls, name)
        elif value:
            type_ = optional_type(field.type) or field.type
            assert_type_compliance(value, type_, name)
