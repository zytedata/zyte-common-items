from zyte_common_items import Product
from zyte_common_items.pipelines import (
    AEGTIN,
    AEAdditionalProperty,
    AEBreadcrumb,
    AEOffer,
    AEPipeline,
    AEProduct,
    AERating,
)

from .test_items import _PRODUCT_ALL_KWARGS


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
                link=None,
            ),
            AEBreadcrumb(
                name="Level 2",
                link=None,
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
    )
