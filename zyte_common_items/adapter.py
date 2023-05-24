"""This module offers better integration with the itemadapter package."""
from types import MappingProxyType
from typing import Any, Collection, Iterator, KeysView

from itemadapter.adapter import AttrsAdapter

from zyte_common_items.base import Item


def _is_empty(value):
    """Return ``True`` if the value is to be considered empty for the purpose
    of excluding it from serialization.

    Empty values include: ``None``, empty collections (tuples, lists, etc.).

    Non-empty values include: empty ``bytes`` or ``str``, ``False``, ``0``.

    *value* is assumed not to be a mapping, which should be treated as a
    non-empty value, but this function would treat as an empty value.
    """
    return value is None or (
        not value
        and not isinstance(value, (bytes, str))
        and isinstance(value, Collection)
    )


class ZyteItemAdapter(AttrsAdapter):
    """Wrap an :ref:`item <items>` to interact with its content as if it was
    a dictionary.

    It can be :ref:`configured <configuration>` into itemadapter_ to improve
    interaction with :ref:`items <items>` for itemadapter users like Scrapy_.

    In extends AttrsAdapter_ with the following features:

    -   Allows interaction and serialization of fields from
        :attr:`~zyte_common_items.Item._unknown_fields_dict` as if they
        were regular item fields.

    -   Removes keys with empty values from the output of
        `ItemAdapter.asdict()`_, for a cleaner output.

    .. _AttrsAdapter: https://github.com/scrapy/itemadapter#built-in-adapters
    .. _itemadapter: https://github.com/scrapy/itemadapter#itemadapter
    .. _ItemAdapter.asdict(): https://github.com/scrapy/itemadapter#asdict---dict
    .. _Scrapy: https://scrapy.org/
    """

    @classmethod
    def is_item(cls, item: Any) -> bool:
        return isinstance(item, Item)

    def get_field_meta(self, field_name: str) -> MappingProxyType:
        if field_name in self._fields_dict:
            return self._fields_dict[field_name].metadata  # type: ignore
        elif field_name in self.item._unknown_fields_dict:
            return MappingProxyType({})
        raise KeyError(field_name)

    def field_names(self) -> KeysView:
        return KeysView({**self._fields_dict, **self.item._unknown_fields_dict})

    def __getitem__(self, field_name: str) -> Any:
        if field_name in self._fields_dict:
            return getattr(self.item, field_name)
        elif field_name in self.item._unknown_fields_dict:
            return self.item._unknown_fields_dict[field_name]
        raise KeyError(field_name)

    def __setitem__(self, field_name: str, value: Any) -> None:
        if field_name in self._fields_dict:
            setattr(self.item, field_name, value)
        else:
            self.item._unknown_fields_dict[field_name] = value

    def __delitem__(self, field_name: str) -> None:
        if field_name in self._fields_dict:
            del self._fields_dict[field_name]
            delattr(self.item, field_name)
        elif field_name in self.item._unknown_fields_dict:
            del self.item._unknown_fields_dict[field_name]
        else:
            raise KeyError(
                f"Object of type {self.item.__class__.__name__} does not contain a field with name {field_name}"
            )

    def __iter__(self) -> Iterator:
        fields = [
            attr
            for attr in self._fields_dict
            if not _is_empty(getattr(self.item, attr))
        ]
        fields.extend(
            attr
            for attr in self.item._unknown_fields_dict
            if not _is_empty(self.item._unknown_fields_dict[attr])
        )
        return iter(fields)


class ZyteItemKeepEmptyAdapter(ZyteItemAdapter):
    """Similar to :class:`~.ZyteItemAdapter` but doesn't remove empty values.

    It is intended to be used in tests and other use cases where it's important
    to differentiate between empty and missing fields.
    """

    def __iter__(self) -> Iterator:
        fields = [attr for attr in self._fields_dict if hasattr(self.item, attr)]
        fields.extend(self.item._unknown_fields_dict)
        return iter(fields)
