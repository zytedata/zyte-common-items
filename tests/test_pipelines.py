from unittest.mock import MagicMock, patch

import pytest

import zyte_common_items.pipelines
from zyte_common_items import Article, ArticleListPage, Product, ProductNavigation
from zyte_common_items.pipelines import DropLowProbabilityItemPipeline


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
    scrapy = pytest.importorskip("scrapy")  # noqa

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
    scrapy = pytest.importorskip("scrapy")  # noqa

    mock_crawler = MagicMock(spec=["spider", "stats"])
    mock_crawler.spider.settings.get.return_value = thresholds_settings
    pipeline = DropLowProbabilityItemPipeline(mock_crawler)
    zyte_common_items.pipelines.DEFAULT_ITEM_PROBABILITY_THRESHOLD = default_threshold

    threshold = pipeline.get_threshold(item, mock_crawler.spider)

    assert threshold == expected_threshold


@pytest.mark.parametrize(
    "items, item_proba, threshold, expected_stats_calls, expected_return",
    [
        (
            [
                MagicMock(spec=Product(url="http://example.com")),
                MagicMock(spec=Article(url="http://example.com")),
            ],
            None,
            0.1,
            [
                ("drop_low_probability_item/processed", 2),
                ("drop_low_probability_item/processed/Product", 1),
                ("drop_low_probability_item/processed/Article", 1),
                ("drop_low_probability_item/kept", 2),
                ("drop_low_probability_item/kept/Product", 1),
                ("drop_low_probability_item/kept/Article", 1),
            ],
            True,
        ),
        (
            [
                MagicMock(spec=Product(url="http://example.com")),
                MagicMock(spec=Article(url="http://example.com")),
            ],
            0.5,
            0.1,
            [
                ("drop_low_probability_item/processed", 2),
                ("drop_low_probability_item/processed/Product", 1),
                ("drop_low_probability_item/processed/Article", 1),
                ("drop_low_probability_item/kept", 2),
                ("drop_low_probability_item/kept/Product", 1),
                ("drop_low_probability_item/kept/Article", 1),
            ],
            True,
        ),
        (
            [
                MagicMock(spec=Product(url="http://example.com")),
                MagicMock(spec=Article(url="http://example.com")),
            ],
            0.01,
            0.1,
            [
                ("drop_low_probability_item/processed", 2),
                ("drop_low_probability_item/processed/Product", 1),
                ("drop_low_probability_item/processed/Article", 1),
                ("drop_low_probability_item/dropped", 2),
                ("drop_low_probability_item/dropped/Product", 1),
                ("drop_low_probability_item/dropped/Article", 1),
            ],
            None,
        ),
    ],
)
def test_process_item(
    items, item_proba, threshold, expected_stats_calls, expected_return
):
    scrapy = pytest.importorskip("scrapy")

    mock_crawler = MagicMock(spec=["spider", "stats"])

    pipeline = DropLowProbabilityItemPipeline(mock_crawler)
    with patch.object(
        DropLowProbabilityItemPipeline, "get_threshold"
    ) as mock_get_threshold:
        mock_get_threshold.return_value = threshold

        for item in items:
            item.get_probability.return_value = item_proba
            try:
                returned_item = pipeline.process_item(item, mock_crawler.spider)
            except scrapy.exceptions.DropItem as e:
                assert (
                    f"This item is dropped since the probability ({item_proba}) "
                    f"is below the threshold ({threshold}):\n{item!r}"
                ) in str(e)
            else:
                assert returned_item == item

        for call, count in expected_stats_calls:
            calls = [
                args
                for args, kwargs in mock_crawler.stats.inc_value.call_args_list
                if args[0] == call
            ]
            assert len(calls) == count


@pytest.mark.parametrize(
    "item, expected_name",
    [
        (
            Article(url="http://example.com"),
            "Article",
        ),
        (
            Product(url="http://example.com"),
            "Product",
        ),
        (
            ProductNavigation(url="http://example.com"),
            "ProductNavigation",
        ),
        (
            ArticleListPage(response=MagicMock()),
            "ArticleListPage",
        ),
    ],
)
def test_get_item_name(item, expected_name):
    assert (
        DropLowProbabilityItemPipeline.get_item_name(MagicMock(), item) == expected_name
    )
