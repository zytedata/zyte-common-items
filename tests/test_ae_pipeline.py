import pytest

from zyte_common_items import Article, ArticleList, JobPosting, Product, ProductList
from zyte_common_items.ae import (
    AEGTIN,
    AEAdditionalProperty,
    AEArticle,
    AEArticleFromList,
    AEArticleList,
    AEBreadcrumb,
    AEJobPosting,
    AELocation,
    AEOffer,
    AEOrganization,
    AEPaginationLink,
    AEProduct,
    AEProductFromList,
    AEProductList,
    AERating,
    AESalary,
)
from zyte_common_items.pipelines import AEPipeline

from .test_items import (
    _ARTICLE_ALL_KWARGS,
    _ARTICLE_LIST_ALL_KWARGS,
    _ARTICLE_LIST_MIN_KWARGS,
    _ARTICLE_MIN_KWARGS,
    _JOB_POSTING_ALL_KWARGS,
    _JOB_POSTING_MIN_KWARGS,
    _PRODUCT_ALL_KWARGS,
    _PRODUCT_LIST_ALL_KWARGS,
    _PRODUCT_LIST_MIN_KWARGS,
    _PRODUCT_MIN_KWARGS,
)


@pytest.mark.parametrize(
    ["item", "expected"],
    (
        (
            Article(**_ARTICLE_MIN_KWARGS),
            AEArticle(
                probability=1.0,
                url="https://www.zyte.com/blog/product-data-extraction-automatic",
            ),
        ),
        (
            Article(**_ARTICLE_ALL_KWARGS),
            AEArticle(
                headline="Guarantee the best results for product data extraction",
                datePublished="2022-08-26T20:56:16Z",
                datePublishedRaw="August 26, 2022",
                dateModified="2022-08-27T21:48:55Z",
                dateModifiedRaw="August 25, 2022",
                inLanguage="en",
                breadcrumbs=[
                    AEBreadcrumb(name="Homepage"),
                    AEBreadcrumb(name="Blog"),
                    AEBreadcrumb(
                        name="Guarantee the best results for product data extraction",
                    ),
                ],
                mainImage="https://www.zyte.com/wp-content/uploads/2022/08/product-data-extraction-zyte.png",
                images=[
                    "https://www.zyte.com/wp-content/uploads/2022/08/product-data-extraction-zyte.png",
                    "https://www.zyte.com/wp-content/uploads/2021/06/Webinar_Product-Data-Quality-01-1024x536.png",
                    "https://www.zyte.com/wp-content/uploads/2022/08/product-data-extraction-automatic.png",
                ],
                description="Product Data Extraction helps understand how consumers use a specific product, foresee improvements and adjustments that ultimately increase sales and demand.",
                articleBody="When businesses operate in a competitive environment it is imperative to know what their competitors are charging in real-time and this can be hard to keep track of. For any data driven organization, implementing a solution that automatically extracts product data from websites in real-time and at scale, is indispensable to stay ahead of the competition. Setting an automatic process for product data extraction can be a powerful tool for data driven businesses of all sizes. You can extract specific products information including offers, price, currency, and availability. Provided that the data extraction process is able to identify the key attributes of a product, it can then use this information to create reports with insights into the behavior of a particular product. For this to work, it is key to have the right procedures in place that guarantee the best results for your automation product extraction projects. By doing so, your organization can better understand how consumers are using a specific product, foresee any necessary adjustments to improve the user experience and as a result, increase sales and demand. In this article, we'll explain not just everything you need to know to get started, but also show you how to guarantee the best results when working with product data extraction.\n\nWhat is automatic product extraction?\n\n...",
                articleBodyHtml='<article>\n<p>When businesses operate in a competitive environment it is imperative to know what their competitors are charging in real-time and this can be hard to keep track of. For any data driven organization, implementing a solution that automatically extracts product data from websites in real-time and at scale, is indispensable to stay ahead of the competition.</p> <p>Setting an automatic process for <a href="https://docs.zyte.com/automatic-extraction/product.html">product data extraction</a> can be a powerful tool for data driven businesses of all sizes. You can extract specific products information including offers, price, currency, and availability. Provided that the data extraction process is able to <a href="/blog/automatic-extraction-data-extractor-review/">identify the key attributes of a product</a>, it can then use this information to create reports with insights into the behavior of a particular product.</p>\n<p>For this to work, it is key to have the right procedures in place that guarantee the best results for your automation product extraction projects. By doing so, your organization can better understand how consumers are using a specific product, foresee any necessary adjustments to improve the user experience and as a result, increase sales and demand.</p>\n<p>In this article, we\'ll explain not just everything you need to know to get started, but also show you how to guarantee the best results when working with product data extraction.</p>\n<h2><strong>What is automatic product extraction?</strong></h2>\n...\n</article>',
                videoUrls=[
                    "https://player.vimeo.com/video/90592864?title=0&byline=0&portrait=0&color=8dc7dc"
                ],
                audioUrls=["https://example.com/audiofile.mp3"],
                probability=1.0,
                canonicalUrl="https://www.zyte.com/blog/product-data-extraction-automatic/",
                url="https://www.zyte.com/blog/product-data-extraction-automatic",
            ),
        ),
        (
            ArticleList(**_ARTICLE_LIST_MIN_KWARGS),
            AEArticleList(
                url="https://www.zyte.com/blog/extract-summit-blog/",
            ),
        ),
        (
            ArticleList(**_ARTICLE_LIST_ALL_KWARGS),
            AEArticleList(
                url="https://www.zyte.com/blog/extract-summit-blog/",
                articles=[
                    AEArticleFromList(
                        url="https://www.zyte.com/blog/reflecting-on-the-2022-web-data-extraction-summit-zyte/",
                        probability=1.0,
                    )
                ],
            ),
        ),
        (
            JobPosting(**_JOB_POSTING_MIN_KWARGS),
            AEJobPosting(
                probability=1.0,
                url="https://example.com/viewjob/12345",
            ),
        ),
        (
            JobPosting(**_JOB_POSTING_ALL_KWARGS),
            AEJobPosting(
                title="Software Engineer",
                datePosted="2019-06-19T00:00:00-05:00",
                validThrough="2019-07-19T00:00:00-05:00",
                description="We are looking for a Software Engineer to join our team.- 35 days holiday- 15% bonus- flexible working arrangements",
                descriptionHtml="<p>We are looking for a Software Engineer to join our team.</p><ul><li>35 days holiday</li><li>15% bonus</li><li>flexible working arrangements</li></ul>",
                employmentType="Full-time",
                hiringOrganization=AEOrganization(raw="ACME Corp."),
                baseSalary=AESalary(
                    raw="$53,000-$55,000 a year", value=55000.0, currency="$"
                ),
                jobLocation=AELocation(raw="New York, NY"),
                probability=0.95,
                url="https://example.com/viewjob/12345",
            ),
        ),
        (
            Product(**_PRODUCT_MIN_KWARGS),
            AEProduct(
                probability=1.0,
                url="https://example.com/?product=product22",
            ),
        ),
        (
            Product(**_PRODUCT_ALL_KWARGS),
            AEProduct(
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
            ),
        ),
        (
            ProductList(**_PRODUCT_LIST_MIN_KWARGS),
            AEProductList(
                url="https://example.com/swiss-watches?sort=new-first",
            ),
        ),
        (
            ProductList(**_PRODUCT_LIST_ALL_KWARGS),
            AEProductList(
                url="https://example.com/swiss-watches?sort=new-first",
                products=[AEProductFromList(probability=1.0)],
                breadcrumbs=[
                    AEBreadcrumb(name="Level 1"),
                    AEBreadcrumb(name="Level 2"),
                ],
                paginationNext=AEPaginationLink(
                    url="https://example.com/swiss-watches?sort=new-first&page=2",
                    text="foo",
                ),
            ),
        ),
    ),
)
def test_main(item, expected):
    pipeline = AEPipeline()
    actual = pipeline.process_item(item, spider=None)
    assert expected == actual
