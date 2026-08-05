from typing import List

from typing_extensions import deprecated

from .request import ProbabilityRequest, Request


@deprecated(
    "request_list_processor is deprecated in favor of "
    "zyte_common_items.processors.probability_request_list_processor"
)
def request_list_processor(request_list: List[Request]) -> List[ProbabilityRequest]:
    from zyte_common_items.processors import probability_request_list_processor

    return probability_request_list_processor(request_list)
