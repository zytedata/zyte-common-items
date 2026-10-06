from typing_extensions import deprecated


@deprecated(
    "RequestListCaster is deprecated. Please use "
    "zyte_common_items.converters.to_probability_request_list"
)
class RequestListCaster:
    def __init__(self, target):
        self._target = target

    def __call__(self, value):
        return [item.cast(self._target) for item in value]
