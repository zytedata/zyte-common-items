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
    ProductFromList,
    ProductList,
    ProductVariant,
)

_PRODUCT_FROM_LIST_ALL_KWARGS = {
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
    "products": [ProductFromList()],
}


def test_product_all_fields():
    product = Product(**_PRODUCT_ALL_KWARGS)  # type: ignore[arg-type]
    for field in list(_PRODUCT_ALL_KWARGS):
        assert getattr(product, field) == _PRODUCT_ALL_KWARGS[field]


def test_product_min_fields():
    product = Product(**_PRODUCT_MIN_KWARGS)  # type: ignore[arg-type]
    for field in list(_PRODUCT_ALL_KWARGS):
        if field in _PRODUCT_MIN_KWARGS:
            continue
        assert getattr(product, field) is None


def test_product_missing_fields():
    for required_field in list(_PRODUCT_MIN_KWARGS):
        incomplete_kwargs = copy(_PRODUCT_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            Product(**incomplete_kwargs)  # type: ignore[arg-type]


def test_product_list_all_fields():
    product_list = ProductList(**_PRODUCT_LIST_ALL_KWARGS)  # type: ignore[arg-type]
    for field in list(_PRODUCT_LIST_ALL_KWARGS):
        assert getattr(product_list, field) == _PRODUCT_LIST_ALL_KWARGS[field]


def test_product_list_min_fields():
    product_list = ProductList(**_PRODUCT_LIST_MIN_KWARGS)  # type: ignore[arg-type]
    for field in list(_PRODUCT_LIST_MIN_KWARGS):
        if field in _PRODUCT_LIST_MIN_KWARGS:
            continue
        assert getattr(product_list, field) is None


def test_product_list_missing_fields():
    for required_field in list(_PRODUCT_LIST_MIN_KWARGS):
        incomplete_kwargs = copy(_PRODUCT_LIST_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            ProductList(**incomplete_kwargs)  # type: ignore[arg-type]


def test_product_from_list_all_fields():
    product_from_list = ProductFromList(**_PRODUCT_FROM_LIST_ALL_KWARGS)  # type: ignore[arg-type]
    for field in list(_PRODUCT_FROM_LIST_ALL_KWARGS):
        assert getattr(product_from_list, field) == _PRODUCT_FROM_LIST_ALL_KWARGS[field]


def test_product_from_list_min_fields():
    product_from_list = ProductFromList()
    for field in list(_PRODUCT_FROM_LIST_ALL_KWARGS):
        assert getattr(product_from_list, field) is None


def test_product_variant_all_fields():
    product_variant = ProductVariant(**_PRODUCT_VARIANT_ALL_KWARGS)  # type: ignore[arg-type]
    for field in list(_PRODUCT_VARIANT_ALL_KWARGS):
        assert getattr(product_variant, field) == _PRODUCT_VARIANT_ALL_KWARGS[field]


def test_product_variant_min_fields():
    product_variant = ProductVariant()
    for field in list(_PRODUCT_VARIANT_ALL_KWARGS):
        assert getattr(product_variant, field) is None
