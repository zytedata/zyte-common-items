from collections.abc import Collection
from contextlib import contextmanager

import attrs
import pytest
from itemadapter import ItemAdapter

from zyte_common_items import Item, Product, ZyteItemAdapter

from .test_items import _PRODUCT_ALL_KWARGS, _PRODUCT_MIN_KWARGS


@contextmanager
def configured_adapter():
    ItemAdapter.ADAPTER_CLASSES.appendleft(ZyteItemAdapter)
    try:
        yield
    finally:
        ItemAdapter.ADAPTER_CLASSES.popleft()


def test_unknown_field_get():
    product = Product.from_dict(
        dict(
            a="b",
            additionalProperties=[{"name": "a", "value": "b", "max": 10}],
            aggregateRating={"worstRating": 0},
            url="https://example.com/",
        )
    )

    with configured_adapter():
        adapter = ItemAdapter(product)
        assert adapter["a"] == "b"

        adapter = ItemAdapter(product.additionalProperties[0])
        assert adapter["max"] == 10

        adapter = ItemAdapter(product.aggregateRating)
        assert adapter["worstRating"] == 0


def test_unknown_field_set():
    product = Product.from_dict(
        dict(
            additionalProperties=[{"name": "a", "value": "b"}],
            aggregateRating={"bestRating": 5.0},
            url="https://example.com/",
        )
    )

    with configured_adapter():
        adapter = ItemAdapter(product)
        adapter["a"] = "b"
        assert adapter["a"] == "b"
        assert product._unknown_fields_dict["a"] == "b"

        adapter = ItemAdapter(product.additionalProperties[0])
        adapter["max"] = 10
        assert adapter["max"] == 10
        assert product.additionalProperties[0]._unknown_fields_dict["max"] == 10

        adapter = ItemAdapter(product.aggregateRating)
        adapter["worstRating"] = 0
        assert adapter["worstRating"] == 0
        assert product.aggregateRating._unknown_fields_dict["worstRating"] == 0


def test_unknown_field_update():
    product = Product.from_dict(
        dict(
            a="b",
            additionalProperties=[{"name": "a", "value": "b", "max": 10}],
            aggregateRating={"worstRating": 0},
            url="https://example.com/",
        )
    )

    with configured_adapter():
        adapter = ItemAdapter(product)
        adapter["a"] = "c"
        assert adapter["a"] == "c"
        assert product._unknown_fields_dict["a"] == "c"

        adapter = ItemAdapter(product.additionalProperties[0])
        adapter["max"] = 20
        assert adapter["max"] == 20
        assert product.additionalProperties[0]._unknown_fields_dict["max"] == 20

        adapter = ItemAdapter(product.aggregateRating)
        adapter["worstRating"] = 1
        assert adapter["worstRating"] == 1
        assert product.aggregateRating._unknown_fields_dict["worstRating"] == 1


def test_unknown_field_remove():
    product = Product.from_dict(
        dict(
            a="b",
            additionalProperties=[{"name": "a", "value": "b", "max": 10}],
            aggregateRating={"worstRating": 0},
            url="https://example.com/",
        )
    )

    with configured_adapter():
        adapter = ItemAdapter(product)
        del adapter["a"]
        assert "a" not in adapter
        assert "a" not in product._unknown_fields_dict

        adapter = ItemAdapter(product.additionalProperties[0])
        del adapter["max"]
        assert "max" not in adapter
        assert "max" not in product.additionalProperties[0]._unknown_fields_dict

        adapter = ItemAdapter(product.aggregateRating)
        del adapter["worstRating"]
        assert "worstRating" not in adapter
        assert "worstRating" not in product.aggregateRating._unknown_fields_dict


def test_asdict_all_fields():
    product = Product(**_PRODUCT_ALL_KWARGS)
    with configured_adapter():
        adapter = ItemAdapter(product)
        actual_dict = adapter.asdict()
    expected_dict = {
        "additionalProperties": [dict(name="foo", value="bar")],
        "aggregateRating": dict(
            bestRating=5.0,
            ratingValue=2.5,
            reviewCount=123,
        ),
        "availability": "InStock",
        "brand": dict(name="Ka-pow"),
        "breadcrumbs": [
            dict(name="Level 1", url="http://example.com/level1"),
            dict(name="Level 2", url="http://example.com/level1/level2"),
        ],
        "canonicalUrl": "https://example.com/product22",
        "color": "white",
        "currency": "USD",
        "currencyRaw": "$",
        "description": "Full freshness all over the fridge\n5 Conversion Modes on demand\nSuper Cooling Plus™",
        "descriptionHtml": (
            "<article><p>Full freshness all over the fridge</p>"
            "<p>5 Conversion Modes on demand</p>"
            "<p>Super Cooling Plus&trade;</p></article>"
        ),
        "features": ["Easily store fragile products.", "Bluetooth connectivity."],
        "gtin": [dict(type="foo", value="bar")],
        "images": [
            dict(url="http://example.com/image1.png"),
        ],
        "mainImage": dict(url="http://example.com/image1.png"),
        "metadata": dict(
            dateDownloaded="2022-12-31T13:01:54Z",
            probability=1.0,
        ),
        "mpn": "HSC0424PP",
        "name": "White two-door refrigerator",
        "price": "9999.99",
        "productId": "A123DK9823",
        "regularPrice": "11999.99",
        "size": "XL",
        "sku": "A123DK9823",
        "style": "polka dots",
        "url": "https://example.com/?product=product22",
        "variants": [{}],
    }
    assert actual_dict == expected_dict


def test_product_asdict_min():
    product = Product(**_PRODUCT_MIN_KWARGS)
    with configured_adapter():
        adapter = ItemAdapter(product)
        actual_dict = adapter.asdict()
    expected_dict = {
        "url": "https://example.com/?product=product22",
    }
    assert actual_dict == expected_dict


def test_product_asdict_tuple():
    product = Product(**_PRODUCT_MIN_KWARGS, variants=({},))
    with configured_adapter():
        adapter = ItemAdapter(product)
        actual_dict = adapter.asdict()
    expected_dict = {
        "url": "https://example.com/?product=product22",
        "variants": ({},),
    }
    assert actual_dict == expected_dict


class EmptyCollection(Collection):
    def __contains__(self, item):
        return False

    def __len__(self):
        return 0

    def __iter__(self):
        return
        yield


@pytest.mark.parametrize(
    "value",
    (
        [],
        tuple(),
        EmptyCollection(),
    ),
)
def test_asdict_empty_collection(value):
    @attrs.define(slots=True)
    class _Item(Item):
        children: Collection[Item]

    item = _Item(value)
    with configured_adapter():
        adapter = ItemAdapter(item)
        actual_dict = adapter.asdict()
    assert actual_dict == {}


def test_asdict_unknown_fields():
    input_dict = dict(
        a="b",
        additionalProperties=[{"name": "a", "value": "b", "max": 10}],
        aggregateRating={"worstRating": 0},
        url="https://example.com/",
    )
    product = Product.from_dict(input_dict)
    with configured_adapter():
        adapter = ItemAdapter(product)
        assert adapter.asdict() == input_dict
