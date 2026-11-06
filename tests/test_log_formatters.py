import pytest  # isort: skip

pytest.importorskip("scrapy")

from logging import INFO
from unittest.mock import MagicMock

from scrapy.exceptions import DropItem

from zyte_common_items.log_formatters import InfoDropItem, ZyteLogFormatter


def _dropped(exception):
    spider = MagicMock()
    spider.crawler.settings = {"DEFAULT_DROPITEM_LOG_LEVEL": "WARNING"}
    return ZyteLogFormatter().dropped({"a": "b"}, exception, None, spider)  # type: ignore[arg-type]


def test_dropped_info():
    assert _dropped(InfoDropItem("foo"))["level"] == INFO


def test_dropped_default():
    assert _dropped(DropItem("foo"))["level"] != INFO
