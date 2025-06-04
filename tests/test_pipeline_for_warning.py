"""
Test module for pipeline component to check if warning is generated or not.
For DropLowProbabilityItemPipeline, warning should not be generated.
For AEPipeline, warning should be generated.
"""

import warnings
from unittest.mock import MagicMock

import pytest  # isort: skip

scrapy = pytest.importorskip("scrapy")  # noqa


WARNING_MSG = r"The zyte_common_items.ae module is a temporary module"


def test_warning():
    """
    Asserts if Deprication warning gets generated or not while
    importing AEPipeline. It should generate a warning message.
    """
    warnings.filterwarnings("default")

    # sys.modules.pop("zyte_common_items.ae", None)
    # sys.modules.pop("zyte_common_items.pipelines", None)

    with warnings.catch_warnings(record=True) as record:
        from zyte_common_items.pipelines import AEPipeline

        ae_pipeline = AEPipeline()
        from zyte_common_items.ae import downgrade
    warn_msg = str(record[0].message)
    assert len(record) == 1
    assert WARNING_MSG in warn_msg
    assert ae_pipeline._downgrade == downgrade


def test_no_warning():
    """
    Asserts if Deprication warning gets generated or not while
    importing DropLowProbabilityItemPipeline. It should not generate a warning
    message.
    """
    warnings.filterwarnings("default")
    with warnings.catch_warnings(record=True) as record:
        from zyte_common_items.pipelines import DropLowProbabilityItemPipeline

        mock_crawler = MagicMock(spec=["spider", "stats"])
        DropLowProbabilityItemPipeline(mock_crawler)
    assert len(record) == 0
