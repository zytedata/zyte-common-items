import attr
import pytest

from tests import crazy_monkey_nullify, load_fixture, temp_seed
from tests.typing import assert_type_compliance
from zyte_common_items import Item
from zyte_common_items.zyte_data_api import (
    GTIN,
    AdditionalProperty,
    Address,
    Area,
    Article,
    ArticleFromList,
    ArticleList,
    AvailableAtOrFrom,
    Breadcrumb,
    Comment,
    CommentList,
    ForumPost,
    ForumPostList,
    FuelEfficiency,
    JobPosting,
    Location,
    MileageFromOdometer,
    Offer,
    Organization,
    PaginationLink,
    Product,
    ProductFromList,
    ProductList,
    ProductRating,
    RealEstate,
    Review,
    ReviewList,
    ReviewRating,
    Salary,
    Topic,
    TradeAction,
    Vehicle,
    VehicleEngine,
    VehicleRating,
)

example_article_result = load_fixture("sample_article.json")[0]
example_article_list_result = load_fixture("sample_article_list.json")[0]
example_product_result = load_fixture("sample_product.json")[0]
example_product_list_result = load_fixture("sample_product_list.json")[0]
example_job_posting_result = load_fixture("sample_job_posting.json")[0]
example_comments_result = load_fixture("sample_comments.json")[0]
example_forum_post_list_result = load_fixture("sample_forum_post_list.json")[0]
example_real_estate_result = load_fixture("sample_real_estate.json")[0]
example_review_list_result = load_fixture("sample_review_list.json")[0]
example_vehicle_result = load_fixture("sample_vehicle.json")[0]


@pytest.mark.parametrize(
    "cls, data",
    [(Offer, offer) for offer in example_product_result["product"]["offers"]]
    + [(Breadcrumb, breadcrumb) for breadcrumb in example_product_result["product"]["breadcrumbs"]]  # type: ignore
    + [
        (AdditionalProperty, additionalProperty)  # type: ignore
        for additionalProperty in example_product_result["product"]["additionalProperty"]
    ]
    + [(GTIN, gtin) for gtin in example_product_result["product"]["gtin"]]  # type: ignore
    + [(ProductRating, example_product_result["product"]["aggregateRating"])]  # type: ignore
    + [(Product, example_product_result["product"])]  # type: ignore
    + [(Article, example_article_result["article"])]  # type: ignore
    + [(ArticleList, example_article_list_result["articleList"])]  # type: ignore
    + [(PaginationLink, example_product_list_result["productList"]["paginationNext"])]  # type: ignore
    + [(ProductList, example_product_list_result["productList"])]  # type: ignore
    + [(JobPosting, example_job_posting_result["jobPosting"])]  # type: ignore
    + [(CommentList, example_comments_result["comments"])]  # type: ignore
    + [(ForumPostList, example_forum_post_list_result["forumPostList"])]  # type: ignore
    + [(RealEstate, example_real_estate_result["realEstate"])]  # type: ignore
    + [(ReviewList, example_review_list_result["reviewList"])]  # type: ignore
    + [
        (Vehicle, example_vehicle_result["vehicle"])  # type: ignore
    ],  # type: ignore
)  # type: ignore
@pytest.mark.parametrize("unexpected_attrs", [{}, {"unexpected_attribute": "Should not fail"}])  # type: ignore
def test_item(cls, data, unexpected_attrs):
    assert cls.from_dict(None) is None
    item = cls.from_dict({**data, **unexpected_attrs})
    assert isinstance(item, cls)
    assert attr.asdict(item) == data
    assert item._unknown_fields_dict == unexpected_attrs
    assert_type_compliance(item)

    with temp_seed(7):
        for _ in range(10):
            data_with_holes = crazy_monkey_nullify(data)
            item = cls.from_dict(data_with_holes)
            assert attr.asdict(item) == data_with_holes

    # AttributeError: 'cls' object has no attribute 'foo'
    with pytest.raises(AttributeError):
        item.foo = "bar"

    # TypeError: __init__() got an unexpected argument 'foo'
    with pytest.raises(TypeError):
        cls(**data, foo="bar")


def test_from_list():
    @attr.s(auto_attribs=True, slots=True)
    class Number(Item):
        value: int

    actual = Number.from_list([None, dict(value=1), None, dict(value=2)])
    expected = [None, Number(1), None, Number(2)]
    assert actual == expected

    assert Number.from_list(None) == []
    assert Number.from_list([]) == []


def assert_all_isinstance(lst, cls):
    assert all(isinstance(el, cls) for el in lst)


def assert_pagination_types(item):
    assert isinstance(item.paginationNext, PaginationLink)
    assert isinstance(item.paginationPrevious, PaginationLink)


def test_article_attr_types():
    item = Article.from_dict(example_article_result["article"])
    assert isinstance(item, Article)
    assert_all_isinstance(item.breadcrumbs, Breadcrumb)


def test_article_list_attr_types():
    item = ArticleList.from_dict(example_article_list_result["articleList"])
    assert isinstance(item, ArticleList)
    assert_pagination_types(item)
    assert_all_isinstance(item.articles, ArticleFromList)


def test_product_attr_types():
    item = Product.from_dict(example_product_result["product"])
    assert isinstance(item, Product)
    assert_all_isinstance(item.offers, Offer)
    assert_all_isinstance(item.gtin, GTIN)
    assert_all_isinstance(item.breadcrumbs, Breadcrumb)
    assert_all_isinstance(item.additionalProperty, AdditionalProperty)
    assert isinstance(item.aggregateRating, ProductRating)


def test_product_list_attr_types():
    item = ProductList.from_dict(example_product_list_result["productList"])
    assert isinstance(item, ProductList)
    assert_pagination_types(item)
    assert_all_isinstance(item.products, ProductFromList)
    assert_all_isinstance(item.breadcrumbs, Breadcrumb)

    product = item.products[0]
    assert isinstance(product.aggregateRating, ProductRating)
    assert_all_isinstance(product.offers, Offer)


def test_job_posting_attr_types():
    item = JobPosting.from_dict(example_job_posting_result["jobPosting"])
    assert isinstance(item, JobPosting)
    assert isinstance(item.baseSalary, Salary)
    assert isinstance(item.hiringOrganization, Organization)
    assert isinstance(item.jobLocation, Location)


def test_comments_attr_types():
    item = CommentList.from_dict(example_comments_result["comments"])
    assert isinstance(item, CommentList)
    assert_all_isinstance(item.comments, Comment)


def test_forum_posts_attr_types():
    item = ForumPostList.from_dict(example_forum_post_list_result["forumPostList"])
    assert isinstance(item, ForumPostList)
    assert_all_isinstance(item.posts, ForumPost)
    assert isinstance(item.topic, Topic)


def test_real_estate_attr_types():
    item = RealEstate.from_dict(example_real_estate_result["realEstate"])
    assert isinstance(item, RealEstate)
    assert_all_isinstance(item.breadcrumbs, Breadcrumb)
    assert_all_isinstance(item.additionalProperty, AdditionalProperty)
    assert isinstance(item.address, Address)
    assert isinstance(item.area, Area)
    assert_all_isinstance(item.tradeActions, TradeAction)


def test_reviews_attr_types():
    item = ReviewList.from_dict(example_review_list_result["reviewList"])
    assert isinstance(item, ReviewList)
    assert_pagination_types(item)
    assert_all_isinstance(item.reviews, Review)

    review = item.reviews[0]
    assert isinstance(review.reviewRating, ReviewRating)


def test_vehicle_attr_types():
    item = Vehicle.from_dict(example_vehicle_result["vehicle"])
    assert isinstance(item, Vehicle)
    assert_all_isinstance(item.offers, Offer)
    assert_all_isinstance(item.breadcrumbs, Breadcrumb)
    assert_all_isinstance(item.additionalProperty, AdditionalProperty)
    assert_all_isinstance(item.fuelEfficiency, FuelEfficiency)
    assert isinstance(item.aggregateRating, VehicleRating)
    assert isinstance(item.mileageFromOdometer, MileageFromOdometer)
    assert isinstance(item.vehicleEngine, VehicleEngine)
    assert isinstance(item.availableAtOrFrom, AvailableAtOrFrom)
