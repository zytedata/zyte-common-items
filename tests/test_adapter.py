from collections import deque
from collections.abc import Collection
from contextlib import contextmanager

# In Python ≤ 3.8 you cannot annotate with “collections.abc.Collection[Item]”,
# so we need to import typing.Collection for annotation instead.
from typing import Collection as CollectionType
from typing import Deque, Optional, Type, cast

import attrs
import pytest
from itemadapter import ItemAdapter
from itemadapter.adapter import AdapterInterface

from zyte_common_items import Item, Product, ZyteItemAdapter
from zyte_common_items.adapter import ZyteItemKeepEmptyAdapter

from .test_items import _PRODUCT_ALL_KWARGS, _PRODUCT_MIN_KWARGS


@contextmanager
def configured_adapter(adapter=ZyteItemAdapter):
    ItemAdapter.ADAPTER_CLASSES.appendleft(adapter)
    try:
        yield
    finally:
        ItemAdapter.ADAPTER_CLASSES.popleft()


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


def test_product_asdict_list():
    product = Product(**_PRODUCT_MIN_KWARGS, variants=[{}])  # type: ignore[list-item]
    with configured_adapter():
        adapter = ItemAdapter(product)
        actual_dict = adapter.asdict()
    expected_dict = {
        "url": "https://example.com/?product=product22",
        "variants": [{}],
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
    @attrs.define
    class _Item(Item):
        children: CollectionType[Item]

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


def test_field_meta():
    metadata = {"b": "c"}

    @attrs.define
    class _Item(Item):
        a = attrs.field(default=None, metadata=metadata)

    item = _Item()
    with configured_adapter():
        adapter = ItemAdapter(item)
        actual_dict = adapter.get_field_meta("a")
    assert actual_dict == metadata


def test_field_meta_missing_field():
    item = Item()
    with configured_adapter():
        adapter = ItemAdapter(item)
        with pytest.raises(KeyError):
            adapter.get_field_meta("a")


def test_field_meta_unknown_field():
    """There cannot be metadata for unknown fields, but trying to get it should
    not cause an exception either."""
    item = Item.from_dict({"a": None})
    with configured_adapter():
        adapter = ItemAdapter(item)
        actual_dict = adapter.get_field_meta("a")
    assert actual_dict == {}


def test_field_names():
    @attrs.define
    class _Item(Item):
        a: int
        b: Optional[int] = None

    item = _Item.from_dict({"a": 1, "c": 2, "d": None})
    with configured_adapter():
        adapter = ItemAdapter(item)
        actual = adapter.field_names()
    assert tuple(actual) == ("a", "b", "c", "d")


def test_known_field_get():
    url = "https://example.com/"
    product = Product(url=url)
    with configured_adapter():
        adapter = ItemAdapter(product)
        assert adapter["url"] == url


def test_known_field_get_missing():
    url = "https://example.com/"
    product = Product(url=url)
    with configured_adapter():
        adapter = ItemAdapter(product)
        assert adapter["canonicalUrl"] is None


def test_known_field_set():
    url = "https://example.com/"
    product = Product(url=url)
    with configured_adapter():
        adapter = ItemAdapter(product)
        adapter["canonicalUrl"] = url
        assert adapter["canonicalUrl"] == url
        assert product.canonicalUrl == url


def test_known_field_update():
    product = Product(url="https://example.com/a")
    with configured_adapter():
        adapter = ItemAdapter(product)
        new_url = "https://example.com/b"
        adapter["url"] = new_url
        assert adapter["url"] == new_url
        assert product.url == new_url


def test_known_field_remove():
    url = "https://example.com/"
    product = Product(url=url, canonicalUrl=url)
    with configured_adapter():
        adapter = ItemAdapter(product)
        del adapter["canonicalUrl"]
        assert "canonicalUrl" not in adapter
        assert not hasattr(product, "canonicalUrl")


def test_known_field_remove_missing():
    product = Product(url="https://example.com/")
    with configured_adapter():
        adapter = ItemAdapter(product)
        del adapter["canonicalUrl"]
        assert "canonicalUrl" not in adapter
        assert not hasattr(product, "canonicalUrl")


def test_known_field_remove_missing_twice():
    product = Product(url="https://example.com/")
    with configured_adapter():
        adapter = ItemAdapter(product)
        del adapter["canonicalUrl"]
        with pytest.raises(KeyError):
            del adapter["canonicalUrl"]


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


def test_unknown_field_get_missing():
    product = Product(url="https://example.com")
    with configured_adapter():
        adapter = ItemAdapter(product)
        with pytest.raises(KeyError):
            adapter["a"]


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


def test_unknown_field_remove_missing():
    product = Product(url="https://example.com/")
    with configured_adapter():
        adapter = ItemAdapter(product)
        with pytest.raises(KeyError):
            del adapter["a"]


def test_keep_empty_adapter_global():
    @attrs.define
    class _Item(Item):
        children: CollectionType[Item]

    item = _Item([])
    with configured_adapter(ZyteItemKeepEmptyAdapter):
        adapter = ItemAdapter(item)
        actual_dict = adapter.asdict()
    assert actual_dict == {"children": []}


def test_keep_empty_adapter_local():
    @attrs.define
    class _Item(Item):
        children: CollectionType[Item]

    class TestAdapter(ItemAdapter):
        ADAPTER_CLASSES = (
            cast(Deque[Type[AdapterInterface]], deque([ZyteItemKeepEmptyAdapter]))
            + ItemAdapter.ADAPTER_CLASSES
        )

    item = _Item([])
    adapter = TestAdapter(item)
    actual_dict = adapter.asdict()
    assert actual_dict == {"children": []}
