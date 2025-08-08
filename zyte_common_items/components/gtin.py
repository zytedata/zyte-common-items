import attrs

from zyte_common_items.base import Item


@attrs.define
class Gtin(Item):
    """GTIN_ type-value pair.

    See :class:`Product.gtin <zyte_common_items.Product.gtin>`.

    .. _GTIN: https://en.wikipedia.org/wiki/Global_Trade_Item_Number
    """

    type: str = attrs.field(
        metadata={
            "json_schema_extra": {
                "enum": [
                    "gtin13",
                    "gtin8",
                    "gtin14",
                    "isbn10",
                    "isbn13",
                    "ismn",
                    "issn",
                    "upc",
                ],
                "llmDescription": "The type of GTIN",
            }
        }
    )
    """Identifier of the GTIN format of ``value``.

    One of: ``"gtin13"``, ``"gtin8"``, ``"gtin14"``, ``"isbn10"``,
    ``"isbn13"``, ``"ismn"``, ``"issn"``, ``"upc"``.
    """

    value: str = attrs.field(
        metadata={
            "json_schema_extra": {
                "llmDescription": "The value of product identifier. Normalized format required: only numerical characters allowed.",
            }
        }
    )
    """Value.

    It should only contain digits.
    """
