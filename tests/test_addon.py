import pytest  # isort: skip

pytest.importorskip("scrapy", minversion="2.10")

from itemadapter import ItemAdapter
from scrapy.settings import Settings

from zyte_common_items import Addon, ZyteItemAdapter, ZyteItemKeepEmptyAdapter
from zyte_common_items.log_formatters import ZyteLogFormatter


@pytest.fixture
def adapter_classes():
    original_value = ItemAdapter.ADAPTER_CLASSES
    try:
        yield
    finally:
        ItemAdapter.ADAPTER_CLASSES = original_value


def test_update_settings(adapter_classes):
    settings = Settings()
    Addon().update_settings(settings)
    assert settings["LOG_FORMATTER"] is ZyteLogFormatter
    assert next(iter(ItemAdapter.ADAPTER_CLASSES)) is ZyteItemAdapter
    Addon().update_settings(settings)
    assert tuple(ItemAdapter.ADAPTER_CLASSES).count(ZyteItemAdapter) == 1


def test_update_settings_keep_empty_adapter(adapter_classes):
    ItemAdapter.ADAPTER_CLASSES = (
        ZyteItemKeepEmptyAdapter,
        *ItemAdapter.ADAPTER_CLASSES,
    )
    Addon().update_settings(Settings())
    assert ZyteItemAdapter not in tuple(ItemAdapter.ADAPTER_CLASSES)
