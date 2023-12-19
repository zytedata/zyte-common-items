from web_poet import Extractor, SelectorExtractor

from .processors import price_processor, simple_price_processor


class _ProductProcessors:
    price = [price_processor]
    regularPrice = [simple_price_processor]


class ProductVariantExtractor(Extractor):
    class Processors(_ProductProcessors):
        pass


class ProductVariantSelectorExtractor(SelectorExtractor):
    class Processors(_ProductProcessors):
        pass


class ProductFromListExtractor(Extractor):
    class Processors(_ProductProcessors):
        pass


class ProductFromListSelectorExtractor(SelectorExtractor):
    class Processors(_ProductProcessors):
        pass
