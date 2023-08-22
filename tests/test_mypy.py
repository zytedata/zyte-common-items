"""This test file is ignored by mypy since we're using pytest-mypy-testing to
assert the mypy errors that should be raised.

Despite some mypy errors, some fields will still attempt proper value conversions
to the proper type. If the given value cannot be converted, a ValueError is raised.
See ``tests/test_conversion.py`` for the conversion checks.

Assertions in mypy are done via these line comments:
    # N: <msg> - assert a mypy note message
    # W: <msg> - assert a mypy warning message
    # E: <msg> - assert a mypy error message
    # R: <msg> - assert a mypy note message Revealed type is '<msg>'.

NOTE:
    Pytest's parametrization doesn't work here due to the dynamic nature of
    variables in each line. For-loops also doesn't work well since the type
    checker needs to narrow down on the type within the test function's scope.
"""

import pytest
from web_poet import HttpResponse

from zyte_common_items import (
    Breadcrumb,
    Image,
    Link,
    Product,
    ProductFromList,
    ProductList,
    ProductVariant,
)

URL = "https://www.some-page/"
RESPONSE = HttpResponse(URL, b"")


# NOTES: The following test cases below for assigning ``ResponseUrl`` instances
# are marked with "xfail" due to the following known mypy bugs:
#   - https://github.com/python/mypy/issues/10187
#   - https://github.com/python/mypy/issues/5313
#   - https://github.com/python-attrs/attrs/issues/889
# Currently, the said bugs causes mypy to raise the following error:
#   'Incompatible types in assignment (expression has type "ResponseUrl",
#   variable has type "Optional[str]")'
# FIXME: Unmark these from "xfail" once the upstream mypy issues are solved.


@pytest.mark.mypy_testing
@pytest.mark.xfail
def test_assignment_image_url():
    img = Image(url=RESPONSE.url)
    img.url = RESPONSE.url


@pytest.mark.mypy_testing
@pytest.mark.xfail
def test_assignment_breadcrumb_url():
    bc = Breadcrumb(url=RESPONSE.url)
    bc.url = RESPONSE.url


@pytest.mark.mypy_testing
@pytest.mark.xfail
def test_assignment_link_url():
    link = Link(url=RESPONSE.url)
    link.url = RESPONSE.url


@pytest.mark.mypy_testing
@pytest.mark.xfail
def test_assignment_product_url():
    product_1 = Product(url=RESPONSE.url)
    product_1.url = RESPONSE.url

    product_2 = Product(url=RESPONSE.url)
    product_2.canonicalUrl = RESPONSE.url


@pytest.mark.mypy_testing
@pytest.mark.xfail
def test_assignment_product_list_url():
    product_list_1 = ProductList(url=RESPONSE.url)
    product_list_1.url = RESPONSE.url

    product_list_2 = ProductList(url=RESPONSE.url)
    product_list_2.canonicalUrl = RESPONSE.url


@pytest.mark.mypy_testing
@pytest.mark.xfail
def test_assignment_product_from_list_url():
    product_from_list_1 = ProductFromList(url=RESPONSE.url)
    product_from_list_1.url = RESPONSE.url


@pytest.mark.mypy_testing
@pytest.mark.xfail
def test_assignment_product_variant_url():
    product_variant_1 = ProductVariant(url=RESPONSE.url)
    product_variant_1.url = RESPONSE.url

    product_variant_2 = ProductVariant(url=RESPONSE.url)
    product_variant_2.canonicalUrl = RESPONSE.url


@pytest.mark.mypy_testing
def test_assignment_image():
    img_1 = Image(url=RESPONSE.url)
    img_1.url = str(RESPONSE.url)

    img_2 = Image(url=RESPONSE.url)
    img_2.url = "https://www.example.com"


@pytest.mark.mypy_testing
def test_assignment_breadcrumb():
    bc_1 = Breadcrumb(url=RESPONSE.url)
    bc_1.url = str(RESPONSE.url)

    bc_2 = Breadcrumb(url=RESPONSE.url)
    bc_2.url = "https://www.example.com"


@pytest.mark.mypy_testing
def test_assignment_link():
    link_1 = Link(url=RESPONSE.url)
    link_1.url = str(RESPONSE.url)

    link_2 = Link(url=RESPONSE.url)
    link_2.url = "https://www.example.com"


@pytest.mark.mypy_testing
def test_assignment_product():
    product_1 = Product(url=RESPONSE.url)
    product_1.url = str(RESPONSE.url)

    product_2 = Product(url=RESPONSE.url)
    product_2.url = "https://www.example.com"

    product_3 = Product(url=RESPONSE.url)
    product_3.canonicalUrl = str(RESPONSE.url)

    product_4 = Product(url=RESPONSE.url)
    product_4.canonicalUrl = "https://www.example.com"


@pytest.mark.mypy_testing
def test_assignment_product_list():
    product_list_1 = ProductList(url=RESPONSE.url)
    product_list_1.url = str(RESPONSE.url)

    product_list_2 = ProductList(url=RESPONSE.url)
    product_list_2.url = "https://www.example.com"

    product_list_3 = ProductList(url=RESPONSE.url)
    product_list_3.canonicalUrl = str(RESPONSE.url)

    product_list_4 = ProductList(url=RESPONSE.url)
    product_list_4.canonicalUrl = "https://www.example.com"


@pytest.mark.mypy_testing
def test_assignment_product_from_list():
    product_from_list_1 = ProductFromList(url=RESPONSE.url)
    product_from_list_1.url = str(RESPONSE.url)

    product_from_list_2 = ProductFromList(url=RESPONSE.url)
    product_from_list_2.url = "https://www.example.com"


@pytest.mark.mypy_testing
def test_assignment_product_variant():
    product_variant_1 = ProductVariant(url=RESPONSE.url)
    product_variant_1.url = str(RESPONSE.url)

    product_variant_2 = ProductVariant(url=RESPONSE.url)
    product_variant_2.url = "https://www.example.com"

    product_variant_3 = ProductVariant(url=RESPONSE.url)
    product_variant_3.canonicalUrl = str(RESPONSE.url)

    product_variant_4 = ProductVariant(url=RESPONSE.url)
    product_variant_4.canonicalUrl = "https://www.example.com"


@pytest.mark.mypy_testing
def test_instantiation_image():
    with pytest.raises(ValueError):
        Image(
            url=123  # E: Argument "url" to "Image" has incompatible type "int"; expected "str | _Url"  [arg-type]
        )


@pytest.mark.mypy_testing
def test_instantiation_breadcrumb():
    with pytest.raises(ValueError):
        Breadcrumb(
            url=123  # E: Argument "url" to "Breadcrumb" has incompatible type "int"; expected "str | _Url | None"  [arg-type]
        )


@pytest.mark.mypy_testing
def test_instantiation_link():
    with pytest.raises(ValueError):
        Link(
            url=123  # E: Argument "url" to "Link" has incompatible type "int"; expected "str | _Url | None"  [arg-type]
        )


@pytest.mark.mypy_testing
def test_instantiation_product_list():
    with pytest.raises(ValueError):
        ProductList(
            url=123  # E: Argument "url" to "ProductList" has incompatible type "int"; expected "str | _Url"  [arg-type]
        )
    with pytest.raises(ValueError):
        ProductList(
            url="https://www.example.com",
            canonicalUrl=123,  # E: Argument "canonicalUrl" to "ProductList" has incompatible type "int"; expected "str | _Url | None"  [arg-type]
        )


@pytest.mark.mypy_testing
def test_instantiation_product_from_list():
    with pytest.raises(ValueError):
        ProductFromList(
            url=123  # E: Argument "url" to "ProductFromList" has incompatible type "int"; expected "str | _Url | None"  [arg-type]
        )


@pytest.mark.mypy_testing
def test_instantiation_product_variant():
    with pytest.raises(ValueError):
        ProductVariant(
            url=123  # E: Argument "url" to "ProductVariant" has incompatible type "int"; expected "str | _Url | None"  [arg-type]
        )
    with pytest.raises(ValueError):
        ProductVariant(
            url="https://www.example.com",
            canonicalUrl=123,  # E: Argument "canonicalUrl" to "ProductVariant" has incompatible type "int"; expected "str | _Url | None"  [arg-type]
        )
