from zyte_common_items import Product, ProductList
from zyte_common_items.pipelines import (
    AEGTIN,
    AEAdditionalProperty,
    AEBreadcrumb,
    AEOffer,
    AEPaginationLink,
    AEPipeline,
    AEProduct,
    AEProductFromList,
    AEProductList,
    AERating,
)

from .test_items import _PRODUCT_ALL_KWARGS, _PRODUCT_LIST_ALL_KWARGS


def test_product():
    product = Product(**_PRODUCT_ALL_KWARGS)
    pipeline = AEPipeline()
    ae_product = pipeline.process_item(product, spider=None)
    assert ae_product == AEProduct(
        url="https://example.com/?product=product22",
        canonicalUrl="https://example.com/product22",
        probability=1.0,
        name="White two-door refrigerator",
        offers=[
            AEOffer(
                price="9999.99",
                currency="$",
                availability="InStock",
                regularPrice="11999.99",
            ),
        ],
        sku="A123DK9823",
        gtin=[
            AEGTIN(
                type="foo",
                value="bar",
            ),
        ],
        mpn="HSC0424PP",
        brand="Ka-pow",
        breadcrumbs=[
            AEBreadcrumb(
                name="Level 1",
            ),
            AEBreadcrumb(
                name="Level 2",
            ),
        ],
        mainImage="http://example.com/image1.png",
        images=[
            "http://example.com/image1.png",
        ],
        description=(
            "Full freshness all over the fridge\n"
            "5 Conversion Modes on demand\n"
            "Super Cooling Plus™"
        ),
        descriptionHtml=(
            "<article>"
            "<p>Full freshness all over the fridge</p>"
            "<p>5 Conversion Modes on demand</p>"
            "<p>Super Cooling Plus&trade;</p>"
            "</article>"
        ),
        additionalProperty=[
            AEAdditionalProperty(
                name="foo",
                value="bar",
            ),
        ],
        aggregateRating=AERating(
            ratingValue=2.5,
            bestRating=5.0,
            reviewCount=123,
        ),
        color="white",
        size="XL",
        style="polka dots",
        hasVariants=[
            AEProduct(
                url="https://example.com/?product=product22",
                probability=1.0,
            )
        ],
    )


def test_product_list():
    product_list = ProductList(**_PRODUCT_LIST_ALL_KWARGS)
    pipeline = AEPipeline()
    ae_product_list = pipeline.process_item(product_list, spider=None)
    assert ae_product_list == AEProductList(
        url="https://example.com/swiss-watches?sort=new-first",
        products=[AEProductFromList(probability=1.0)],
        breadcrumbs=[
            AEBreadcrumb(name="Level 1"),
            AEBreadcrumb(name="Level 2"),
        ],
        paginationNext=AEPaginationLink(
            url="https://example.com/swiss-watches?sort=new-first&page=2", text="foo"
        ),
    )
