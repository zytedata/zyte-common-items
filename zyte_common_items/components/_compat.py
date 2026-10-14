import sys

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

from .request import ProbabilityRequest, Request


@deprecated(
    "request_list_processor is deprecated in favor of "
    "zyte_common_items.processors.probability_request_list_processor"
)
def request_list_processor(request_list: list[Request]) -> list[ProbabilityRequest]:
    from zyte_common_items.processors import (  # noqa: PLC0415
        probability_request_list_processor,
    )

    return probability_request_list_processor(request_list)
