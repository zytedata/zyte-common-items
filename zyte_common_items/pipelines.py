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
