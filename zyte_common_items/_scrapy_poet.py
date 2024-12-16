"""Scrapy components that require scrapy-poet."""

from logging import getLogger
from typing import Any, Set, Type

from itemadapter import ItemAdapter
from scrapy import Spider
from scrapy.crawler import Crawler
from scrapy.exceptions import NotConfigured
from scrapy.utils.misc import load_object
from scrapy_poet import InjectionMiddleware
from web_poet.fields import get_fields_dict
from web_poet.utils import get_fq_class_name

from zyte_common_items.fields import is_auto_field

logger = getLogger(__name__)


class AutoFieldStatsItemPipeline:
    """Allows generating stats for :ref:`auto fields <auto>`.

    To enable, set :setting:`ZYTE_COMMON_ITEMS_AUTO_FIELD_STATS` to ``True``.

    .. setting:: ZYTE_COMMON_ITEMS_AUTO_FIELD_STATS

    ZYTE_COMMON_ITEMS_AUTO_FIELD_STATS
    ==================================

    Default: ``False``

    If for any combination of item type and URL there is no registered page
    object class, the following stat is set:

    .. code-block:: python

        "zyte_common_items/auto_fields/<item class import path>": "(all fields)"

    .. note:: A literal ``(all fields)`` string is used as value, not a list
        with all fields.

    When a page object class is registered for a given combination of item type
    and URL, and that page object class overrides some fields, the following
    stat is set:

    .. code-block:: python

        "zyte_common_items/auto_fields/<override class import path>": (
            "<space-separated list of fields not overridden>"
        )

    .. note:: :func:`zyte_common_items.fields.is_auto_field` is used to
        determine whether a field has been overridden or not.

    Item URLs are read from the ``url`` field by default. Use
    :setting:`ZYTE_COMMON_ITEMS_AUTO_FIELD_URL_FIELDS` to configure a different
    field for any given item type.

    .. setting:: ZYTE_COMMON_ITEMS_AUTO_FIELD_URL_FIELDS

    ZYTE_COMMON_ITEMS_AUTO_FIELD_URL_FIELDS
    =======================================

    Default: ``{}``

    Dictionary where keys are item types or their import paths, and values are
    strings with the name of the field in those item types that indicates the
    source URL of the item.

    For example:

    .. code-block:: python
        :caption: settings.py

        ZYTE_COMMON_ITEMS_AUTO_FIELD_URL_FIELDS = {
            "my_project.items.CustomItem": "custom_url_field",
        }

    If a URL field is not specified for an item, ``url`` is used by default.
    """

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler: Crawler):
        if not crawler.settings.getbool("ZYTE_COMMON_ITEMS_AUTO_FIELD_STATS", False):
            raise NotConfigured

        raw_url_fields = crawler.settings.getdict(
            "ZYTE_COMMON_ITEMS_AUTO_FIELD_URL_FIELDS", {}
        )
        self._url_fields = {load_object(k): v for k, v in raw_url_fields.items()}
        self._seen: Set[Type] = set()
        self._crawler = crawler
        self._stats = crawler.stats
        self._item_cls_without_url: Set[Type] = set()

    def open_spider(self, spider):
        try:
            component = self._crawler.get_downloader_middleware(InjectionMiddleware)
        except AttributeError:  # Scrapy < 2.12
            for component in self._crawler.engine.downloader.middleware.middlewares:
                if isinstance(component, InjectionMiddleware):
                    break
            else:
                component = None
        if not component:
            raise RuntimeError(
                "Could not find scrapy_poet.InjectionMiddleware among "
                "downloader middlewares. scrapy-poet may be misconfigured."
            )
        self._registry = component.injector.registry

    def process_item(self, item: Any, spider: Spider):
        item_cls = item.__class__

        url_field = self._url_fields.get(item_cls, "url")
        adapter = ItemAdapter(item)
        url = adapter.get(url_field, None)
        if not url:
            if item_cls not in self._item_cls_without_url:
                self._item_cls_without_url.add(item_cls)
                logger.warning(
                    f"An item of type {item_cls} was missing a non-empty URL "
                    f"in its {url_field!r} field. An item URL is necessary to "
                    f"determine the page object that was used to generate "
                    f"that item, and hence print the auto field stats that "
                    f"you requested by enabling the "
                    f"ZYTE_COMMON_ITEMS_AUTO_FIELD_STATS setting. If "
                    f"{url_field!r} is the wrong URL field for that item "
                    f"type, use the ZYTE_COMMON_ITEMS_AUTO_FIELD_URL_FIELDS "
                    f"setting to set a different field."
                )
            return item

        page_cls = self._registry.page_cls_for_item(url, item_cls)

        cls = page_cls or item_cls
        if cls in self._seen:
            return item
        self._seen.add(cls)

        if not page_cls:
            field_list = "(all fields)"
        else:
            auto_fields = set()
            missing_fields = False
            for field_name in get_fields_dict(page_cls):
                if is_auto_field(page_cls, field_name):  # type: ignore[arg-type]
                    auto_fields.add(field_name)
                else:
                    missing_fields = True
            if missing_fields:
                field_list = " ".join(sorted(auto_fields))
            else:
                field_list = "(all fields)"

        cls_fqn = get_fq_class_name(cls)
        self._stats.set_value(f"zyte_common_items/auto_fields/{cls_fqn}", field_list)
        return item
