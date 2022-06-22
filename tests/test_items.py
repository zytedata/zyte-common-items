from copy import copy

import pytest

from zyte_common_items import (
    AdditionalProperty,
    AggregateRating,
    Brand,
    Breadcrumb,
    Gtin,
    Image,
    Metadata,
    Product,
    ProductVariant,
)

_PRODUCT_VARIANT_ALL_KWARGS = {
    "additionalProperties": [AdditionalProperty(name="foo", value="bar")],
    "availability": "InStock",
    "canonicalUrl": "https://example.com/product22",
    "color": "white",
    "currency": "USD",
    "currencyRaw": "$",
    "gtin": [Gtin(type="foo", value="bar")],
    "images": [
        Image(
            data_url=(
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFBAMAAAB"
                "/QTvWAAAAFVBMVEXMzMyWlpaxsbG3t7e+vr7FxcWjo6PZoQRwAAAACXBIWXMA"
                "AA7EAAAOxAGVKw4bAAAAEklEQVQImWNgQALKDgwMYQwMAAOLALoJbp2PAAAAA"
                "ElFTkSuQmCC"
            ),
        ),
        Image(url="http://example.com/image1.png"),
    ],
    "mainImage": Image(url="http://example.com/image1.png"),
    "mpn": "HSC0424PP",
    "name": "White two-door refrigerator",
    "price": "9999.99",
    "productId": "A123DK9823",
    "regularPrice": "11999.99",
    "size": "XL",
    "sku": "A123DK9823",
    "style": "polka dots",
}
_PRODUCT_MIN_KWARGS = {
    "url": "https://example.com/?product=product22",
    "metadata": Metadata(
        date_downloaded="20221231T130154Z",
        probability=1.0,
    ),
}
_PRODUCT_ALL_KWARGS = {
    **_PRODUCT_MIN_KWARGS,
    **_PRODUCT_VARIANT_ALL_KWARGS,
    "aggregateRating": AggregateRating(
        best_rating=5.0,
        rating_value=2.5,
        review_count=123,
    ),
    "brand": Brand(name="Ka-pow"),
    "breadcrumbs": [
        Breadcrumb(name="Level 1", link="http://example.com/level1"),
        Breadcrumb(name="Level 2", link="http://example.com/level1/level2"),
    ],
    "description": ("Full freshness all over the fridge\n5 Conversion Modes on demand\nSuper Cooling Plus™"),
    "descriptionHtml": (
        "<article><p>Full freshness all over the fridge</p>"
        "<p>5 Conversion Modes on demand</p>"
        "<p>Super Cooling Plus&trade;</p></article>"
    ),
    "features": ["Easily store fragile products.", "Bluetooth connectivity."],
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


def test_product_variant_all_fields():
    product_variant = ProductVariant(**_PRODUCT_VARIANT_ALL_KWARGS)
    for field in list(_PRODUCT_VARIANT_ALL_KWARGS):
        assert getattr(product_variant, field) == _PRODUCT_VARIANT_ALL_KWARGS[field]


def test_product_variant_min_fields():
    product_variant = ProductVariant()
    for field in list(_PRODUCT_VARIANT_ALL_KWARGS):
        assert getattr(product_variant, field) is None
