from itemadapter import ItemAdapter
from scrapy.settings import BaseSettings
from scrapy.utils.misc import load_object

from zyte_common_items import ZyteItemAdapter, ZyteItemKeepEmptyAdapter
from zyte_common_items.pipelines import DropLowProbabilityItemPipeline


def _setdefault(settings, setting, cls, pos):
    setting_value = settings[setting]
    if not setting_value:
        settings[setting] = {cls: pos}
        return
    if cls in setting_value:
        return
    for cls_or_path in setting_value:
        if isinstance(cls_or_path, str):
            _cls = load_object(cls_or_path)
            if _cls == cls:
                return
    settings[setting][cls] = pos


class Addon:
    def update_settings(self, settings: BaseSettings) -> None:
        if not any(
            issubclass(cls, (ZyteItemAdapter, ZyteItemKeepEmptyAdapter))
            for cls in ItemAdapter.ADAPTER_CLASSES
        ):
            ItemAdapter.ADAPTER_CLASSES.appendleft(ZyteItemAdapter)
        _setdefault(
            settings,
            "ITEM_PIPELINES",
            DropLowProbabilityItemPipeline,
            100,
        )
        try:
            from zyte_common_items.pipelines import AutoFieldStatsItemPipeline
        except ImportError:  # scrapy-poet not installed
            pass
        else:
            _setdefault(
                settings,
                "ITEM_PIPELINES",
                AutoFieldStatsItemPipeline,
                200,
            )
