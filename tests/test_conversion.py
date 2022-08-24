"""This test file is ignored by mypy so don't rely on type assertions in this.

Instead, take a look at the ``tests/test_mypy.py``.
"""
import pytest
from web_poet import HttpResponse, RequestUrl, ResponseUrl

from zyte_common_items import (
    Breadcrumb,
    Image,
    Link,
    Product,
    ProductFromList,
    ProductList,
    ProductVariant,
)


@pytest.mark.parametrize(
    "cls,fields",
    [
        (Image, ["url"]),
        (Breadcrumb, ["url"]),
        (Link, ["url"]),
        (Product, ["url", "canonicalUrl"]),
        (ProductList, ["url", "canonicalUrl"]),
        (ProductFromList, ["url"]),
        (ProductVariant, ["url", "canonicalUrl"]),
    ],
)
def test_webpoet_URL_classes(cls, fields):
    """Ensure that the URL classes from web-poet are properly converted into
    URL strings when instantiating.
    """
    url = "https://www.some-url.com"
    response = HttpResponse(url, b"")

    response_url_obj = response.url
    assert type(response_url_obj) == ResponseUrl

    request_url_obj = response.urljoin("/another-page")
    assert type(request_url_obj) == RequestUrl

    # Ensure that both types of URL classes are covered
    for url_obj in [response_url_obj, request_url_obj]:
        data = {field: url_obj for field in fields}
        obj = cls(**data)

        for field in fields:
            # The URL classes should be converted to strings on instantiation
            attribute = getattr(obj, field)
            assert type(attribute) == str
            assert attribute == str(url_obj)

            # The conversion should also work via field assignment
            setattr(obj, field, response.urljoin("/somewhere"))
            attribute = getattr(obj, field)
            assert type(attribute) == str
            assert attribute == "https://www.some-url.com/somewhere"

            # Setting other values that are not strings or URL classes would
            # raise a ValueError
            with pytest.raises(ValueError):
                setattr(obj, field, 123)


@pytest.mark.parametrize("cls", [ProductVariant, Product, ProductFromList])
def test_webpoet_URL_mainImage(cls):
    response = HttpResponse("https://www.some-page", b"")
    data = {
        "mainImage": {
            "url": response.urljoin("img1.png"),
        },
        "url": response.url,
    }
    assert type(data["mainImage"]["url"]) == RequestUrl

    # The URL classes should be converted to strings on instantiation
    obj = cls.from_dict(data)
    assert type(obj.mainImage) == Image
    assert obj.mainImage.url == "https://www.some-page/img1.png"

    # The conversion should also work via field assignment
    img_url = response.urljoin("/different-img.png")
    assert type(img_url) == RequestUrl
    obj.mainImage.url = img_url
    assert type(obj.mainImage) == Image
    assert obj.mainImage.url == "https://www.some-page/different-img.png"

    # Setting other values that are not strings or URL classes would
    # raise a ValueError
    with pytest.raises(ValueError):
        obj.mainImage.url = False

    data = {"mainImage": {"url": 123}, "url": 123}
    with pytest.raises(ValueError):
        obj = cls.from_dict(data)


@pytest.mark.parametrize("cls", [ProductVariant, Product])
def test_webpoet_URL_images(cls):
    response = HttpResponse("https://www.some-page", b"")
    data = {
        "images": [
            {"url": response.urljoin("img1.png")},
            {"url": response.urljoin("img2.png")},
        ],
        "url": response.url,
    }
    assert type(data["images"][0]["url"]) == RequestUrl

    # The URL classes should be converted to strings on instantiation
    obj = cls.from_dict(data)
    assert type(obj.images[0]) == Image
    assert [img.url for img in obj.images] == [
        "https://www.some-page/img1.png",
        "https://www.some-page/img2.png",
    ]

    # The conversion should also work via field assignment
    img_url = response.urljoin("/different-img.png")
    assert type(img_url) == RequestUrl
    obj.images[0].url = img_url
    assert type(obj.images[0]) == Image
    assert obj.images[0].url == "https://www.some-page/different-img.png"

    # Setting other values that are not strings or URL classes would
    # raise a ValueError
    with pytest.raises(ValueError):
        obj.images[1].url = False

    data = {
        "images": [
            {"url": 123},
            {"url": 456},
        ],
        "url": 789,
    }
    with pytest.raises(ValueError):
        obj = cls.from_dict(data)
