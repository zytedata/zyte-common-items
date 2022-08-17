"""This test file is ignored by mypy since we're using pytest-mypy-testing to
assert the mypy errors that should be raised.

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

response = HttpResponse("https://www.some-page/", b"")


@pytest.mark.mypy_testing
def test_assignment_image():
    img_1 = Image(url=response.url)
    img_1.url = response.url

    img_2 = Image(url=response.url)
    img_2.url = str(response.url)

    img_3 = Image(url=response.url)
    img_3.url = 123  # E: Incompatible types in assignment (expression has type "int", variable has type "str")


@pytest.mark.mypy_testing
def test_assignment_breadcrumb():
    bc_1 = Breadcrumb(url=response.url)
    bc_1.url = response.url

    bc_2 = Breadcrumb(url=response.url)
    bc_2.url = str(response.url)

    bc_3 = Breadcrumb(url=response.url)
    bc_3.url = 123  # E: Incompatible types in assignment (expression has type "int", variable has type "Optional[str]")


@pytest.mark.mypy_testing
def test_assignment_link():
    link_1 = Link(url=response.url)
    link_1.url = response.url

    link_2 = Link(url=response.url)
    link_2.url = str(response.url)

    link_3 = Link(url=response.url)
    link_3.url = (
        123  # E: Incompatible types in assignment (expression has type "int", variable has type "Optional[str]")
    )


@pytest.mark.mypy_testing
def test_assignment_product():
    product_1 = Product(url=response.url)
    product_1.url = response.url

    product_2 = Product(url=response.url)
    product_2.url = str(response.url)

    product_3 = Product(url=response.url)
    product_3.url = 123  # E: Incompatible types in assignment (expression has type "int", variable has type "str")

    product_4 = Product(url=response.url)
    product_4.canonicalUrl = response.url

    product_5 = Product(url=response.url)
    product_5.canonicalUrl = str(response.url)

    product_6 = Product(url=response.url)
    product_6.canonicalUrl = (
        123  # E: Incompatible types in assignment (expression has type "int", variable has type "Optional[str]")
    )


@pytest.mark.mypy_testing
def test_assignment_product_list():
    product_list_1 = ProductList(url=response.url)
    product_list_1.url = response.url

    product_list_2 = ProductList(url=response.url)
    product_list_2.url = str(response.url)

    product_list_3 = ProductList(url=response.url)
    product_list_3.url = 123  # E: Incompatible types in assignment (expression has type "int", variable has type "str")

    product_list_4 = ProductList(url=response.url)
    product_list_4.canonicalUrl = response.url

    product_list_5 = ProductList(url=response.url)
    product_list_5.canonicalUrl = str(response.url)

    product_list_6 = ProductList(url=response.url)
    product_list_6.canonicalUrl = (
        123  # E: Incompatible types in assignment (expression has type "int", variable has type "Optional[str]")
    )


@pytest.mark.mypy_testing
def test_assignment_product_from_list():
    product_from_list_1 = ProductFromList(url=response.url)
    product_from_list_1.url = response.url

    product_from_list_2 = ProductFromList(url=response.url)
    product_from_list_2.url = str(response.url)

    product_from_list_3 = ProductFromList(url=response.url)
    product_from_list_3.url = (
        123  # E: Incompatible types in assignment (expression has type "int", variable has type "Optional[str]")
    )


@pytest.mark.mypy_testing
def test_assignment_product_variant():
    product_variant_1 = ProductVariant(url=response.url)
    product_variant_1.url = response.url

    product_variant_2 = ProductVariant(url=response.url)
    product_variant_2.url = str(response.url)

    product_variant_3 = ProductVariant(url=response.url)
    product_variant_3.url = (
        123  # E: Incompatible types in assignment (expression has type "int", variable has type "Optional[str]")
    )

    product_variant_4 = ProductVariant(url=response.url)
    product_variant_4.canonicalUrl = response.url

    product_variant_5 = ProductVariant(url=response.url)
    product_variant_5.canonicalUrl = str(response.url)

    product_variant_6 = ProductVariant(url=response.url)
    product_variant_6.canonicalUrl = (
        123  # E: Incompatible types in assignment (expression has type "int", variable has type "Optional[str]")
    )


# NOTE: The tests below are marked to fail since the following error is
# encountered in mypy:
#
#   "error: Skipping analyzing "web_poet": module is installed, but missing
#   library stubs or py.typed marker"
#
# This means that mypy renders all contents (i.e. URL classes) from web-poet to
# be of type Any. To fix this, web-poet must either be PEP 561 complient with
# or register at typeshed
#
# Reference:
#   https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-library-stubs-or-py-typed-marker


@pytest.mark.xfail
@pytest.mark.mypy_testing
def test_instantiation_image():
    Image(url=123)  # E: Argument "url" to "Image" has incompatible type "int"; expected "Union[str, Url]"


@pytest.mark.xfail
@pytest.mark.mypy_testing
def test_instantiation_breadcrumb():
    Breadcrumb(url=123)  # E: Argument "url" to "Breadcrumb" has incompatible type "int"; expected "Union[str, Url]"


@pytest.mark.xfail
@pytest.mark.mypy_testing
def test_instantiation_link():
    Link(url=123)  # E: Argument "url" to "Link" has incompatible type "int"; expected "Union[str, Url]"


@pytest.mark.xfail
@pytest.mark.mypy_testing
def test_instantiation_product_list():
    ProductList(url=123)  # E: Argument "url" to "ProductList" has incompatible type "int"; expected "Union[str, Url]"
    ProductList(
        url="https://www.example.com", canonicalUrl=123
    )  # E: Argument "canonicalUrl" to "ProductList" has incompatible type "int"; expected "Union[str, Url]"


@pytest.mark.xfail
@pytest.mark.mypy_testing
def test_instantiation_product_from_list():
    ProductFromList(
        url=123
    )  # E: Argument "url" to "ProductFromList" has incompatible type "int"; expected "Union[str, Url]"


@pytest.mark.xfail
@pytest.mark.mypy_testing
def test_instantiation_product_variant():
    ProductVariant(
        url=123
    )  # E: Argument "url" to "ProductVariant" has incompatible type "int"; expected "Union[str, Url]"
    ProductVariant(
        url="https://www.example.com", canonicalUrl=123
    )  # E: Argument "canonicalUrl" to "ProductList" has incompatible type "int"; expected "Union[str, Url]"
