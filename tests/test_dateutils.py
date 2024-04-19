import datetime

from zyte_common_items._dateutils import format_datetime, parse_iso_datetime


def test_parse_and_format():
    dt_str = "2024-04-11T15:06:02Z"
    dt_obj = datetime.datetime(
        year=2024,
        month=4,
        day=11,
        hour=15,
        minute=6,
        second=2,
        microsecond=0,
        tzinfo=datetime.timezone.utc,
    )

    assert parse_iso_datetime(dt_str) == dt_obj
    assert format_datetime(dt_obj) == dt_str
