from itemadapter import ItemAdapter
from scrapy.settings import BaseSettings

from . import ZyteItemAdapter, ZyteItemKeepEmptyAdapter
from .log_formatters import ZyteLogFormatter


class Addon:
    def update_settings(self, settings: BaseSettings) -> None:
        if not any(
            issubclass(cls, (ZyteItemAdapter, ZyteItemKeepEmptyAdapter))
            for cls in ItemAdapter.ADAPTER_CLASSES
        ):
            ItemAdapter.ADAPTER_CLASSES = (
                ZyteItemAdapter,
                *ItemAdapter.ADAPTER_CLASSES,
            )

        settings.set("LOG_FORMATTER", ZyteLogFormatter, priority="addon")
