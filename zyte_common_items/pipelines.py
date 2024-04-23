from copy import deepcopy
from warnings import warn

from zyte_common_items import ae


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
        warn(
            (
                "The zyte_common_items.pipelines.AEPipeline item pipeline has "
                "been implemented temporarily to help speed up migrating from "
                "Zyte Automatic Extraction to Zyte API automatic extraction "
                "(https://docs.zyte.com/zyte-api/migration/zyte/autoextract.html). "
                "However, this item pipeline will eventually be removed. "
                "Please, update your code not to depend on this item pipeline "
                "anymore."
            ),
            DeprecationWarning,
            stacklevel=2,
        )

    def process_item(self, item, spider):
        return ae.downgrade(item)


class DropLowProbabilityItemPipeline:
    """This pipeline drops an item if its probability, defined in the settings,
    is less than the specified threshold.

    By default, 0.1 threshold is used, i.e. items with probabillity < 0.1 are dropped.

    You can customize the thresholds by using the ITEM_PROBABILITY_THRESHOLDS setting that offers
    greater flexibility, allowing you to define thresholds for each Item class separately or
    set a default threshold for all other item classes.

    Thresholds for Item classes can be defined using either the path to the Item class or
    directly using the Item classes themselves.

    The example of using ITEM_PROBABILITY_THRESHOLDS:

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

    def process_item(self, item, spider):
        from scrapy.exceptions import DropItem

        item_name = self.get_item_name(item)
        item_proba = item.get_probability()
        threshold = self.get_threshold_for_item(item, spider)

        self.stats.inc_value("drop_low_probability_item/processed")
        self.stats.inc_value(f"drop_low_probability_item/processed/{item_name}")

        if item_proba is None or item_proba >= threshold:
            self.stats.inc_value("drop_low_probability_item/kept")
            self.stats.inc_value(f"drop_low_probability_item/kept/{item_name}")
            return item

        self.stats.inc_value("drop_low_probability_item/dropped")
        self.stats.inc_value(f"drop_low_probability_item/dropped/{item_name}")

        raise DropItem(
            f"This item is dropped since the probability ({item_proba}) "
            f"is below the threshold ({threshold}):\n{item!r}"
        )
