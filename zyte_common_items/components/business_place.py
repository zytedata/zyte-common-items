from __future__ import annotations

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

    dayOfWeek: str | None = None
    """English weekday name."""

    opens: str | None = None
    """Opening time in ISO 8601 format, local time."""

    closes: str | None = None
    """Closing time in ISO 8601 format, local time."""

    rawDayOfWeek: str | None = None
    """Day of the week, as it appears on the page, without processing."""

    rawOpens: str | None = None
    """Opening time, as it appears on the page, without processing."""

    rawCloses: str | None = None
    """Closing time, as it appears on the page, without processing."""
