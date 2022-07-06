from types import MappingProxyType
from typing import Any, Collection, Iterator, KeysView

from itemadapter.adapter import AttrsAdapter

from zyte_common_items.base import Item


def _is_empty(value):
    return value is None or (not value and not isinstance(value, (bytes, str)) and isinstance(value, Collection))


class ZyteItemAdapter(AttrsAdapter):
    """itemadapter adapter for zyte-common-items items.

    Configure it as early as possible in your code::

        from itemadapter import ItemAdapter
        from zyte_common_items import ZyteItemAdapter

        ItemAdapter.ADAPTER_CLASSES.appendleft(ZyteItemAdapter)

    This adapter:

    -   Allows interaction and serialization of fields not yet defined in the
        corresponding zyte-common-items item but received as input from Zyte
        Data API.

    -   Removes keys with empty values from the output of
        ``ItemAdapter.asdict()``, for a cleaner output.
    """

    @classmethod
    def is_item(cls, item: Any) -> bool:
        return isinstance(item, Item)

    def get_field_meta(self, field_name: str) -> MappingProxyType:
        if field_name in self._fields_dict:
            return self._fields_dict[field_name].metadata  # type: ignore
        else:
            return MappingProxyType({})

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
            try:
                delattr(self.item, field_name)
            except AttributeError:
                raise KeyError(field_name)
        elif field_name in self.item._unknown_fields_dict:
            del self.item._unknown_fields_dict[field_name]
        else:
            raise KeyError(
                f"Object of type {self.item.__class__.__name__} does not contain a field with name {field_name}"
            )

    def __iter__(self) -> Iterator:
        fields = [attr for attr in self._fields_dict if not _is_empty(getattr(self.item, attr))]
        fields.extend(
            attr
            for attr in self.item._unknown_fields_dict
            if (attr not in fields and not _is_empty(self.item._unknown_fields_dict[attr]))
        )
        return iter(fields)
