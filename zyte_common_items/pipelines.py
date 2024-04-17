from warnings import warn

from zyte_common_items import ae

DEFAULT_ITEM_PROBABILITY_THRESHOLD = 0.1


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
    """Drop item when it's probability is less than the threshold.

    This pipeline drops item if it's probability, defined in the settings,
    is less than the specified threshold. Thresholds can be defined per item type
    using `ITEM_PROBABILITY_THRESHOLDS` in two ways:

    With paths to Item classes:
        ITEM_PROBABILITY_THRESHOLDS = {
            "zyte_common_items.items.Article": 0.1,
            "zyte_common_items.items.Product": 0.2
        }

    With Item classes:
        from zyte_common_items import Article, Product
        ITEM_PROBABILITY_THRESHOLDS = {
            Article: 0.1,
            Product: 0.2
        }
    """

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.thresholds = {}
        self.init_thresholds(crawler.spider)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def init_thresholds(self, spider):
        from scrapy.utils.misc import load_object

        thresholds_settings = spider.settings.get("ITEM_PROBABILITY_THRESHOLDS", {})
        for item, threshold in thresholds_settings.items():
            item_type = load_object(item) if isinstance(item, str) else item
            self.thresholds[item_type] = threshold

    def get_threshold(self, item, spider):
        return self.thresholds.get(type(item), DEFAULT_ITEM_PROBABILITY_THRESHOLD)

    def get_item_name(self, item):
        item_name = item.__class__.__name__
        return item_name[0].lower() + item_name[1:]

    def process_item(self, item, spider):
        import scrapy

        threshold = self.get_threshold(item, spider)

        self.stats.inc_value("item/crawl/total", spider=spider)
        item_proba = item.get_probability()
        if item_proba is None or item_proba >= threshold:
            return item

        self.stats.inc_value(
            f"drop_item/{self.get_item_name(item)}/low_probability", spider=spider
        )
        raise scrapy.exceptions.DropItem(
            f"The item: {item!r} is dropped as the probability ({item_proba}) "
            f"is below the threshold ({threshold})"
        )
