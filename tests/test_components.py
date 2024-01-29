from web_poet import RequestUrl

from zyte_common_items import (
    Address,
    AggregateRating,
    Amenity,
    BaseSalary,
    Breadcrumb,
    BusinessPlaceMetadata,
    Header,
    HiringOrganization,
    JobLocation,
    JobPostingMetadata,
    Link,
    Metadata,
    NamedLink,
    OpeningHoursItem,
    ParentPlace,
    ProbabilityMetadata,
    ProbabilityRequest,
    Reactions,
    RealEstateArea,
    Request,
    SocialMediaPostAuthor,
    SocialMediaPostMetadata,
    StarRating,
    Url,
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
    assert metadata.probability == 1.0


def test_named_link_optional_fields():
    NamedLink(name="foo")
    NamedLink(url="https://example.com")


def test_business_place_metadata_default_values():
    metadata = BusinessPlaceMetadata()
    assert metadata.dateDownloaded is None
    assert metadata.probability == 1.0
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


def test_real_estate_area():
    RealEstateArea(value=123.45, unitCode="SQMT", raw="123.45 square meters")
    RealEstateArea(
        value=123.45, unitCode="SQMT", raw="123.45 square meters", areaType="LOT"
    )


def test_headers():
    Header(name="Connection", value="keep-alive")
    Header(name="Content-Type", value="text/html; charset=utf-8")


def test_probability_request():
    ProbabilityRequest(url="https://example.com")
    headers = [
        Header(name="Content-Type", value="application/x-www-form-urlencoded"),
        Header(name="Host", value="foo.example"),
    ]
    request = ProbabilityRequest(
        name="Post Test",
        url="https://example.com/test",
        method="POST",
        body="ZmllbGQxPXZhbHVlMSZmaWVsZDI9dmFsdWUy",
        headers=headers,
        metadata=ProbabilityMetadata(probability=0.5),
    )
    assert request.get_probability() == 0.5

    request = ProbabilityRequest(
        name="Get with RequestURL object",
        url=RequestUrl("https://example.com/test"),
    )

    assert request.url == "https://example.com/test"
    assert request.get_probability() is None


def test_request():
    Request(url="https://example.com")
    headers = [
        Header(name="Content-Type", value="application/x-www-form-urlencoded"),
        Header(name="Host", value="foo.example"),
    ]
    Request(
        name="Post Test",
        url="https://example.com/test",
        method="POST",
        body="ZmllbGQxPXZhbHVlMSZmaWVsZDI9dmFsdWUy",
        headers=headers,
    )

    request = Request(
        name="Get with RequestURL object",
        url=RequestUrl("https://example.com/test"),
    )

    assert request.url == "https://example.com/test"


def test_job_location():
    JobLocation(raw="New York, NY")


def test_base_salary():
    BaseSalary(
        raw="$53,000-$55,000 a year",
        valueMin="53000",
        valueMax="55000",
        rateType="yearly",
        currencyRaw="$",
        currency="USD",
    )


def test_hiring_organization():
    HiringOrganization(name="Example Inc.", nameRaw="Example Inc. USA", id="12345")


def test_job_posting_metadata():
    JobPostingMetadata(
        dateDownloaded="2020-01-01", probability=0.5, searchText="Software Engineer"
    )


def test_reactions():
    Reactions(reposts=1, likes=2, dislikes=3)


def test_social_media_post_author():
    SocialMediaPostAuthor(
        numberOfFollowers=5,
        numberOfFollowing=5,
        dateAccountCreated="2020-01-01",
        location="New York, NY",
        isVerified=True,
    )


def test_social_media_post_metadata():
    SocialMediaPostMetadata(
        dateDownloaded="2020-01-01", probability=0.5, searchText="Extract Summit"
    )


def test_url():
    Url(url="https://example.com")
