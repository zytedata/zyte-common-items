from copy import copy

import pytest

from zyte_common_items import (
    AdditionalProperty,
    Address,
    AggregateRating,
    Amenity,
    Brand,
    Breadcrumb,
    BusinessPlace,
    BusinessPlaceMetadata,
    Gtin,
    Image,
    Link,
    Metadata,
    NamedLink,
    OpeningHours,
    ParentPlace,
    Product,
    ProductFromList,
    ProductList,
    ProductVariant,
    StarRating,
)

_PRODUCT_FROM_LIST_ALL_KWARGS: dict = {
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
_PRODUCT_VARIANT_ALL_KWARGS: dict = {
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
_PRODUCT_MIN_KWARGS: dict = {
    "url": "https://example.com/?product=product22",
}
_PRODUCT_ALL_KWARGS: dict = {
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
    "description": (
        "Full freshness all over the fridge\n5 Conversion Modes on demand\nSuper Cooling Plus™"
    ),
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
_PRODUCT_LIST_MIN_KWARGS: dict = {
    "url": "https://example.com/swiss-watches?sort=new-first",
}
_PRODUCT_LIST_ALL_KWARGS: dict = {
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

_BUSINESS_PLACE_MIN_KWARGS: dict = {"url": "https://place-listing.example/place/12345"}

_BUSINESS_PLACE_ALL_KWARGS: dict = {
    **_BUSINESS_PLACE_MIN_KWARGS,
    "placeId": "ChIJ02PI3bsaB3wRh-IwsWeJ0nI",
    "name": "Sheraton Kauai Resort",
    "actions": [
        NamedLink(name="Reserve Table", url="https://example.com"),
        NamedLink(name="Book Room", url="https://example.com"),
    ],
    "additionalProperties": [
        AdditionalProperty(name="Popular for", value="Lunch,Dinner")
    ],
    "address": Address(addressRaw="2440 Hoonani Rd, Koloa, HI 96756, US"),
    "reservationAction": NamedLink(name="Reserve a table", url="https://example.com"),
    "categories": ["Hotel", "Wedding venue"],
    "description": "Oceanfront resort offering Hawaiian dining, plus 2 outdoor pools & a fitness center.",
    "features": ["Pool", "Free Parking"],
    "map": "https://map.example/place/12345",
    "images": [
        Image("http://example.com/image1.png"),
    ],
    "amenityFeatures": [Amenity(name="Free WiFi", value=True)],
    "aggregateRating": AggregateRating(
        bestRating=5.0,
        ratingValue=2.5,
        reviewCount=123,
    ),
    "starRating": StarRating(raw="4-star Hotel"),
    "containedInPlace": ParentPlace(name="Gateway Plaza", placeId="ChIJCVDfcE_GBtq"),
    "openingHours": [OpeningHours(dayOfWeek="Monday", opens="10:00")],
    "reviewSites": [NamedLink(name="Expedia", url="https://example.com")],
    "telephone": "(808) 742-1661",
    "priceRange": "zz",
    "timezone": "Pacific/Honolulu",
    "isVerified": True,
    "website": "https://example.com",
    "tags": ["Dogs", "Family"],
    "metadata": BusinessPlaceMetadata(
        searchText="hotel", dateDownloaded="2022-12-31T13L01L54Z", probability=0.95
    ),
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
        incomplete_kwargs: dict = copy(_PRODUCT_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            Product(**incomplete_kwargs)


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
        incomplete_kwargs: dict = copy(_PRODUCT_LIST_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            ProductList(**incomplete_kwargs)


def test_product_from_list_all_fields():
    product_from_list = ProductFromList(**_PRODUCT_FROM_LIST_ALL_KWARGS)
    for field in list(_PRODUCT_FROM_LIST_ALL_KWARGS):
        assert getattr(product_from_list, field) == _PRODUCT_FROM_LIST_ALL_KWARGS[field]


def test_product_from_list_min_fields():
    product_from_list = ProductFromList()
    for field in list(_PRODUCT_FROM_LIST_ALL_KWARGS):
        assert getattr(product_from_list, field) is None


def test_product_variant_all_fields():
    product_variant = ProductVariant(**_PRODUCT_VARIANT_ALL_KWARGS)
    for field in list(_PRODUCT_VARIANT_ALL_KWARGS):
        assert getattr(product_variant, field) == _PRODUCT_VARIANT_ALL_KWARGS[field]


def test_product_variant_min_fields():
    product_variant = ProductVariant()
    for field in list(_PRODUCT_VARIANT_ALL_KWARGS):
        assert getattr(product_variant, field) is None


def test_business_place_all_fields():
    place = BusinessPlace(**_BUSINESS_PLACE_ALL_KWARGS)
    for field in list(_BUSINESS_PLACE_ALL_KWARGS):
        assert getattr(place, field) == _BUSINESS_PLACE_ALL_KWARGS[field]


def test_business_place_min_fields():
    place = BusinessPlace(**_BUSINESS_PLACE_MIN_KWARGS)
    for field in list(_BUSINESS_PLACE_ALL_KWARGS):
        if field in _BUSINESS_PLACE_MIN_KWARGS:
            continue
        assert getattr(place, field) is None


def test_business_place_missing_fields():
    for required_field in list(_BUSINESS_PLACE_MIN_KWARGS):
        incomplete_kwargs: dict = copy(_BUSINESS_PLACE_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            BusinessPlace(**incomplete_kwargs)
