from __future__ import annotations

from typing import Optional

import attrs

from zyte_common_items.base import Item


@attrs.define(kw_only=True)
class Amenity(Item):
    """An amenity that a business place has"""

    #: Name of amenity.
    name: str

    #: Availability of the amenity.
    value: bool


@attrs.define(kw_only=True)
class ParentPlace(Item):
    """If the place is located inside another place, these are the details of the parent place."""

    #: Name of the parent place.
    name: str

    #: Identifier of the parent place.
    placeId: str


@attrs.define(kw_only=True)
class OpeningHoursItem(Item):
    """Specification of opening hours of a business place."""

    #: English weekday name.
    dayOfWeek: Optional[str] = None

    #: Opening time in ISO 8601 format, local time.
    opens: Optional[str] = None

    #: Closing time in ISO 8601 format, local time.
    closes: Optional[str] = None

    #: Day of the week, as it appears on the page, without processing.
    rawDayOfWeek: Optional[str] = None

    #: Opening time, as it appears on the page, without processing.
    rawOpens: Optional[str] = None

    #: Closing time, as it appears on the page, without processing.
    rawCloses: Optional[str] = None
