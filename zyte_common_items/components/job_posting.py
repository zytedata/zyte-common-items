from __future__ import annotations

from typing import Optional

import attrs

from zyte_common_items.base import Item


@attrs.define(kw_only=True)
class JobLocation(Item):
    """Location of a job offer."""

    #: Job location, as it appears on the website.
    raw: Optional[str] = None


@attrs.define(kw_only=True)
class BaseSalary(Item):
    """Base salary of a job offer."""

    #: Salary amount as it appears on the website.
    raw: Optional[str] = None

    #: The minimum value of the base salary as a number string.
    valueMin: Optional[str] = None

    #: The maximum value of the base salary as a number string.
    valueMax: Optional[str] = None

    #: The type of rate associated with the salary, e.g. monthly, annual, daily.
    rateType: Optional[str] = None

    #: Currency associated with the salary amount.
    currency: Optional[str] = None

    #: Currency associated with the salary amount, without normalization.
    currencyRaw: Optional[str] = None


@attrs.define(kw_only=True)
class HiringOrganization(Item):
    """Organization that is hiring for a job offer."""

    #: Name of the hiring organization.
    name: Optional[str] = None

    #: Organization information as available on the website.
    nameRaw: Optional[str] = None

    #: Identifier of the organization used by job posting website.
    id: Optional[str] = None
