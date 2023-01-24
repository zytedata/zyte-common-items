from web_poet import Unset

from zyte_common_items import AggregateRating, Breadcrumb, Link, Metadata


def test_aggregated_rating_optional_fields():
    AggregateRating(bestRating=5.0)
    AggregateRating(ratingValue=2.5)
    AggregateRating(reviewCount=123)


def test_breadcrumb_optional_fields():
    Breadcrumb(name="foo")
    Breadcrumb(url="https://example.com")


def test_link_optional_fields():
    Link(text="foo")
    Link(url="https://example.com")


def test_metadata_default_values():
    metadata = Metadata()
    assert metadata.dateDownloaded is Unset
    assert metadata.probability is Unset
