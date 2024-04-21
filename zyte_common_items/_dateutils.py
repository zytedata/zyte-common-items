import datetime
import sys

try:
    from datetime import UTC
except ImportError:
    # Python < 3.11
    from datetime import timezone

    UTC = timezone.utc


def format_datetime(dt) -> str:
    """Return the specified :class:`~datetime.datetime` object, assumed to be
    in the UTC timezone, in ISO format, with the timezone specified as
    ``Z``."""
    return f"{dt.replace(tzinfo=None).isoformat(timespec='seconds')}Z"


def parse_iso_datetime(date_str) -> datetime.datetime:
    """
    Parse ISO-formatted UTC date (with a timezone specified as Z)
    to a TZ-aware datetime object.
    """
    if sys.version_info < (3, 11):
        assert date_str[-1] == "Z"
        return datetime.datetime.fromisoformat(date_str[:-1]).replace(tzinfo=UTC)
    return datetime.datetime.fromisoformat(date_str)


def utcnow_formatted() -> str:
    return format_datetime(utcnow())


def utcnow() -> datetime.datetime:
    """Return current datetime in UTC, as a tz-aware datetime object"""
    return datetime.datetime.now(UTC)
