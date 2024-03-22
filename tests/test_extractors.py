import attrs
import pytest
from parsel import Selector
from web_poet import field

from zyte_common_items import (
    ProductFromList,
    ProductFromListExtractor,
    ProductFromListSelectorExtractor,
    ProductVariant,
    ProductVariantExtractor,
    ProductVariantSelectorExtractor,
)

from .test_processors import gtin_expected, gtin_str


@pytest.mark.asyncio
async def test_product_from_list_extractor():
    @attrs.define
    class MyProductFromListExtractor(ProductFromListExtractor):
        selector: Selector

        @field
        def price(self):
            return self.selector.css("price")

        @field
        def regularPrice(self):
            return self.selector.css("oldPrice")

    selector = Selector("<data><price>10€</price><oldPrice>20€</oldPrice></data>")
    extracted = await MyProductFromListExtractor(selector).to_item()

    assert isinstance(extracted, ProductFromList)
    assert extracted.price == "10.00"
    assert extracted.regularPrice == "20.00"


@pytest.mark.asyncio
async def test_product_from_list_selector_extractor():
    class MyProductFromListSelectorExtractor(ProductFromListSelectorExtractor):
        @field
        def price(self):
            return self.css("price")

        @field
        def regularPrice(self):
            return self.css("oldPrice")

    selector = Selector("<data><price>10€</price><oldPrice>20€</oldPrice></data>")
    extracted = await MyProductFromListSelectorExtractor(selector).to_item()

    assert isinstance(extracted, ProductFromList)
    assert extracted.price == "10.00"
    assert extracted.regularPrice == "20.00"


@pytest.mark.asyncio
async def test_product_variant_extractor():
    @attrs.define
    class MyProductVariantExtractor(ProductVariantExtractor):
        selector: Selector

        @field
        def gtin(self):
            return self.selector.css("gtin")

        @field
        def price(self):
            return self.selector.css("price")

        @field
        def regularPrice(self):
            return self.selector.css("oldPrice")

    selector = Selector(
        f"<data>"
        f"<price>10€</price>"
        f"<oldPrice>20€</oldPrice>"
        f"<unusedField>foo</unusedField>"
        f"<gtin>{gtin_str}</gtin>"
        f"</data>"
    )
    extracted = await MyProductVariantExtractor(selector).to_item()

    assert isinstance(extracted, ProductVariant)
    assert extracted.gtin == gtin_expected
    assert extracted.price == "10.00"
    assert extracted.regularPrice == "20.00"


@pytest.mark.asyncio
async def test_product_variant_selector_extractor():
    class MyProductVariantSelectorExtractor(ProductVariantSelectorExtractor):
        @field
        def gtin(self):
            return self.css("gtin")

        @field
        def price(self):
            return self.css("price")

        @field
        def regularPrice(self):
            return self.css("oldPrice")

    selector = Selector(
        f"<data>"
        f"<price>10€</price>"
        f"<oldPrice>20€</oldPrice>"
        f"<unusedField>foo</unusedField>"
        f"<gtin>{gtin_str}</gtin>"
        f"</data>"
    )
    extracted = await MyProductVariantSelectorExtractor(selector).to_item()

    assert isinstance(extracted, ProductVariant)
    assert extracted.gtin == gtin_expected
    assert extracted.price == "10.00"
    assert extracted.regularPrice == "20.00"
