from typing import Optional

import attrs

from zyte_common_items.base import Item


@attrs.define(kw_only=True)
class RealEstateArea(Item):
    """Area of a place, with type, units, value and raw value."""

    value: float
    """Area."""

    unitCode: str
    """Unit of the value field, one of: SQMT (square meters), SQFT (square feet),
    ACRE (acres)."""

    areaType: Optional[str] = None
    """Type of area, one of: LOT, FLOOR."""

    raw: str
    """Area in the raw format, as it appears on the website."""
