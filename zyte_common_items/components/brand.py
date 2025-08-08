import attrs

from zyte_common_items.base import Item


@attrs.define
class Brand(Item):
    """Brand.

    See :attr:`Product.brand <zyte_common_items.Product.brand>`.
    """

    name: str = attrs.field(
        metadata={"json_schema_extra": {"llmDescription": "Name of the brand."}}
    )
    """Name as it appears on the source webpage (no post-processing)."""
