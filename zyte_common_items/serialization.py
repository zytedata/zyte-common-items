"""Web-poet serialization support for Zyte Common Items.

This module registers serialization and deserialization functions for
Item classes with web-poet's serialization system, allowing
web-poet testing framework to work when page objects use
zyte-common-items items as dependencies.
"""

import json
from typing import Type

import itemadapter
from web_poet.serialization import SerializedLeafData, register_serialization

from zyte_common_items.adapter import ZyteItemAdapter
from zyte_common_items.base import Item


class ZCEItemAdapter(itemadapter.ItemAdapter):
    """ItemAdapter configured to use ZyteItemAdapter for serialization."""

    ADAPTER_CLASSES = [ZyteItemAdapter]


def _serialize_item(o: Item) -> SerializedLeafData:
    """Serialize an Item instance to JSON."""
    item_dict = ZCEItemAdapter(o).asdict()
    item_json = json.dumps(item_dict, ensure_ascii=False, indent=2)
    return {"json": item_json.encode()}


def _deserialize_item(cls: Type[Item], data: SerializedLeafData) -> Item:
    """Deserialize JSON data back to an Item instance."""
    return cls.from_dict(json.loads(data["json"]))


# Register serialization for the base Item class
# This will work for all Item subclasses via singledispatch
register_serialization(_serialize_item, _deserialize_item)
