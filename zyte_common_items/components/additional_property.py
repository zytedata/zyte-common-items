import attrs

from zyte_common_items.base import Item


@attrs.define
class AdditionalProperty(Item):
    """A name-value pair.

    See :attr:`Product.additionalProperties
    <zyte_common_items.Product.additionalProperties>`.
    """

    #: Name.
    name: str

    #: Value.
    value: str
