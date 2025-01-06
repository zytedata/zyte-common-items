from logging import INFO

from scrapy.exceptions import DropItem
from scrapy.logformatter import LogFormatter


class InfoDropItem(DropItem):
    """DropItem subclass for items that should be dropped with an INFO message
    (instead of the default WARNING message)."""


class ZyteLogFormatter(LogFormatter):
    def dropped(self, item, exception, response, spider):
        data = super().dropped(item, exception, response, spider)
        if isinstance(exception, InfoDropItem):
            data["level"] = INFO
        return data
