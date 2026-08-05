# Raise ImportError if Scrapy is missing.
import scrapy  # isort: skip  # noqa: F401

import logging
from copy import deepcopy

from .base import ProbabilityMixin
from .log_formatters import InfoDropItem

logger = logging.getLogger(__name__)


class AEPipeline:
    """Replace standard items with matching items with the old Zyte Automatic
    Extraction schema.

    This item pipeline is intended to help in the `migration from Zyte
    Automatic Extraction to Zyte API automatic extraction
    <https://docs.zyte.com/zyte-api/migration/zyte/autoextract.html>`_.

    In the simplest scenarios, it can be added to the ``ITEM_PIPELINES``
    setting in migrated code to ensure that the schema of output items matches
    the old schema.

    In scenarios where page object classes were being used to fix, extend or
    customize extraction, it is recommended to migrate page object classes to
    the new schemas, or move page object class code to the corresponding spider
    callback.

    If you have callbacks with custom code based on the old schema, you can
    either migrate that code, and ideally move it to a page object class, or
    use zyte_common_items.ae.downgrade at the beginning of the callback, e.g.:

    .. code-block:: python

        from zyte_common_items import ae

        ...


        def parse_product(self, response: DummyResponse, product: Product):
            product = ae.downgrade(product)
            ...
    """

    def __init__(self):
        from . import ae

        self._downgrade = ae.downgrade

    def process_item(self, item, spider):
        return self._downgrade(item)


class DropLowProbabilityItemPipeline:
    """:ref:`Item pipeline <topics-item-pipeline>` that drops items that have
    a low probability.

    The :setting:`ITEM_PROBABILITY_THRESHOLDS` setting determines the
    probability thresholds. By default, items with probability < 0.1 are
    dropped.

    :class:`dict` objects with items as values are supported. For those, the
    probability of each item is evaluated, and items with a low probability are
    removed from the :class:`dict`. If the :class:`dict` ends up empty, it is
    dropped entirely.

    .. setting:: ITEM_PROBABILITY_THRESHOLDS

    ITEM_PROBABILITY_THRESHOLDS
    ---------------------------

    Default: ``{"default": 0.1}``

    Allows defining a threshold for each item class and a default threshold
    for any other item class.

    Thresholds for item classes can be defined using either an import path of
    the item class or directly using the item class itself.

    For example:

    .. code-block:: python

        from zyte_common_items import Article

        ITEM_PROBABILITY_THRESHOLDS = {
            Article: 0.2,
            "zyte_common_items.Product": 0.3,
            "default": 0.15,
        }
    """

    DEFAULT_THRESHOLD = 0.1

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.thresholds_for_item = {}
        self.default_threshold = None
        self.init_thresholds(crawler.spider)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def init_thresholds(self, spider):
        from scrapy.utils.misc import load_object

        thresholds_settings = deepcopy(
            spider.settings.get("ITEM_PROBABILITY_THRESHOLDS", {})
        )

        self.default_threshold = thresholds_settings.pop(
            "default", self.DEFAULT_THRESHOLD
        )

        for item, threshold in thresholds_settings.items():
            item_type = load_object(item) if isinstance(item, str) else item
            self.thresholds_for_item[item_type] = threshold

    def get_threshold_for_item(self, item, spider):
        return self.thresholds_for_item.get(type(item), self.default_threshold)

    def get_item_name(self, item):
        return item.__class__.__name__

    def _process_probability(self, item, threshold):
        if not isinstance(item, ProbabilityMixin):
            return True
        item_proba = item.get_probability()
        if item_proba is None:
            # don't emit stats for types without probability
            return True
        item_name = self.get_item_name(item)
        self.stats.inc_value("drop_low_probability_item/processed")
        self.stats.inc_value(f"drop_low_probability_item/processed/{item_name}")
        if item_proba >= threshold:
            self.stats.inc_value("drop_low_probability_item/kept")
            self.stats.inc_value(f"drop_low_probability_item/kept/{item_name}")
            return True
        self.stats.inc_value("drop_low_probability_item/dropped")
        self.stats.inc_value(f"drop_low_probability_item/dropped/{item_name}")
        return False

    def process_item(self, item, spider):
        if isinstance(item, dict):
            if len(item) == 0:
                return item
            # for nested items remove sub-items that have low probability
            # instead of dropping the whole result
            new_item = {}
            for item_type, sub_item in item.items():
                threshold = self.get_threshold_for_item(sub_item, spider)
                if self._process_probability(sub_item, threshold):
                    new_item[item_type] = sub_item
                else:
                    logger.info(
                        f"This sub-item is dropped since the probability ({sub_item.get_probability()}) "
                        f"is below the threshold ({threshold}):\n{sub_item!r}"
                    )
            if not new_item:
                # everything has been removed
                raise InfoDropItem(
                    "This item is dropped since the probability of all its sub-items "
                    "is below the threshold:"
                )
            return new_item

        threshold = self.get_threshold_for_item(item, spider)
        if self._process_probability(item, threshold):
            return item
        raise InfoDropItem(
            f"This item is dropped since the probability ({item.get_probability()}) "
            f"is below the threshold ({threshold}):"
        )
