from web_poet import Extractor, SelectorExtractor

from .items import ProductFromList, ProductVariant
from .processors import price_processor, simple_price_processor


class _ProductProcessors:
    price = [price_processor]
    regularPrice = [simple_price_processor]


class ProductFromListExtractor(Extractor[ProductFromList]):
    """:class:`~web_poet.pages.Extractor` for :class:`ProductFromList`."""

    class Processors(_ProductProcessors):
        pass


class ProductFromListSelectorExtractor(SelectorExtractor[ProductFromList]):
    """:class:`~web_poet.pages.SelectorExtractor` for
    :class:`ProductFromList`."""

    class Processors(_ProductProcessors):
        pass


class ProductVariantExtractor(Extractor[ProductVariant]):
    """:class:`~web_poet.pages.Extractor` for :class:`ProductVariant`."""

    class Processors(_ProductProcessors):
        pass


class ProductVariantSelectorExtractor(SelectorExtractor[ProductVariant]):
    """:class:`~web_poet.pages.SelectorExtractor` for
    :class:`ProductVariant`."""

    class Processors(_ProductProcessors):
        pass
