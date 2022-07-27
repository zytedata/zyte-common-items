from copy import copy

import pytest

from zyte_common_items import (
    AdditionalProperty,
    AggregateRating,
    Brand,
    Breadcrumb,
    Gtin,
    Image,
    Link,
    Metadata,
    Product,
    ProductList,
    ProductListItem,
    ProductVariant,
)

_PRODUCT_LIST_ITEM_ALL_KWARGS = {
    "currency": "USD",
    "currencyRaw": "$",
    "mainImage": Image("http://example.com/image1.png"),
    "metadata": Metadata(
        dateDownloaded="2022-12-31T13:01:54Z",
        probability=1.0,
    ),
    "name": "White two-door refrigerator",
    "price": "9999.99",
    "productId": "A123DK9823",
    "regularPrice": "11999.99",
    "url": "https://example.com/?product=product22",
}
_PRODUCT_VARIANT_ALL_KWARGS = {
    "additionalProperties": [AdditionalProperty("foo", "bar")],
    "availability": "InStock",
    "canonicalUrl": "https://example.com/product22",
    "color": "white",
    "currency": "USD",
    "currencyRaw": "$",
    "gtin": [Gtin("foo", "bar")],
    "images": [
        Image("http://example.com/image1.png"),
    ],
    "mainImage": Image("http://example.com/image1.png"),
    "mpn": "HSC0424PP",
    "name": "White two-door refrigerator",
    "price": "9999.99",
    "productId": "A123DK9823",
    "regularPrice": "11999.99",
    "size": "XL",
    "sku": "A123DK9823",
    "style": "polka dots",
    "url": "https://example.com/?product=product22",
}
_PRODUCT_MIN_KWARGS = {
    "url": "https://example.com/?product=product22",
}
_PRODUCT_ALL_KWARGS = {
    **_PRODUCT_MIN_KWARGS,
    **_PRODUCT_VARIANT_ALL_KWARGS,
    "aggregateRating": AggregateRating(
        bestRating=5.0,
        ratingValue=2.5,
        reviewCount=123,
    ),
    "brand": Brand("Ka-pow"),
    "breadcrumbs": [
        Breadcrumb(name="Level 1", url="http://example.com/level1"),
        Breadcrumb(name="Level 2", url="http://example.com/level1/level2"),
    ],
    "description": ("Full freshness all over the fridge\n5 Conversion Modes on demand\nSuper Cooling Plus™"),
    "descriptionHtml": (
        "<article><p>Full freshness all over the fridge</p>"
        "<p>5 Conversion Modes on demand</p>"
        "<p>Super Cooling Plus&trade;</p></article>"
    ),
    "features": ["Easily store fragile products.", "Bluetooth connectivity."],
    "metadata": Metadata(
        dateDownloaded="2022-12-31T13:01:54Z",
        probability=1.0,
    ),
    "variants": [ProductVariant()],
}
_PRODUCT_LIST_MIN_KWARGS = {
    "url": "https://example.com/swiss-watches?sort=new-first",
}
_PRODUCT_LIST_ALL_KWARGS = {
    **_PRODUCT_LIST_MIN_KWARGS,
    "breadcrumbs": [
        Breadcrumb(name="Level 1", url="http://example.com/level1"),
        Breadcrumb(name="Level 2", url="http://example.com/level1/level2"),
    ],
    "canonicalUrl": "https://example.com/swiss-watches",
    "categoryName": "Swiss Watches",
    "metadata": Metadata(
        dateDownloaded="2022-12-31T13:01:54Z",
        probability=1.0,
    ),
    "pageNumber": 1,
    "paginationNext": Link(
        text="foo",
        url="https://example.com/swiss-watches?sort=new-first&page=2",
    ),
    "products": [ProductListItem()],
}


def test_product_all_fields():
    product = Product(**_PRODUCT_ALL_KWARGS)
    for field in list(_PRODUCT_ALL_KWARGS):
        assert getattr(product, field) == _PRODUCT_ALL_KWARGS[field]


def test_product_min_fields():
    product = Product(**_PRODUCT_MIN_KWARGS)
    for field in list(_PRODUCT_ALL_KWARGS):
        if field in _PRODUCT_MIN_KWARGS:
            continue
        assert getattr(product, field) is None


def test_product_missing_fields():
    for required_field in list(_PRODUCT_MIN_KWARGS):
        incomplete_kwargs = copy(_PRODUCT_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            Product(**incomplete_kwargs)


def test_product_unknown_input():
    product = Product.from_dict(
        dict(
            a="b",
            additionalProperties=[{"name": "a", "value": "b", "max": 10}],
            aggregateRating=dict(worstRating=0),
            brand={"name": "Zyte", "slug": "zyte"},
            breadcrumbs=[{"children": [{"name": "foo"}, {"url": "bar"}]}],
            gtin=[{"type": "gtin8", "value": "00000000", "checkPass": False}],
            images=[{"url": "http://example.com/image1.png", "format": "PNG"}],
            mainImage={
                "url": "http://example.com/image1.jpeg",
                "format": "JPEG",
            },
            metadata=dict(
                author="Guido",
            ),
            url="https://example.com/?product=product22",
            variants=[dict(position=1)],
        )
    )
    assert product._unknown_fields_dict["a"] == "b"
    assert product.additionalProperties[0]._unknown_fields_dict["max"] == 10
    assert product.aggregateRating._unknown_fields_dict["worstRating"] == 0
    assert product.brand._unknown_fields_dict["slug"] == "zyte"
    assert product.breadcrumbs[0]._unknown_fields_dict["children"] == [{"name": "foo"}, {"url": "bar"}]
    assert product.gtin[0]._unknown_fields_dict["checkPass"] is False
    assert product.images[0]._unknown_fields_dict["format"] == "PNG"
    assert product.mainImage._unknown_fields_dict["format"] == "JPEG"
    assert product.metadata._unknown_fields_dict["author"] == "Guido"
    assert product.variants[0]._unknown_fields_dict["position"] == 1


def test_product_list_all_fields():
    product_list = ProductList(**_PRODUCT_LIST_ALL_KWARGS)
    for field in list(_PRODUCT_LIST_ALL_KWARGS):
        assert getattr(product_list, field) == _PRODUCT_LIST_ALL_KWARGS[field]


def test_product_list_min_fields():
    product_list = ProductList(**_PRODUCT_LIST_MIN_KWARGS)
    for field in list(_PRODUCT_LIST_MIN_KWARGS):
        if field in _PRODUCT_LIST_MIN_KWARGS:
            continue
        assert getattr(product_list, field) is None


def test_product_list_missing_fields():
    for required_field in list(_PRODUCT_LIST_MIN_KWARGS):
        incomplete_kwargs = copy(_PRODUCT_LIST_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            ProductList(**incomplete_kwargs)


def test_product_list_unknown_input():
    product_list = ProductList.from_dict(
        dict(
            a="b",
            breadcrumbs=[{"children": [{"name": "foo"}, {"url": "bar"}]}],
            metadata=dict(
                author="Guido",
            ),
            url="https://example.com/?product=product22",
            products=[dict(position=1)],
        )
    )
    assert product_list._unknown_fields_dict["a"] == "b"
    assert product_list.breadcrumbs[0]._unknown_fields_dict["children"] == [{"name": "foo"}, {"url": "bar"}]
    assert product_list.metadata._unknown_fields_dict["author"] == "Guido"
    assert product_list.products[0]._unknown_fields_dict["position"] == 1


def test_product_list_item_all_fields():
    product_list_item = ProductListItem(**_PRODUCT_LIST_ITEM_ALL_KWARGS)
    for field in list(_PRODUCT_LIST_ITEM_ALL_KWARGS):
        assert getattr(product_list_item, field) == _PRODUCT_LIST_ITEM_ALL_KWARGS[field]


def test_product_list_item_min_fields():
    product_list_item = ProductListItem()
    for field in list(_PRODUCT_LIST_ITEM_ALL_KWARGS):
        assert getattr(product_list_item, field) is None


def test_product_variant_all_fields():
    product_variant = ProductVariant(**_PRODUCT_VARIANT_ALL_KWARGS)
    for field in list(_PRODUCT_VARIANT_ALL_KWARGS):
        assert getattr(product_variant, field) == _PRODUCT_VARIANT_ALL_KWARGS[field]


def test_product_variant_min_fields():
    product_variant = ProductVariant()
    for field in list(_PRODUCT_VARIANT_ALL_KWARGS):
        assert getattr(product_variant, field) is None
