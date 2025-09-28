import random


def crazy_monkey_nullify(data, drop_prob=0.5):
    """Make some attributes None or [] recursively"""

    def nullify(value):
        if drop_prob <= random.random():
            return [] if isinstance(value, list) else None
        return crazy_monkey_nullify(value, drop_prob)

    if isinstance(data, list):
        return [crazy_monkey_nullify(value, drop_prob) for value in data]
    if isinstance(data, dict):
        return {k: nullify(v) for k, v in data.items()}
    return data
