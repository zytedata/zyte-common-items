import pytest  # isort: skip

scrapy = pytest.importorskip("scrapy")  # noqa

import sys
import warnings
from copy import deepcopy
from unittest.mock import MagicMock, patch

from zyte_common_items import (
    Article,
    ArticleListPage,
    CustomAttributes,
    CustomAttributesMetadata,
    CustomAttributesValues,
    Product,
    ProductNavigation,
)
from zyte_common_items.base import ProbabilityMixin
from zyte_common_items.pipelines import DropLowProbabilityItemPipeline


@pytest.mark.parametrize(
    "thresholds_settings, default_threshold, expected_thresholds, expected_default_thresholds",
    [
        ({}, 0.09, {}, 0.09),
        (
            {
                "zyte_common_items.Article": 0.2,
                "zyte_common_items.Product": 0.3,
            },
            None,
            {
                Article: 0.2,
                Product: 0.3,
            },
            None,
        ),  # thresholds for items per Item's path
        (
            {Article: 0.4, Product: 0.5},
            None,
            {
                Article: 0.4,
                Product: 0.5,
            },
            None,
        ),  # thresholds for items per Item's class
        (
            {Article: 0.4},
            0.09,
            {
                Article: 0.4,
            },
            0.09,
        ),  # default threshold is taken from DEFAULT_ITEM_PROBABILITY_THRESHOLD
        (
            {"default": 0.6, Article: 0.4},
            0.09,
            {
                Article: 0.4,
            },
            0.6,
        ),  # default threshold is taken from settings with the key 'default'
        (
            {"default": 0, Article: 0.4},
            0.09,
            {
                Article: 0.4,
            },
            0,
        ),  # default threshold is taken from settings with the key 'default' == 0
    ],
)
def test_init_thresholds(
    thresholds_settings,
    default_threshold,
    expected_thresholds,
    expected_default_thresholds,
):
    mock_crawler = MagicMock(spec=["spider", "stats"])
    initial_thresholds_settings = deepcopy(thresholds_settings)
    mock_crawler.spider.settings.get.return_value = thresholds_settings
    DropLowProbabilityItemPipeline.DEFAULT_THRESHOLD = default_threshold
    pipeline = DropLowProbabilityItemPipeline(mock_crawler)
    assert pipeline.thresholds_for_item == expected_thresholds
    assert pipeline.default_threshold == expected_default_thresholds
    assert initial_thresholds_settings == thresholds_settings


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
def test_get_threshold_for_item(
    thresholds_settings, item, default_threshold, expected_threshold
):
    mock_crawler = MagicMock(spec=["spider", "stats"])
    mock_crawler.spider.settings.get.return_value = thresholds_settings
    pipeline = DropLowProbabilityItemPipeline(mock_crawler)
    pipeline.default_threshold = default_threshold

    threshold = pipeline.get_threshold_for_item(item, mock_crawler.spider)

    assert threshold == expected_threshold


@pytest.mark.parametrize(
    "items, item_proba, threshold, expected_stats_calls",
    [
        (
            [
                MagicMock(spec=Product(url="http://example.com")),
                MagicMock(spec=Article(url="http://example.com")),
            ],
            None,
            0.1,
            [
                ("drop_low_probability_item/processed", 0),
                ("drop_low_probability_item/kept", 0),
            ],
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
        ),
        (
            [
                {
                    "product": MagicMock(spec=Product(url="http://example.com")),
                    "customAttributes": MagicMock(
                        spec=CustomAttributes(
                            values=CustomAttributesValues({"foo": "bar"}),
                            metadata=CustomAttributesMetadata(),
                        )
                    ),
                },
            ],
            0.01,
            0.1,
            [
                ("drop_low_probability_item/processed", 1),
                ("drop_low_probability_item/processed/Product", 1),
                ("drop_low_probability_item/dropped", 1),
                ("drop_low_probability_item/dropped/Product", 1),
            ],
        ),
        (
            [
                {
                    "product": MagicMock(spec=Product(url="http://example.com")),
                    "article": MagicMock(spec=Article(url="http://example.com")),
                },
            ],
            0.01,
            0.1,
            [
                ("drop_low_probability_item/processed", 2),
                ("drop_low_probability_item/processed/Product", 1),
                ("drop_low_probability_item/processed/Article", 1),
                ("drop_low_probability_item/dropped", 1),
                ("drop_low_probability_item/dropped/Product", 1),
            ],
        ),
        (
            [
                scrapy.Item(),
            ],
            0.01,
            0.1,
            [
                ("drop_low_probability_item/processed", 0),
                ("drop_low_probability_item/kept", 0),
            ],
        ),
        (
            [
                {"foo": 42},
            ],
            0.01,
            0.1,
            [
                ("drop_low_probability_item/processed", 0),
                ("drop_low_probability_item/kept", 0),
            ],
        ),
        (
            [
                {},
            ],
            0.01,
            0.1,
            [
                ("drop_low_probability_item/processed", 0),
                ("drop_low_probability_item/kept", 0),
            ],
        ),
    ],
)
def test_process_item(items, item_proba, threshold, expected_stats_calls):
    mock_crawler = MagicMock(spec=["spider", "stats"])

    pipeline = DropLowProbabilityItemPipeline(mock_crawler)
    with patch.object(
        DropLowProbabilityItemPipeline, "get_threshold_for_item"
    ) as mock_get_threshold_for_item:
        mock_get_threshold_for_item.return_value = threshold

        for item in items:
            if isinstance(item, dict):
                # only set the specified probability on the product for simplicity
                for item_type, sub_item in item.items():
                    if item_type == "product":
                        sub_item.get_probability.return_value = item_proba
                    elif item_type == "customAttributes":
                        sub_item.get_probability.return_value = None
                    elif isinstance(sub_item, ProbabilityMixin):
                        sub_item.get_probability.return_value = 1.0  # type: ignore[attr-defined]
            elif isinstance(item, ProbabilityMixin):
                item.get_probability.return_value = item_proba  # type: ignore[attr-defined]
            try:
                returned_item = pipeline.process_item(item, mock_crawler.spider)
            except scrapy.exceptions.DropItem as e:
                assert (
                    f"This item is dropped since the probability ({item_proba}) "
                    f"is below the threshold ({threshold}):"
                ) in str(e)
            else:
                if isinstance(item, dict):
                    expected_item = item.copy()
                    expected_item.pop("product", None)
                else:
                    expected_item = item
                assert returned_item == expected_item

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


def test_warning():
    warning_msg = r"The zyte_common_items.ae module is a temporary module"
    warnings.filterwarnings("default")
    sys.modules.pop("zyte_common_items.ae", None)
    sys.modules.pop("zyte_common_items.pipelines", None)
    sys.modules.pop("zyte_common_items", None)

    with warnings.catch_warnings(record=True) as record:
        from zyte_common_items.pipelines import AEPipeline

        ae_pipeline = AEPipeline()
    warn_msg = str(record[0].message)
    assert len(record) == 1
    assert warning_msg in warn_msg
    from zyte_common_items.ae import downgrade

    assert ae_pipeline._downgrade == downgrade


def test_no_warning():
    warnings.filterwarnings("default")
    sys.modules.pop("zyte_common_items.ae", None)
    sys.modules.pop("zyte_common_items.pipelines", None)
    sys.modules.pop("zyte_common_items", None)

    with warnings.catch_warnings(record=True) as record:
        from zyte_common_items.pipelines import DropLowProbabilityItemPipeline

        mock_crawler = MagicMock(spec=["spider", "stats"])
        DropLowProbabilityItemPipeline(mock_crawler)
    assert len(record) == 0
