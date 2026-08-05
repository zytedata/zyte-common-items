from logging import INFO

from scrapy.exceptions import DropItem
from scrapy.logformatter import LogFormatter


class InfoDropItem(DropItem):
    """:class:`~scrapy.exceptions.DropItem` subclass for items that should be
    dropped with an ``INFO`` message (instead of the default ``WARNING``
    message).

    It is used, for example, by
    :class:`~zyte_common_items.pipelines.DropLowProbabilityItemPipeline`.
    """


class ZyteLogFormatter(LogFormatter):
    """Log formatter that implements support for :class:`InfoDropItem`."""

    def dropped(self, item, exception, response, spider):
        data = super().dropped(item, exception, response, spider)
        if isinstance(exception, InfoDropItem):
            data["level"] = INFO
        return data
