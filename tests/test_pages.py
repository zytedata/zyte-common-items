import warnings
from datetime import datetime
from typing import Optional
from warnings import catch_warnings

import attrs
import pytest
from web_poet import HttpResponse, RequestUrl, ResponseUrl, Returns, field

import zyte_common_items
from zyte_common_items import (
    BaseProductListPage,
    BaseProductNavigationPage,
    BaseProductPage,
    HasMetadata,
    Metadata,
    Page,
    ProbabilityMetadata,
    ProbabilityRequest,
    Product,
    ProductFromList,
    ProductListMetadata,
    ProductListPage,
    ProductMetadata,
    ProductPage,
    Request,
)


@pytest.mark.parametrize(
    "page_class",
    (
        BaseProductPage,
        BaseProductListPage,
    ),
)
def test_base_pages_default(page_class):
    page = page_class(request_url=RequestUrl("https://example.com"))
    assert page.url == "https://example.com"
    assert isinstance(page.url, str)
    # NOTE: test_metadata covers .metadata


@pytest.mark.parametrize(
    "page_class",
    (
        ProductPage,
        ProductListPage,
    ),
)
def test_pages_default(page_class):
    url = ResponseUrl("https://example.com")
    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <h1>Foo</h1>
        </body>
    </html>
    """
    response = HttpResponse(url=url, body=html)
    page = page_class(response=response)
    assert page.url == "https://example.com"
    assert isinstance(page.url, str)
    # NOTE: test_metadata covers .metadata


@pytest.mark.asyncio
async def test_example():
    datetime_before = datetime.utcnow().replace(microsecond=0)

    @attrs.define
    class BookPage(ProductPage):
        @field
        def name(self):
            return self.css("h1::text").get()

    url = ResponseUrl("https://example.com/books/1")
    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <h1>Foo</h1>
        </body>
    </html>
    """
    response = HttpResponse(url=url, body=html)

    item = await BookPage(response=response).to_item()

    assert item.url == str(url)
    assert item.name == "Foo"
    assert item.metadata.probability == 1.0

    item_datetime_string = item.metadata.dateDownloaded
    assert item_datetime_string.endswith("Z")
    item_datetime = datetime.fromisoformat(item_datetime_string[:-1])
    datetime_after = datetime.utcnow().replace(microsecond=0)
    assert datetime_before <= item_datetime <= datetime_after


@pytest.mark.asyncio
async def test_mixin_leak():
    """https://github.com/zytedata/zyte-common-items/pull/29"""

    class MyProductListPage(ProductListPage):
        @field
        def products(self):
            return [{"name": "foo"}, {"name": "bar"}]

    class MyProductPage(ProductPage):
        @field
        def brand(self):
            return "baz"

    from web_poet.fields import get_fields_dict

    assert set(get_fields_dict(MyProductListPage)) == {"metadata", "products", "url"}
    assert set(get_fields_dict(MyProductPage)) == {
        "brand",
        "currency",
        "currencyRaw",
        "description",
        "descriptionHtml",
        "metadata",
        "url",
    }


@pytest.mark.asyncio
async def test_no_item_found_Page():
    class MyProductPage(ProductPage):
        def validate_input(self):
            return self.no_item_found()

    response = HttpResponse(url="http://example.com", body=b"<html></html>")
    page = MyProductPage(response=response)

    item = await page.to_item()
    assert item.metadata.probability == 0
    assert item.url == "http://example.com"


@pytest.mark.asyncio
async def test_no_item_found_BasePage():
    class MyProductPage(BaseProductPage):
        def validate_input(self):
            return self.no_item_found()

    page = MyProductPage(request_url=RequestUrl("http://example.com"))

    item = await page.to_item()
    assert item.metadata.probability == 0
    assert item.url == "http://example.com"


def test_page_pairs():
    """For every page, a base page and an auto page, and vice versa."""
    pages = {
        obj_name
        for obj_name in zyte_common_items.__dict__
        if (
            not (obj_name.startswith("Base") or obj_name.startswith("Auto"))
            and obj_name.endswith("Page")
            and obj_name != "Page"
        )
    }

    actual_base_pages = {
        obj_name
        for obj_name in zyte_common_items.__dict__
        if (
            obj_name.startswith("Base")
            and obj_name.endswith("Page")
            and obj_name != "BasePage"
        )
    }
    expected_base_pages = {f"Base{page}" for page in pages}
    assert actual_base_pages == expected_base_pages

    actual_auto_pages = {
        obj_name
        for obj_name in zyte_common_items.__dict__
        if (obj_name.startswith("Auto") and obj_name.endswith("Page"))
    }
    expected_auto_pages = {f"Auto{page}" for page in pages}
    assert actual_auto_pages == expected_auto_pages


def test_matching_items():
    """For every page, an item."""
    pages = {
        obj_name
        for obj_name in zyte_common_items.__dict__
        if (
            not (obj_name.startswith("Base") or obj_name.startswith("Auto"))
            and obj_name.endswith("Page")
            and obj_name != "Page"
        )
    }
    for page in pages:
        item = page[:-4]
        assert item in zyte_common_items.__dict__


METADATA_FIELDS = {
    "Article": {"dateDownloaded", "probability"},
    "ArticleList": {"dateDownloaded"},
    "ArticleNavigation": {"dateDownloaded"},
    "BusinessPlace": {"dateDownloaded", "probability", "searchText"},
    "Product": {"dateDownloaded", "probability"},
    "ProductList": {"dateDownloaded"},
    "ProductNavigation": {"dateDownloaded"},
    "RealEstate": {"dateDownloaded", "probability"},
    "JobPosting": {"dateDownloaded", "probability", "searchText"},
    "SocialMediaPost": {"dateDownloaded", "probability", "searchText"},
}


def check_default_metadata(cls, kwargs, item_name):
    start = datetime.utcnow().replace(microsecond=0)

    obj = cls(**kwargs)

    metadata_cls = zyte_common_items.__dict__[f"{item_name}Metadata"]
    assert type(obj.metadata) == metadata_cls

    expected_fields = METADATA_FIELDS[item_name]

    def allow_field(field_name):
        for prefix in ["_", "from_", "get_"]:
            if field_name.startswith(prefix):
                return False
        return True

    actual_fields = {field for field in dir(obj.metadata) if allow_field(field)}
    error_message = (
        f"{metadata_cls}: actual fields ({actual_fields}) != expected fields "
        f"({expected_fields})"
    )
    assert actual_fields == expected_fields, error_message

    if "dateDownloaded" in actual_fields:
        assert isinstance(
            obj.metadata.dateDownloaded, str
        ), f"{cls} does not get dateDownloaded set by default"
        assert obj.metadata.dateDownloaded.endswith("Z")
        actual = datetime.fromisoformat(obj.metadata.dateDownloaded[:-1])
        end = datetime.utcnow().replace(microsecond=0)
        assert start <= actual <= end

    if "probability" in actual_fields:
        assert isinstance(obj.metadata.probability, float)
        assert obj.metadata.probability == 1.0


def test_metadata():
    """Test metadata expectations for pages.

    For every type-specific page and base page:

    -   There must be a matching metadata class.

    -   The metadata attribute must be of that metadata class.

    -   The default value of metadata must have dateDownloaded and probability
        filled if available in the metadata class.
    """
    pages = {
        obj_name
        for obj_name in zyte_common_items.__dict__
        if (
            not (obj_name.startswith("Base") or obj_name.startswith("Auto"))
            and obj_name.endswith("Page")
            and obj_name != "Page"
        )
    }

    for page in pages:
        item_name = page[:-4]

        page_cls = getattr(zyte_common_items, page)
        response_url = ResponseUrl("https://example.com")
        html = b"""
        <!DOCTYPE html>
        <html>
            <body>
                <h1>Foo</h1>
            </body>
        </html>
        """
        page_kwargs = {"response": HttpResponse(url=response_url, body=html)}
        check_default_metadata(page_cls, page_kwargs, item_name)

        base_page = f"Base{page}"
        base_page_cls = getattr(zyte_common_items, base_page)
        base_page_kwargs = {"request_url": RequestUrl("https://example.com")}
        check_default_metadata(base_page_cls, base_page_kwargs, item_name)


def test_metadata_generic():
    """Ensure that when a subclass returns an instance of the generic Metadata
    class, it gets replaced by the corresponding, more specific metadata
    class."""

    class CustomProductPage(ProductPage):
        @field
        def metadata(self):
            return Metadata(dateDownloaded="foo", probability=0.5)

    url = ResponseUrl("https://example.com")
    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <h1>Foo</h1>
        </body>
    </html>
    """
    page1 = CustomProductPage(response=HttpResponse(url=url, body=html))
    with catch_warnings():
        warnings.simplefilter("error")
        metadata1 = page1.metadata
    assert type(metadata1) == ProductMetadata
    assert metadata1.dateDownloaded == "foo"
    assert metadata1.probability == 0.5

    class ExtraAttrProductPage(ProductPage):
        @field
        def metadata(self):
            return Metadata(dateDownloaded="foo", probability=0.5, searchText="bar")

    page2 = ExtraAttrProductPage(response=HttpResponse(url=url, body=html))
    with pytest.warns(RuntimeWarning, match=r"dropping the non-default values"):
        metadata2 = page2.metadata
    assert type(metadata2) == ProductMetadata
    assert metadata2.dateDownloaded == "foo"
    assert metadata2.probability == 0.5

    class DefaultAttrProductListPage(ProductListPage):
        @field
        def metadata(self):
            return Metadata(dateDownloaded="foo", probability=1.0)

        @field
        def products(self):
            return [ProductFromList(url=url, metadata=Metadata())]

    page3 = DefaultAttrProductListPage(response=HttpResponse(url=url, body=html))
    with catch_warnings():
        warnings.simplefilter("error")
        metadata3 = page3.metadata
        metadata4 = page3.products[0].metadata
    assert type(metadata3) == ProductListMetadata
    assert metadata3.dateDownloaded == "foo"
    assert not hasattr(metadata3, "probability")
    assert type(metadata4) == ProbabilityMetadata
    assert metadata4.probability == 1.0


def test_metadata_override():
    """Test using HasMetadata to override the metadata class."""

    @attrs.define(kw_only=True)
    class CustomProductMetadata(ProductMetadata):
        new_field: Optional[str] = None

    class CustomProductPage(ProductPage, HasMetadata[CustomProductMetadata]):
        @field
        def metadata(self):
            return Metadata(dateDownloaded="foo", probability=0.5)

    url = ResponseUrl("https://example.com")
    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <h1>Foo</h1>
        </body>
    </html>
    """
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    metadata = page.metadata
    assert type(metadata) == CustomProductMetadata
    assert metadata.new_field is None


def test_hasmetadata_inheritance():
    """Ensure that a subclass with just Returns doesn't break _get_metadata_class()."""

    class MyProduct(Product):
        pass

    class CustomProductPage(ProductPage, Returns[MyProduct]):
        pass

    url = ResponseUrl("https://example.com")
    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <h1>Foo</h1>
        </body>
    </html>
    """
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    metadata = page.metadata
    assert type(metadata) == ProductMetadata


def test_metadata_cls_none():
    """Ensure that metadata_cls can be None."""

    class CustomProductPage(Page, Returns[Product]):
        pass

    url = ResponseUrl("https://example.com")
    html = b"""
    <!DOCTYPE html>
    <html>
        <body>
            <h1>Foo</h1>
        </body>
    </html>
    """
    page = CustomProductPage(response=HttpResponse(url=url, body=html))
    with pytest.raises(ValueError):
        page.metadata


def test_request():
    """Test Request class conversion"""

    class CustomNavPage(BaseProductNavigationPage):
        @field
        def subCategories(self):
            return [Request(url="https://example.com")]

        @field
        def items(self):
            return [Request(url="https://example.com")]

        @field
        def nextPage(self):
            return Request(url="https://example.com")

    url = RequestUrl("https://example.com")
    page = CustomNavPage(url)
    for request in [page.subCategories[0], page.items[0]]:
        assert type(request) == ProbabilityRequest
        assert request.metadata is not None
        assert request.metadata.probability == 1.0
    assert type(page.nextPage) == Request
