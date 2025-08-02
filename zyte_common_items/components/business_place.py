from __future__ import annotations

from typing import Optional

import attrs

from zyte_common_items.base import Item


@attrs.define(kw_only=True)
class Amenity(Item):
    """An amenity that a business place has"""

    name: str
    """Name of amenity."""

    value: bool
    """Availability of the amenity."""


@attrs.define(kw_only=True)
class ParentPlace(Item):
    """If the place is located inside another place, these are the details of
    the parent place."""

    name: str
    """Name of the parent place."""

    placeId: str
    """Identifier of the parent place."""


@attrs.define(kw_only=True)
class OpeningHoursItem(Item):
    """Specification of opening hours of a business place."""

    dayOfWeek: Optional[str] = None
    """English weekday name."""

    opens: Optional[str] = None
    """Opening time in ISO 8601 format, local time."""

    closes: Optional[str] = None
    """Closing time in ISO 8601 format, local time."""

    rawDayOfWeek: Optional[str] = None
    """Day of the week, as it appears on the page, without processing."""

    rawOpens: Optional[str] = None
    """Opening time, as it appears on the page, without processing."""

    rawCloses: Optional[str] = None
    """Closing time, as it appears on the page, without processing."""
