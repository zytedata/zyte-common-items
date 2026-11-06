import pytest

pytest.importorskip("scrapy")

from zyte_common_items import (
    Article,
    ArticleFromList,
    ArticleList,
    ArticleMetadata,
    Author,
    Brand,
    Image,
    JobPosting,
    ProbabilityMetadata,
    Product,
    ProductFromList,
    ProductList,
)
from zyte_common_items.ae import (
    AEArticle,
    AEArticleList,
    AEJobPosting,
    AEProduct,
    AEProductList,
    _convert_list_item_metadata,
    downgrade,
)
from zyte_common_items.components import BaseSalary

URL = "https://example.com"


def test_downgrade_unsupported_item():
    item = Image(url=URL)
    assert downgrade(item) is item


def test_metadata_without_probability():
    item = Article(url=URL, metadata=ArticleMetadata(probability=None))
    assert AEArticle.from_item(item).probability == 1.0


def test_authors():
    item = Article(
        url=URL,
        authors=[Author(nameRaw="Raw Name"), Author(nameRaw="Other", name="Name")],
    )
    assert AEArticle.from_item(item).author == "Raw Name"


def test_authors_without_names():
    item = Article(url=URL, authors=[Author(email="a@example.com")])
    assert AEArticle.from_item(item).author is None


def test_image_urls_all_empty():
    item = Article(url=URL, images=[Image(url="")])
    assert AEArticle.from_item(item).images == []


def test_main_image_without_url():
    item = Article(url=URL, mainImage=Image(url=""))
    assert AEArticle.from_item(item).mainImage is None


def test_article_list_metadata():
    item = ArticleList(
        url=URL,
        articles=[
            ArticleFromList(url=URL, metadata=ProbabilityMetadata(probability=0.5)),
            ArticleFromList(url=URL, metadata=ProbabilityMetadata(probability=None)),
        ],
    )
    articles = AEArticleList.from_item(item).articles
    assert [article.probability for article in articles] == [0.5, 1.0]


def test_job_posting_salary_without_max_value():
    item = JobPosting(url=URL, baseSalary=BaseSalary(raw="Competitive"))
    assert AEJobPosting.from_item(item).baseSalary.raw == "Competitive"  # type: ignore[union-attr]


def test_job_posting_salary_with_max_value():
    item = JobPosting(
        url=URL, baseSalary=BaseSalary(valueMax="10.5", currencyRaw="EUR")
    )
    salary = AEJobPosting.from_item(item).baseSalary
    assert salary.value == 10.5  # type: ignore[union-attr]
    assert salary.currency == "EUR"  # type: ignore[union-attr]


def test_product_brand_without_name():
    item = Product(url=URL, brand=Brand(name=""))
    assert AEProduct.from_item(item).brand is None


def test_product_list_metadata():
    item = ProductList(
        url=URL,
        products=[
            ProductFromList(url=URL, metadata=ProbabilityMetadata(probability=0.5)),
            ProductFromList(url=URL, metadata=ProbabilityMetadata(probability=None)),
        ],
    )
    products = AEProductList.from_item(item).products
    assert [product.probability for product in products] == [0.5, 1.0]


@pytest.mark.parametrize(
    ("item", "expected"),
    [
        ({}, {"probability": 1.0}),
        ({"metadata": {}}, {"probability": 1.0}),
        ({"metadata": {"probability": 0.5}}, {"probability": 0.5}),
        ({"metadata": {"other": "value"}}, {"probability": 1.0}),
    ],
)
def test_convert_list_item_metadata(item, expected):
    _convert_list_item_metadata(item)
    assert item == expected
