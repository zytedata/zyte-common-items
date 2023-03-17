from zyte_common_items import (
    Address,
    AggregateRating,
    Amenity,
    Breadcrumb,
    BusinessPlaceMetadata,
    Link,
    Metadata,
    NamedLink,
    OpeningHoursItem,
    ParentPlace,
    StarRating,
)


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
    assert metadata.dateDownloaded is None
    assert metadata.probability is None


def test_named_link_optional_fields():
    NamedLink(name="foo")
    NamedLink(url="https://example.com")


def test_business_place_metadata_default_values():
    metadata = BusinessPlaceMetadata()
    assert metadata.dateDownloaded is None
    assert metadata.probability is None
    assert metadata.searchText is None


def test_address():
    Address(addressRaw="2440 Hoonani Rd, Koloa, HI 96756, US")
    Address(streetAddress="2440 Hoonani Rd, Koloa, HI 96756")
    Address(addressCity="Koloa")
    Address(addressLocality="Poipu")
    Address(addressRegion="Kauaʻi County")
    Address(addressCountry="US")
    Address(postalCode="96756")
    Address(postalCodeAux="HI")
    Address(latitude=21.8768183)
    Address(longitude=-159.3620652)


def test_amenity():
    Amenity(name="WiFi", value=True)
    Amenity(name="WiFi", value=False)


def test_star_rating():
    StarRating(raw="4-star hotel")
    StarRating(ratingValue=4)


def test_parent_place():
    ParentPlace(name="Gateway Plaza", placeId="ChIJCVDfcEKuEmsR7_zYc0_GBtQ")


def test_opening_hours():
    OpeningHoursItem(dayOfWeek="Sunday", opens="9:00", closes="12:00")
