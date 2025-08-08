import attrs

from zyte_common_items.base import Item


@attrs.define
class AdditionalProperty(Item):
    """A name-value pair.

    See :attr:`Product.additionalProperties
    <zyte_common_items.Product.additionalProperties>`.
    """

    name: str = attrs.field(
        metadata={"json_schema_extra": {"llmDescription": "Name of the property"}}
    )
    """Name."""

    value: str = attrs.field(
        metadata={"json_schema_extra": {"llmDescription": "Value of the property"}}
    )
    """Value."""
