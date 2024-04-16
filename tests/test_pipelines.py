from unittest.mock import MagicMock, patch

import pytest

import zyte_common_items.pipelines
from zyte_common_items import Article, ArticleListPage, Product, ProductNavigation
from zyte_common_items.pipelines import DropItem, DropLowProbabilityItemPipeline


@pytest.mark.parametrize(
    "thresholds_settings, expected_thresholds",
    [
        ({}, {}),
        (
            {
                "zyte_common_items.items.Article": 0.2,
                "zyte_common_items.items.Product": 0.3,
            },
            {
                Article: 0.2,
                Product: 0.3,
            },
        ),
        (
            {Article: 0.4, Product: 0.5},
            {
                Article: 0.4,
                Product: 0.5,
            },
        ),
    ],
)
def test_init_thresholds(thresholds_settings, expected_thresholds):
    mock_crawler = MagicMock(spec=["spider", "stats"])
    mock_crawler.spider.settings.get.return_value = thresholds_settings
    pipeline = DropLowProbabilityItemPipeline(mock_crawler)
    assert pipeline.thresholds == expected_thresholds


@pytest.mark.parametrize(
    "item, thresholds_settings, default_threshold, expected_threshold",
    [
        (
            Article(url="http://example.com"),
            {Article: 0.3, Product: 0.4},
            0.01,
            0.3,
        ),
        (
            Product(url="http://example.com"),
            {Article: 0.3, Product: 0.4},
            0.01,
            0.4,
        ),
        (Article(url="http://example.com"), {}, 0.01, 0.01),
        (Article(url="http://example.com"), {Product: 0.2}, 0.01, 0.01),
    ],
)
def test_get_threshold(
    thresholds_settings, item, default_threshold, expected_threshold
):
    mock_crawler = MagicMock(spec=["spider", "stats"])
    mock_crawler.spider.settings.get.return_value = thresholds_settings
    pipeline = DropLowProbabilityItemPipeline(mock_crawler)
    zyte_common_items.pipelines.DEFAULT_ITEM_PROBABILITY_THRESHOLD = default_threshold

    threshold = pipeline.get_threshold(item, mock_crawler.spider)

    assert threshold == expected_threshold


@pytest.mark.parametrize(
    "item, item_proba, threshold, expected_stats_calls, expected_return",
    [
        (
            MagicMock(),
            None,
            0.1,
            ["item/crawl/total"],
            True,
        ),
        (
            MagicMock(),
            0.5,
            0.1,
            ["item/crawl/total"],
            True,
        ),
        (
            MagicMock(),
            0.01,
            0.1,
            ["item/crawl/total", "drop_item/magicmock/low_probability"],
            None,
        ),
    ],
)
def test_process_item(
    item, item_proba, threshold, expected_stats_calls, expected_return
):
    mock_crawler = MagicMock(spec=["spider", "stats"])
    item.get_probability.return_value = item_proba

    pipeline = DropLowProbabilityItemPipeline(mock_crawler)
    with patch.object(
        DropLowProbabilityItemPipeline, "get_threshold"
    ) as mock_get_threshold:
        mock_get_threshold.return_value = threshold

        try:
            returned_item = pipeline.process_item(item, mock_crawler.spider)
        except DropItem as e:
            assert (
                f"The item: {item!r} is dropped as the probability ({item_proba}) is "
                f"below the threshold ({threshold})"
            ) in str(e)
        else:
            assert returned_item == item

        for call in expected_stats_calls:
            mock_crawler.stats.inc_value.assert_any_call(
                call, spider=mock_crawler.spider
            )


@pytest.mark.parametrize(
    "item, expected_name",
    [
        (
            Article(url="http://example.com"),
            "article",
        ),
        (
            Product(url="http://example.com"),
            "product",
        ),
        (
            ProductNavigation(url="http://example.com"),
            "productNavigation",
        ),
        (
            ArticleListPage(response=MagicMock()),
            "articleListPage",
        ),
    ],
)
def test_get_item_name(item, expected_name):
    assert (
        DropLowProbabilityItemPipeline.get_item_name(MagicMock(), item) == expected_name
    )
