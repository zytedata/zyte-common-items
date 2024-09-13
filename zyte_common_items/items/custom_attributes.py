from typing import Any, Dict

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import CustomAttributesMetadata


@attrs.define
class CustomAttributes(Item):
    """Extracted custom attribute values and metadata."""

    #: Custom attribute values
    values: Dict[str, Any]

    #: Custom attribute extraction metadata
    metadata: CustomAttributesMetadata
