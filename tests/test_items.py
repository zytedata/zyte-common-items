from copy import copy
from datetime import datetime, timezone

import pytest
from web_poet import ResponseUrl

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

_PRODUCT_VARIANT_MIN_KWARGS = {
    "url": ResponseUrl("https://example.com/?product=product22"),
}
_PRODUCT_VARIANT_ALL_KWARGS = {
    **_PRODUCT_VARIANT_MIN_KWARGS,
    "additional_properties": [AdditionalProperty(name="foo", value="bar")],
    "availability": "InStock",
    "canonical_url": ResponseUrl("https://example.com/product22"),
    "color": "white",
    "currency": "USD",
    "currency_raw": "$",
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
    "main_image": Image(url="http://example.com/image1.png"),
    "mpn": "HSC0424PP",
    "name": "White two-door refrigerator",
    "price": "9999.99",
    "regular_price": "11999.99",
    "size": "XL",
    "sku": "A123DK9823",
    "style": "polka dots",
}
_PRODUCT_MIN_KWARGS = {
    **_PRODUCT_VARIANT_MIN_KWARGS,
    "metadata": Metadata(
        date_downloaded=datetime(2022, 12, 31, 13, 1, 54, tzinfo=timezone.utc),
        probability=1.0,
    ),
}
_PRODUCT_ALL_KWARGS = {
    **_PRODUCT_MIN_KWARGS,
    **_PRODUCT_VARIANT_ALL_KWARGS,
    "aggregate_rating": AggregateRating(
        best_rating=5.0,
        rating_value=2.5,
        review_count=123,
    ),
    "brand": Brand(name="Ka-pow"),
    "breadcrumbs": [
        Breadcrumb(name="Level 1", link="http://example.com/level1"),
        Breadcrumb(name="Level 2", link="http://example.com/level1/level2"),
    ],
    "description": ("Full freshness all over the fridge\n" "5 Conversion Modes on demand\n" "Super Cooling Plus™"),
    "description_html": (
        "<article><p>Full freshness all over the fridge</p>"
        "<p>5 Conversion Modes on demand</p>"
        "<p>Super Cooling Plus&trade;</p></article>"
    ),
    "features": ["Easily store fragile products.", "Bluetooth connectivity."],
    "product_id": "A123DK9823",
}


def test_product_all_fields():
    product = Product(**_PRODUCT_ALL_KWARGS)

    assert product.additional_properties == _PRODUCT_ALL_KWARGS["additional_properties"]

    assert product.aggregate_rating == _PRODUCT_ALL_KWARGS["aggregate_rating"]

    assert product.availability == _PRODUCT_ALL_KWARGS["availability"]

    assert product.brand == _PRODUCT_ALL_KWARGS["brand"]

    assert product.breadcrumbs == _PRODUCT_ALL_KWARGS["breadcrumbs"]

    assert str(product.canonical_url) == str(_PRODUCT_ALL_KWARGS["canonical_url"])
    assert product.canonical_url.__class__ == ResponseUrl

    assert product.color == _PRODUCT_ALL_KWARGS["color"]

    assert product.currency == _PRODUCT_ALL_KWARGS["currency"]

    assert product.currency_raw == _PRODUCT_ALL_KWARGS["currency_raw"]

    assert product.description == _PRODUCT_ALL_KWARGS["description"]

    assert product.description_html == _PRODUCT_ALL_KWARGS["description_html"]

    assert product.features == _PRODUCT_ALL_KWARGS["features"]

    assert product.gtin == _PRODUCT_ALL_KWARGS["gtin"]

    assert product.images == _PRODUCT_ALL_KWARGS["images"]

    assert product.main_image == _PRODUCT_ALL_KWARGS["main_image"]

    assert product.metadata == _PRODUCT_ALL_KWARGS["metadata"]

    assert product.mpn == _PRODUCT_ALL_KWARGS["mpn"]

    assert product.name == _PRODUCT_ALL_KWARGS["name"]

    assert product.price == _PRODUCT_ALL_KWARGS["price"]

    assert product.product_id == _PRODUCT_ALL_KWARGS["product_id"]

    assert product.regular_price == _PRODUCT_ALL_KWARGS["regular_price"]

    assert product.size == _PRODUCT_ALL_KWARGS["size"]

    assert product.sku == _PRODUCT_ALL_KWARGS["sku"]

    assert product.style == _PRODUCT_ALL_KWARGS["style"]

    assert str(product.url) == str(_PRODUCT_ALL_KWARGS["url"])
    assert product.url.__class__ == ResponseUrl


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

    assert product_variant.additional_properties == _PRODUCT_VARIANT_ALL_KWARGS["additional_properties"]

    assert product_variant.availability == _PRODUCT_VARIANT_ALL_KWARGS["availability"]

    assert str(product_variant.canonical_url) == str(_PRODUCT_VARIANT_ALL_KWARGS["canonical_url"])
    assert product_variant.canonical_url.__class__ == ResponseUrl

    assert product_variant.color == _PRODUCT_VARIANT_ALL_KWARGS["color"]

    assert product_variant.currency == _PRODUCT_VARIANT_ALL_KWARGS["currency"]

    assert product_variant.currency_raw == _PRODUCT_VARIANT_ALL_KWARGS["currency_raw"]

    assert product_variant.gtin == _PRODUCT_VARIANT_ALL_KWARGS["gtin"]

    assert product_variant.images == _PRODUCT_VARIANT_ALL_KWARGS["images"]

    assert product_variant.main_image == _PRODUCT_VARIANT_ALL_KWARGS["main_image"]

    assert product_variant.mpn == _PRODUCT_VARIANT_ALL_KWARGS["mpn"]

    assert product_variant.name == _PRODUCT_VARIANT_ALL_KWARGS["name"]

    assert product_variant.price == _PRODUCT_VARIANT_ALL_KWARGS["price"]

    assert product_variant.regular_price == _PRODUCT_VARIANT_ALL_KWARGS["regular_price"]

    assert product_variant.size == _PRODUCT_VARIANT_ALL_KWARGS["size"]

    assert product_variant.sku == _PRODUCT_VARIANT_ALL_KWARGS["sku"]

    assert product_variant.style == _PRODUCT_VARIANT_ALL_KWARGS["style"]

    assert str(product_variant.url) == str(_PRODUCT_VARIANT_ALL_KWARGS["url"])
    assert product_variant.url.__class__ == ResponseUrl


def test_product_variant_min_fields():
    product_variant = ProductVariant(**_PRODUCT_VARIANT_MIN_KWARGS)
    for field in list(_PRODUCT_VARIANT_ALL_KWARGS):
        if field in _PRODUCT_VARIANT_MIN_KWARGS:
            continue
        assert getattr(product_variant, field) is None


def test_product_variant_missing_fields():
    for required_field in list(_PRODUCT_VARIANT_MIN_KWARGS):
        incomplete_kwargs = copy(_PRODUCT_VARIANT_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            ProductVariant(**incomplete_kwargs)
