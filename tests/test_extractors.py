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


@pytest.mark.asyncio
async def test_product_from_list_extractor():
    @attrs.define
    class MyProductFromListExtractor(ProductFromListExtractor):
        data: dict

        @field
        def price(self):
            return self.data["price"]

        @field
        def regularPrice(self):
            return self.data["regularPrice"]

    data = {"price": Selector("10€"), "regularPrice": Selector("20€")}
    extracted = await MyProductFromListExtractor(data).to_item()

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
            return self.css("regularPrice")

    selector = Selector(
        "<data><price>10€</price><regularPrice>20€</regularPrice></data>"
    )
    extracted = await MyProductFromListSelectorExtractor(selector).to_item()

    assert isinstance(extracted, ProductFromList)
    assert extracted.price == "10.00"
    assert extracted.regularPrice == "20.00"


@pytest.mark.asyncio
async def test_product_variant_extractor():
    @attrs.define
    class MyProductVariantExtractor(ProductVariantExtractor):
        data: dict

        @field
        def price(self):
            return self.data["price"]

        @field
        def regularPrice(self):
            return self.data["regularPrice"]

    data = {"price": Selector("10€"), "regularPrice": Selector("20€")}
    extracted = await MyProductVariantExtractor(data).to_item()

    assert isinstance(extracted, ProductVariant)
    assert extracted.price == "10.00"
    assert extracted.regularPrice == "20.00"


@pytest.mark.asyncio
async def test_product_variant_selector_extractor():
    class MyProductVariantSelectorExtractor(ProductVariantSelectorExtractor):
        @field
        def price(self):
            return self.css("price")

        @field
        def regularPrice(self):
            return self.css("regularPrice")

    selector = Selector(
        "<data><price>10€</price><regularPrice>20€</regularPrice></data>"
    )
    extracted = await MyProductVariantSelectorExtractor(selector).to_item()

    assert isinstance(extracted, ProductVariant)
    assert extracted.price == "10.00"
    assert extracted.regularPrice == "20.00"
