import attrs
import pytest
from parsel import Selector
from web_poet import field

from zyte_common_items import ProductVariant, ProductVariantExtractor


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
