from typing import Optional

import attrs

from zyte_common_items.base import Item


@attrs.define(kw_only=True)
class RealEstateArea(Item):
    """Area of a place, with type, units, value and raw value."""

    #: Area
    value: float

    #: Unit of the value field, one of: SQMT (square meters), SQFT (square
    #: feet), ACRE (acres).
    unitCode: str

    #: Type of area, one of: LOT, FLOOR
    areaType: Optional[str] = None

    #: Area in the raw format, as it appears on the website.
    raw: str
