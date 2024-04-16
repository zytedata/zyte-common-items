import warnings


class RequestListCaster:
    """Deprecated."""

    def __init__(self, target):
        warnings.warn(
            "RequestListCaster is deprecated. Please use"
            "zyte_common_items.converters.to_probability_request_list",
            DeprecationWarning,
            stacklevel=2,
        )
        self._target = target

    def __call__(self, value):
        return [item.cast(self._target) for item in value]
