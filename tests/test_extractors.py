import attrs
import pytest
from web_poet import field

from zyte_common_items import ProductVariantExtractor


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

    data = {"price": "10€", "regularPrice": "20€"}
    extracted = await MyProductVariantExtractor(data).to_item()
    assert extracted == {"price": "10.00", "regularPrice": "20.00"}
