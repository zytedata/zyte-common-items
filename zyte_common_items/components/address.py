import attrs

from zyte_common_items.base import Item


@attrs.define(kw_only=True)
class Address(Item):
    """Address item."""

    addressRaw: str | None = None
    """The raw address information, as it appears on the website."""

    streetAddress: str | None = None
    """The street address of the place."""

    addressCity: str | None = None
    """The city the place is located in."""

    addressLocality: str | None = None
    """The locality to which the place belongs."""

    addressRegion: str | None = None
    """The region of the place."""

    addressCountry: str | None = None
    """The country the place is located in.

    The country name or the `ISO 3166-1 alpha-2 country code
    <https://en.wikipedia.org/wiki/ISO_3166-1>`__.
    """

    postalCode: str | None = None
    """The postal code of the address."""

    postalCodeAux: str | None = None
    """The auxiliary part of the postal code.

    It may include a state abbreviation or town name, depending on local
    standards.
    """

    latitude: float | None = None
    """Geographical latitude of the place."""

    longitude: float | None = None
    """Geographical longitude of the place."""
