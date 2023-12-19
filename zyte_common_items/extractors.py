from web_poet import Extractor, SelectorExtractor

from .items import ProductFromList, ProductVariant
from .processors import price_processor, simple_price_processor


class _ProductProcessors:
    price = [price_processor]
    regularPrice = [simple_price_processor]


class ProductVariantExtractor(Extractor[ProductVariant]):
    class Processors(_ProductProcessors):
        pass


class ProductVariantSelectorExtractor(SelectorExtractor[ProductVariant]):
    class Processors(_ProductProcessors):
        pass


class ProductFromListExtractor(Extractor[ProductFromList]):
    class Processors(_ProductProcessors):
        pass


class ProductFromListSelectorExtractor(SelectorExtractor[ProductFromList]):
    class Processors(_ProductProcessors):
        pass
