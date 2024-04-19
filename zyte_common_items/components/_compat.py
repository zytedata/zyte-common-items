import warnings
from typing import List

from .request import ProbabilityRequest, Request


def request_list_processor(request_list: List[Request]) -> List[ProbabilityRequest]:
    """Deprecated. Please use
    :func:`zyte_common_items.processors.probability_request_list_processor` instead."""
    warnings.warn(
        message="request_list_processor is deprecated in favor of "
        "zyte_common_items.processors.probability_request_list_processor",
        category=DeprecationWarning,
        stacklevel=2,
    )
    from zyte_common_items.processors import probability_request_list_processor

    return probability_request_list_processor(request_list)
