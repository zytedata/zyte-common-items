from unittest.mock import MagicMock

import pytest

import zyte_common_items.pipelines
from zyte_common_items.pipelines import DropItem, DropLowProbabilityItemPipeline


@pytest.mark.parametrize(
    "item_class_name, settings, default_threshold, expected_threshold",
    [
        ("Article", {"Article": 0.1, "Product": 0.2}, 0.01, 0.1),
        ("Product", {"Article": 0.1, "Product": 0.2}, 0.01, 0.2),
        ("Article", {}, 0.01, 0.01),
        ("Article", {"Product": 0.2}, 0.01, 0.01),
    ],
)
def test_get_threshold(settings, item_class_name, default_threshold, expected_threshold):
    spider = MagicMock()
    spider.settings.get.return_value = settings
    zyte_common_items.pipelines.DEFAULT_ITEM_PROBABILITY_THRESHOLD = default_threshold
    item = MagicMock()
    item.__class__.__name__ = item_class_name
    pipeline = DropLowProbabilityItemPipeline(MagicMock())
    threshold = pipeline.get_threshold(item, spider)

    assert threshold == expected_threshold


@pytest.mark.parametrize("item, item_proba, threshold, expected_stats_calls, expected_return", [
    (MagicMock(), None, 0.1, ["item/crawl/total", "item/crawl/extracted_with_high_proba"], True),
    (MagicMock(), 0.5, 0.1, ["item/crawl/total", "item/crawl/extracted_with_high_proba"], True),
    (MagicMock(), 0.01, 0.1, ["item/crawl/total", "item/crawl/dropped_with_low_proba"], None),
])
@pytest.mark.asyncio
async def test_process_item(item, item_proba, threshold, expected_stats_calls, expected_return):
    spider = MagicMock()
    stats = MagicMock()

    item.get_probability.return_value = item_proba

    pipeline = DropLowProbabilityItemPipeline(stats)
    pipeline.stats = stats
    pipeline.threshold = threshold

    try:
        returned_item = await pipeline.process_item(item, spider)
    except DropItem as e:
        assert (f"The item: {item!r} is dropped as the probability ({item_proba}) is "
                f"below the threshold ({threshold})") in str(e)
    else:
        assert returned_item == item

    for call in expected_stats_calls:
        getattr(stats, "inc_value").assert_any_call(call, spider=spider)
