from __future__ import annotations

import attrs

from zyte_common_items.base import Item


@attrs.define(kw_only=True)
class JobLocation(Item):
    """Location of a job offer."""

    raw: str | None = None
    """Job location, as it appears on the website."""


@attrs.define(kw_only=True)
class BaseSalary(Item):
    """Base salary of a job offer."""

    raw: str | None = None
    """Salary amount as it appears on the website."""

    valueMin: str | None = None
    """The minimum value of the base salary as a number string."""

    valueMax: str | None = None
    """The maximum value of the base salary as a number string."""

    rateType: str | None = None
    """The type of rate associated with the salary, e.g. monthly, annual,
    daily."""

    currency: str | None = None
    """Currency associated with the salary amount."""

    currencyRaw: str | None = None
    """Currency associated with the salary amount, without normalization."""


@attrs.define(kw_only=True)
class HiringOrganization(Item):
    """Organization that is hiring for a job offer."""

    name: str | None = None
    """Name of the hiring organization."""

    nameRaw: str | None = None
    """Organization information as available on the website."""

    id: str | None = None
    """Identifier of the organization used by job posting website."""
