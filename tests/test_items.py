from copy import copy

import pytest

import zyte_common_items
from zyte_common_items import (
    AdditionalProperty,
    Address,
    AggregateRating,
    Amenity,
    Article,
    ArticleFromList,
    ArticleList,
    ArticleListMetadata,
    ArticleMetadata,
    ArticleNavigation,
    ArticleNavigationMetadata,
    Audio,
    Author,
    BaseSalary,
    Brand,
    Breadcrumb,
    BusinessPlace,
    BusinessPlaceMetadata,
    Gtin,
    Header,
    HiringOrganization,
    Image,
    JobLocation,
    JobPosting,
    JobPostingMetadata,
    Link,
    Metadata,
    NamedLink,
    OpeningHoursItem,
    ParentPlace,
    ProbabilityMetadata,
    ProbabilityRequest,
    Product,
    ProductFromList,
    ProductList,
    ProductListMetadata,
    ProductMetadata,
    ProductNavigation,
    ProductNavigationMetadata,
    ProductVariant,
    Reactions,
    RealEstate,
    RealEstateArea,
    RealEstateMetadata,
    Request,
    SocialMediaPost,
    SocialMediaPostAuthor,
    SocialMediaPostMetadata,
    StarRating,
    Url,
    Video,
)

_ARTICLE_FROM_LIST_ALL_KWARGS: dict = {
    "articleBody": "We held the 2022 Web Data Extraction Summit three weeks ago. I wanted to extend a huge thank you to everyone who came, especially our guest speakers, who shared some great insights throughout the day.",
    "authors": [
        Author(
            name="Honorable Zytan",
            nameRaw="Honorable Zytan",
        ),
    ],
    "datePublished": "2022-10-25T00:00:00Z",
    "datePublishedRaw": "October 25, 2022",
    "headline": "Reflecting on the 2022 Web Data Extraction Summit | Zyte",
    "images": [
        Image(
            "https://www.zyte.com/wp-content/uploads/2021/10/Extract-Summit-2021_Blog-Summary_Header-85.png"
        ),
    ],
    "inLanguage": "en",
    "mainImage": Image(
        "https://www.zyte.com/wp-content/uploads/2021/10/Extract-Summit-2021_Blog-Summary_Header-85.png"
    ),
    "metadata": ProbabilityMetadata(
        probability=0.8437236322711676,
    ),
    "url": "https://www.zyte.com/blog/reflecting-on-the-2022-web-data-extraction-summit-zyte/",
}
_ARTICLE_MIN_KWARGS: dict = {
    "url": "https://www.zyte.com/blog/product-data-extraction-automatic",
}
_ARTICLE_ALL_KWARGS: dict = {
    **_ARTICLE_MIN_KWARGS,
    "headline": "Guarantee the best results for product data extraction",
    "datePublished": "2022-08-26T20:56:16Z",
    "datePublishedRaw": "August 26, 2022",
    "dateModified": "2022-08-27T21:48:55Z",
    "dateModifiedRaw": "August 25, 2022",
    "authors": [Author()],
    "breadcrumbs": [
        Breadcrumb(
            name="Homepage",
            url="https://www.zyte.com",
        ),
        Breadcrumb(
            name="Blog",
            url="https://www.zyte.com/blog/",
        ),
        Breadcrumb(
            name="Guarantee the best results for product data extraction",
        ),
    ],
    "inLanguage": "en",
    "mainImage": Image(
        "https://www.zyte.com/wp-content/uploads/2022/08/product-data-extraction-zyte.png"
    ),
    "images": [
        Image(
            "https://www.zyte.com/wp-content/uploads/2022/08/product-data-extraction-zyte.png"
        ),
        Image(
            "https://www.zyte.com/wp-content/uploads/2021/06/Webinar_Product-Data-Quality-01-1024x536.png"
        ),
        Image(
            "https://www.zyte.com/wp-content/uploads/2022/08/product-data-extraction-automatic.png"
        ),
    ],
    "description": "Product Data Extraction helps understand how consumers use a specific product, foresee improvements and adjustments that ultimately increase sales and demand.",
    "articleBody": "When businesses operate in a competitive environment it is imperative to know what their competitors are charging in real-time and this can be hard to keep track of. For any data driven organization, implementing a solution that automatically extracts product data from websites in real-time and at scale, is indispensable to stay ahead of the competition. Setting an automatic process for product data extraction can be a powerful tool for data driven businesses of all sizes. You can extract specific products information including offers, price, currency, and availability. Provided that the data extraction process is able to identify the key attributes of a product, it can then use this information to create reports with insights into the behavior of a particular product. For this to work, it is key to have the right procedures in place that guarantee the best results for your automation product extraction projects. By doing so, your organization can better understand how consumers are using a specific product, foresee any necessary adjustments to improve the user experience and as a result, increase sales and demand. In this article, we'll explain not just everything you need to know to get started, but also show you how to guarantee the best results when working with product data extraction.\n\nWhat is automatic product extraction?\n\n...",
    "articleBodyHtml": '<article>\n<p>When businesses operate in a competitive environment it is imperative to know what their competitors are charging in real-time and this can be hard to keep track of. For any data driven organization, implementing a solution that automatically extracts product data from websites in real-time and at scale, is indispensable to stay ahead of the competition.</p> <p>Setting an automatic process for <a href="https://docs.zyte.com/automatic-extraction/product.html">product data extraction</a> can be a powerful tool for data driven businesses of all sizes. You can extract specific products information including offers, price, currency, and availability. Provided that the data extraction process is able to <a href="/blog/automatic-extraction-data-extractor-review/">identify the key attributes of a product</a>, it can then use this information to create reports with insights into the behavior of a particular product.</p>\n<p>For this to work, it is key to have the right procedures in place that guarantee the best results for your automation product extraction projects. By doing so, your organization can better understand how consumers are using a specific product, foresee any necessary adjustments to improve the user experience and as a result, increase sales and demand.</p>\n<p>In this article, we\'ll explain not just everything you need to know to get started, but also show you how to guarantee the best results when working with product data extraction.</p>\n<h2><strong>What is automatic product extraction?</strong></h2>\n...\n</article>',
    "videos": [
        Video(
            "https://player.vimeo.com/video/90592864?title=0&byline=0&portrait=0&color=8dc7dc"
        ),
    ],
    "audios": [
        Audio("https://example.com/audiofile.mp3"),
    ],
    "canonicalUrl": "https://www.zyte.com/blog/product-data-extraction-automatic/",
    "url": "https://www.zyte.com/blog/product-data-extraction-automatic",
    "metadata": ArticleMetadata(
        dateDownloaded="2022-12-31T13:01:54Z",
        probability=1.0,
    ),
}
_ARTICLE_LIST_MIN_KWARGS: dict = {
    "url": "https://www.zyte.com/blog/extract-summit-blog/",
}
_ARTICLE_LIST_ALL_KWARGS: dict = {
    **_ARTICLE_LIST_MIN_KWARGS,
    "canonicalUrl": "https://www.zyte.com/blog/extract-summit-blog/",
    "articles": [
        ArticleFromList(
            url="https://www.zyte.com/blog/reflecting-on-the-2022-web-data-extraction-summit-zyte/",
        ),
    ],
    "breadcrumbs": [
        Breadcrumb(
            name="Homepage",
            url="https://www.zyte.com/",
        ),
        Breadcrumb(
            name="Blog",
            url="https://www.zyte.com/blog/",
        ),
        Breadcrumb(
            name="Extract Summit",
            url="https://www.zyte.com/blog/extract-summit-blog/",
        ),
    ],
    "metadata": ArticleListMetadata(
        dateDownloaded="2022-12-31T13:01:54Z",
    ),
}

_ARTICLE_NAVIGATION_MIN_KWARGS: dict = {"url": "https://example.com/real-estate/12345"}

_ARTICLE_NAVIGATION_ALL_KWARGS: dict = {
    **_ARTICLE_NAVIGATION_MIN_KWARGS,
    "categoryName": "Swiss Watches",
    "subCategories": [
        ProbabilityRequest(
            url="http://books.toscrape.com/catalogue/category/books/",
            method="POST",
            body="YmFzZTY0LWVuY29kZWQ=",
            headers=[Header(name="content-type", value="text/json")],
            name="Travel",
            metadata=ProbabilityMetadata(probability=0.99),
        ),
        ProbabilityRequest(
            url="http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
            name="Mystery",
            metadata=ProbabilityMetadata(probability=0.97),
        ),
    ],
    "items": [
        ProbabilityRequest(
            url="http://books.toscrape.com/catalogue/in-her-wake_980",
            method="POST",
            body="YmFzZTY0LWVuY29kZWQ=",
            headers=[Header(name="content-type", value="text/json")],
            name="In Her Wake",
            metadata=ProbabilityMetadata(probability=0.99),
        ),
        ProbabilityRequest(
            url="http://books.toscrape.com/catalogue/how-music-works_979/index.html",
            name="How Music Works",
            metadata=ProbabilityMetadata(probability=0.98),
        ),
    ],
    "nextPage": Request(
        url="http://books.toscrape.com/catalogue/page-3.html",
        name="Next page",
        method="POST",
        body="Im9rIg==",
        headers=[Header(name="content-type", value="text/json")],
    ),
    "pageNumber": 5,
    "metadata": ArticleNavigationMetadata(dateDownloaded="2022-12-31T13:01:54Z"),
}

_BUSINESS_PLACE_MIN_KWARGS: dict = {}

_BUSINESS_PLACE_ALL_KWARGS: dict = {
    **_BUSINESS_PLACE_MIN_KWARGS,
    "url": "https://place-listing.example/place/12345",
    "placeId": "ChIJ02PI3bsaB3wRh-IwsWeJ0nI",
    "name": "Sheraton Kauai Resort",
    "actions": [
        NamedLink(name="Reserve Table", url="https://example.com"),
        NamedLink(name="Book Room", url="https://example.com"),
    ],
    "additionalProperties": [
        AdditionalProperty(name="Popular for", value="Lunch,Dinner")
    ],
    "address": Address(addressRaw="2440 Hoonani Rd, Koloa, HI 96756, US"),
    "reservationAction": NamedLink(name="Reserve a table", url="https://example.com"),
    "categories": ["Hotel", "Wedding venue"],
    "description": "Oceanfront resort offering Hawaiian dining, plus 2 outdoor pools & a fitness center.",
    "features": ["Pool", "Free Parking"],
    "map": "https://map.example/place/12345",
    "images": [
        Image("http://example.com/image1.png"),
    ],
    "amenityFeatures": [Amenity(name="Free WiFi", value=True)],
    "aggregateRating": AggregateRating(
        bestRating=5.0,
        ratingValue=2.5,
        reviewCount=123,
    ),
    "starRating": StarRating(raw="4-star Hotel"),
    "containedInPlace": ParentPlace(name="Gateway Plaza", placeId="ChIJCVDfcE_GBtq"),
    "openingHours": [OpeningHoursItem(dayOfWeek="Monday", opens="10:00")],
    "reviewSites": [NamedLink(name="Expedia", url="https://example.com")],
    "telephone": "(808) 742-1661",
    "priceRange": "zz",
    "timezone": "Pacific/Honolulu",
    "isVerified": True,
    "website": "https://example.com",
    "tags": ["Dogs", "Family"],
    "metadata": BusinessPlaceMetadata(
        searchText="hotel", dateDownloaded="2022-12-31T13L01L54Z", probability=0.95
    ),
}

_PRODUCT_FROM_LIST_ALL_KWARGS: dict = {
    "currency": "USD",
    "currencyRaw": "$",
    "mainImage": Image("http://example.com/image1.png"),
    "metadata": ProbabilityMetadata(
        probability=1.0,
    ),
    "name": "White two-door refrigerator",
    "price": "9999.99",
    "productId": "A123DK9823",
    "regularPrice": "11999.99",
    "url": "https://example.com/?product=product22",
}
_PRODUCT_VARIANT_ALL_KWARGS: dict = {
    "additionalProperties": [AdditionalProperty("foo", "bar")],
    "availability": "InStock",
    "canonicalUrl": "https://example.com/product22",
    "color": "white",
    "currency": "USD",
    "currencyRaw": "$",
    "gtin": [Gtin("foo", "bar")],
    "images": [
        Image("http://example.com/image1.png"),
    ],
    "mainImage": Image("http://example.com/image1.png"),
    "mpn": "HSC0424PP",
    "name": "White two-door refrigerator",
    "price": "9999.99",
    "productId": "A123DK9823",
    "regularPrice": "11999.99",
    "size": "XL",
    "sku": "A123DK9823",
    "style": "polka dots",
    "url": "https://example.com/?product=product22",
}
_PRODUCT_MIN_KWARGS: dict = {
    "url": "https://example.com/?product=product22",
}
_PRODUCT_ALL_KWARGS: dict = {
    **_PRODUCT_MIN_KWARGS,
    **_PRODUCT_VARIANT_ALL_KWARGS,
    "aggregateRating": AggregateRating(
        bestRating=5.0,
        ratingValue=2.5,
        reviewCount=123,
    ),
    "brand": Brand("Ka-pow"),
    "breadcrumbs": [
        Breadcrumb(name="Level 1", url="http://example.com/level1"),
        Breadcrumb(name="Level 2", url="http://example.com/level1/level2"),
    ],
    "description": (
        "Full freshness all over the fridge\n5 Conversion Modes on demand\nSuper Cooling Plus™"
    ),
    "descriptionHtml": (
        "<article><p>Full freshness all over the fridge</p>"
        "<p>5 Conversion Modes on demand</p>"
        "<p>Super Cooling Plus&trade;</p></article>"
    ),
    "features": ["Easily store fragile products.", "Bluetooth connectivity."],
    "metadata": ProductMetadata(
        dateDownloaded="2022-12-31T13:01:54Z",
        probability=1.0,
    ),
    "variants": [ProductVariant()],
}
_PRODUCT_LIST_MIN_KWARGS: dict = {
    "url": "https://example.com/swiss-watches?sort=new-first",
}
_PRODUCT_LIST_ALL_KWARGS: dict = {
    **_PRODUCT_LIST_MIN_KWARGS,
    "breadcrumbs": [
        Breadcrumb(name="Level 1", url="http://example.com/level1"),
        Breadcrumb(name="Level 2", url="http://example.com/level1/level2"),
    ],
    "canonicalUrl": "https://example.com/swiss-watches",
    "categoryName": "Swiss Watches",
    "metadata": ProductListMetadata(
        dateDownloaded="2022-12-31T13:01:54Z",
    ),
    "pageNumber": 1,
    "paginationNext": Link(
        text="foo",
        url="https://example.com/swiss-watches?sort=new-first&page=2",
    ),
    "products": [ProductFromList()],
}

_REAL_ESTATE_MIN_KWARGS: dict = {
    "url": "https://example.com/real-estate/12345",
}

_REAL_ESTATE_ALL_KWARGS: dict = {
    **_REAL_ESTATE_MIN_KWARGS,
    "breadcrumbs": [
        Breadcrumb(name="Level 1", url="http://example.com/level1"),
        Breadcrumb(name="Level 2", url="http://example.com/level1/level2"),
    ],
    "realEstateId": "12345",
    "name": "Beautiful 2 bedroom apartment",
    "datePublished": "2022-12-31T13:01:54Z",
    "datePublishedRaw": "2022-12-31",
    "description": "Beautiful 2 bedroom apartment in the heart of the city",
    "mainImage": Image("http://example.com/image1.png"),
    "images": [
        Image("http://example.com/image1.png"),
        Image("http://example.com/image2.png"),
    ],
    "address": Address(addressRaw="2440 Hoonani Rd, Koloa, HI 96756, US"),
    "area": RealEstateArea(
        value=100,
        unitCode="SQMT",
        areaType="LOT",
        raw="100 sqm",
    ),
    "numberOfBathroomsTotal": 2,
    "numberOfFullBathrooms": 1,
    "numberOfPartialBathrooms": 1,
    "numberOfBedrooms": 2,
    "numberOfRooms": 2,
    "tradeType": "RENT",
    "price": "456456",
    "rentalPeriod": "MONTH",
    "currency": "USD",
    "currencyRaw": "$",
    "additionalProperties": [
        AdditionalProperty(name="Parking", value="Garage"),
        AdditionalProperty(name="Pets", value="Allowed"),
    ],
    "propertyType": "flat",
    "yearBuilt": 1997,
    "virtualTourUrl": "https://example.com",
    "metadata": RealEstateMetadata(
        dateDownloaded="2022-12-31T13:01:54Z",
        probability=1.0,
    ),
}

_PRODUCT_NAVIGATION_MIN_KWARGS: dict = {"url": "https://example.com/real-estate/12345"}

_PRODUCT_NAVIGATION_ALL_KWARGS: dict = {
    **_PRODUCT_NAVIGATION_MIN_KWARGS,
    "categoryName": "Swiss Watches",
    "subCategories": [
        ProbabilityRequest(
            url="http://books.toscrape.com/catalogue/category/books/",
            method="POST",
            body="YmFzZTY0LWVuY29kZWQ=",
            headers=[Header(name="content-type", value="text/json")],
            name="Travel",
            metadata=ProbabilityMetadata(probability=0.99),
        ),
        ProbabilityRequest(
            url="http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
            name="Mystery",
            metadata=ProbabilityMetadata(probability=0.97),
        ),
    ],
    "items": [
        ProbabilityRequest(
            url="http://books.toscrape.com/catalogue/in-her-wake_980",
            method="POST",
            body="YmFzZTY0LWVuY29kZWQ=",
            headers=[Header(name="content-type", value="text/json")],
            name="In Her Wake",
            metadata=ProbabilityMetadata(probability=0.99),
        ),
        ProbabilityRequest(
            url="http://books.toscrape.com/catalogue/how-music-works_979/index.html",
            name="How Music Works",
            metadata=ProbabilityMetadata(probability=0.98),
        ),
    ],
    "nextPage": Request(
        url="http://books.toscrape.com/catalogue/page-3.html",
        name="Next page",
        method="POST",
        body="Im9rIg==",
        headers=[Header(name="content-type", value="text/json")],
    ),
    "pageNumber": 5,
    "metadata": ProductNavigationMetadata(dateDownloaded="2022-12-31T13:01:54Z"),
}

_JOB_POSTING_MIN_KWARGS: dict = {
    "url": "https://example.com/viewjob/12345",
}

_JOB_POSTING_ALL_KWARGS: dict = {
    **_JOB_POSTING_MIN_KWARGS,
    "jobPostingId": "12345",
    "datePublished": "2019-06-19T00:00:00-05:00",
    "datePublishedRaw": "19 June 2019",
    "dateModified": "2019-06-21T00:00:00-05:00",
    "dateModifiedRaw": "21 June 2019",
    "validThrough": "2019-07-19T00:00:00-05:00",
    "validThroughRaw": "19 July 2019",
    "jobTitle": "Software Engineer",
    "headline": "Are you our next Software Engineer?",
    "jobLocation": JobLocation(raw="New York, NY"),
    "description": "We are looking for a Software Engineer to join our team."
    "- 35 days holiday"
    "- 15% bonus"
    "- flexible working arrangements",
    "descriptionHtml": "<p>We are looking for a Software Engineer to join our team.</p>"
    "<ul>"
    "<li>35 days holiday</li>"
    "<li>15% bonus</li>"
    "<li>flexible working arrangements</li>"
    "</ul>",
    "employmentType": "Full-time",
    "baseSalary": BaseSalary(
        raw="$53,000-$55,000 a year",
        valueMin="53000",
        valueMax="55000",
        rateType="yearly",
        currencyRaw="$",
        currency="USD",
    ),
    "requirements": [
        "Experience in managing diverse teams",
        "Great sense of responsibility",
        "5+ years of proven experience in sales",
        "Ability to travel",
    ],
    "hiringOrganization": HiringOrganization(
        name="ACME Corp.", nameRaw="ACME Corp., US", id="54321"
    ),
    "jobStartDate": "2019-08-01T00:00:00-05:00",
    "jobStartDateRaw": "01 August 2019",
    "remoteStatus": "Remote",
    "metadata": JobPostingMetadata(
        dateDownloaded="2022-12-31T13:01:54Z",
        probability=0.95,
        searchText="Software Engineer",
    ),
}

_SOCIAL_MEDIA_POST_MIN_KWARGS: dict = {
    "url": "https://example.com/viewjob/12345",
}

_SOCIAL_MEDIA_POST_ALL_KWARGS: dict = {
    **_SOCIAL_MEDIA_POST_MIN_KWARGS,
    "postId": "1569750785201676290",
    "reactions": Reactions(reposts=1, likes=1, dislikes=1),
    "text": (
        "Join us for the @usertag_1 2022 Coding Contest and stand a chance to win bragging rights plus awesome "
        "prizes! Register for free - https://hubs.li/Q01mcRlk0 #coding #webdata #dataextraction #webscraping "
        "#scrapy #python"
    ),
    "datePublished": "2023-10-04T00:00:00Z",
    "hashtags": [
        "coding",
        "webdata",
        "dataextraction",
        "webscraping",
        "scrapy",
        "python",
    ],
    "mediaUrls": [
        {
            "url": Url(url="https://example.com/image1.png"),
        },
        {
            "url": Url(url="https://video.twimg.com/tweet_video/FcjgBTkX0AAXPUh.mp4"),
        },
    ],
    "author": SocialMediaPostAuthor(
        numberOfFollowers=5,
        numberOfFollowing=5,
        dateAccountCreated="2022-10-04",
        location="San Francisco, CA",
        isVerified=True,
    ),
    "metadata": SocialMediaPostMetadata(
        dateDownloaded="2022-12-31T13:01:54Z",
        probability=0.95,
        searchText="Extract Summit",
    ),
}


def test_article_all_fields():
    article = Article(**_ARTICLE_ALL_KWARGS)
    for field in list(_ARTICLE_ALL_KWARGS):
        assert getattr(article, field) == _ARTICLE_ALL_KWARGS[field]


def test_article_min_fields():
    article = Article(**_ARTICLE_MIN_KWARGS)
    for field in list(_ARTICLE_ALL_KWARGS):
        if field in _ARTICLE_MIN_KWARGS:
            continue
        assert getattr(article, field) is None


def test_article_missing_fields():
    for required_field in list(_ARTICLE_MIN_KWARGS):
        incomplete_kwargs: dict = copy(_ARTICLE_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            Article(**incomplete_kwargs)


def test_article_list_all_fields():
    article_list = ArticleList(**_ARTICLE_LIST_ALL_KWARGS)
    for field in list(_ARTICLE_LIST_ALL_KWARGS):
        assert getattr(article_list, field) == _ARTICLE_LIST_ALL_KWARGS[field]


def test_article_list_min_fields():
    article_list = ArticleList(**_ARTICLE_LIST_MIN_KWARGS)
    for field in list(_ARTICLE_LIST_MIN_KWARGS):
        if field in _ARTICLE_LIST_MIN_KWARGS:
            continue
        assert getattr(article_list, field) is None


def test_article_list_missing_fields():
    for required_field in list(_ARTICLE_LIST_MIN_KWARGS):
        incomplete_kwargs: dict = copy(_ARTICLE_LIST_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            ArticleList(**incomplete_kwargs)


def test_article_from_list_all_fields():
    article_from_list = ArticleFromList(**_ARTICLE_FROM_LIST_ALL_KWARGS)
    for field in list(_ARTICLE_FROM_LIST_ALL_KWARGS):
        assert getattr(article_from_list, field) == _ARTICLE_FROM_LIST_ALL_KWARGS[field]


def test_article_from_list_min_fields():
    article_from_list = ArticleFromList()
    for field in list(_ARTICLE_FROM_LIST_ALL_KWARGS):
        assert getattr(article_from_list, field) is None


def test_article_navigation_all_fields():
    article_navigation = ArticleNavigation(**_ARTICLE_NAVIGATION_ALL_KWARGS)
    for field in list(_ARTICLE_NAVIGATION_ALL_KWARGS):
        assert (
            getattr(article_navigation, field) == _ARTICLE_NAVIGATION_ALL_KWARGS[field]
        )


def test_article_navigation_min_fields():
    article_navigation = ArticleNavigation(**_ARTICLE_NAVIGATION_MIN_KWARGS)
    for field in list(_ARTICLE_NAVIGATION_ALL_KWARGS):
        if field in _ARTICLE_NAVIGATION_MIN_KWARGS:
            continue
        assert getattr(article_navigation, field) is None


def test_article_navigation_missing_fields():
    for required_field in list(_ARTICLE_NAVIGATION_MIN_KWARGS):
        incomplete_kwargs: dict = copy(_ARTICLE_NAVIGATION_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            ArticleNavigation(**incomplete_kwargs)


def test_product_all_fields():
    product = Product(**_PRODUCT_ALL_KWARGS)
    for field in list(_PRODUCT_ALL_KWARGS):
        assert getattr(product, field) == _PRODUCT_ALL_KWARGS[field]


def test_product_min_fields():
    product = Product(**_PRODUCT_MIN_KWARGS)
    for field in list(_PRODUCT_ALL_KWARGS):
        if field in _PRODUCT_MIN_KWARGS:
            continue
        assert getattr(product, field) is None


def test_product_missing_fields():
    for required_field in list(_PRODUCT_MIN_KWARGS):
        incomplete_kwargs: dict = copy(_PRODUCT_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            Product(**incomplete_kwargs)


def test_product_list_all_fields():
    product_list = ProductList(**_PRODUCT_LIST_ALL_KWARGS)
    for field in list(_PRODUCT_LIST_ALL_KWARGS):
        assert getattr(product_list, field) == _PRODUCT_LIST_ALL_KWARGS[field]


def test_product_list_min_fields():
    product_list = ProductList(**_PRODUCT_LIST_MIN_KWARGS)
    for field in list(_PRODUCT_LIST_MIN_KWARGS):
        if field in _PRODUCT_LIST_MIN_KWARGS:
            continue
        assert getattr(product_list, field) is None


def test_product_list_missing_fields():
    for required_field in list(_PRODUCT_LIST_MIN_KWARGS):
        incomplete_kwargs: dict = copy(_PRODUCT_LIST_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            ProductList(**incomplete_kwargs)


def test_product_from_list_all_fields():
    product_from_list = ProductFromList(**_PRODUCT_FROM_LIST_ALL_KWARGS)
    for field in list(_PRODUCT_FROM_LIST_ALL_KWARGS):
        assert getattr(product_from_list, field) == _PRODUCT_FROM_LIST_ALL_KWARGS[field]


def test_product_from_list_min_fields():
    product_from_list = ProductFromList()
    for field in list(_PRODUCT_FROM_LIST_ALL_KWARGS):
        assert getattr(product_from_list, field) is None


def test_product_variant_all_fields():
    product_variant = ProductVariant(**_PRODUCT_VARIANT_ALL_KWARGS)
    for field in list(_PRODUCT_VARIANT_ALL_KWARGS):
        assert getattr(product_variant, field) == _PRODUCT_VARIANT_ALL_KWARGS[field]


def test_product_variant_min_fields():
    product_variant = ProductVariant()
    for field in list(_PRODUCT_VARIANT_ALL_KWARGS):
        assert getattr(product_variant, field) is None


def test_business_place_all_fields():
    place = BusinessPlace(**_BUSINESS_PLACE_ALL_KWARGS)
    for field in list(_BUSINESS_PLACE_ALL_KWARGS):
        assert getattr(place, field) == _BUSINESS_PLACE_ALL_KWARGS[field]


def test_business_place_min_fields():
    place = BusinessPlace(**_BUSINESS_PLACE_MIN_KWARGS)
    for field in list(_BUSINESS_PLACE_ALL_KWARGS):
        if field in _BUSINESS_PLACE_MIN_KWARGS:
            continue
        assert getattr(place, field) is None


def test_business_place_missing_fields():
    for required_field in list(_BUSINESS_PLACE_MIN_KWARGS):
        incomplete_kwargs: dict = copy(_BUSINESS_PLACE_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            BusinessPlace(**incomplete_kwargs)


def test_real_estate_all_fields():
    real_estate = RealEstate(**_REAL_ESTATE_ALL_KWARGS)
    for field in list(_REAL_ESTATE_ALL_KWARGS):
        assert getattr(real_estate, field) == _REAL_ESTATE_ALL_KWARGS[field]


def test_real_estate_min_fields():
    real_estate = RealEstate(**_REAL_ESTATE_MIN_KWARGS)
    for field in list(_REAL_ESTATE_ALL_KWARGS):
        if field in _REAL_ESTATE_MIN_KWARGS:
            continue
        assert getattr(real_estate, field) is None


def test_real_estate_missing_fields():
    for required_field in list(_REAL_ESTATE_MIN_KWARGS):
        incomplete_kwargs: dict = copy(_REAL_ESTATE_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            RealEstate(**incomplete_kwargs)


def test_product_navigation_all_fields():
    product_navigation = ProductNavigation(**_PRODUCT_NAVIGATION_ALL_KWARGS)
    for field in list(_PRODUCT_NAVIGATION_ALL_KWARGS):
        assert (
            getattr(product_navigation, field) == _PRODUCT_NAVIGATION_ALL_KWARGS[field]
        )


def test_product_navigation_min_fields():
    product_navigation = ProductNavigation(**_PRODUCT_NAVIGATION_MIN_KWARGS)
    for field in list(_PRODUCT_NAVIGATION_ALL_KWARGS):
        if field in _PRODUCT_NAVIGATION_MIN_KWARGS:
            continue
        assert getattr(product_navigation, field) is None


def test_product_navigation_missing_fields():
    for required_field in list(_PRODUCT_NAVIGATION_MIN_KWARGS):
        incomplete_kwargs: dict = copy(_PRODUCT_NAVIGATION_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            ProductNavigation(**incomplete_kwargs)


def test_metadata():
    """Test metadata expectations for items.

    For every item:

    -   There must be a matching metadata class.

    -   The metadata attribute must be of that metadata class.

    -   If the generic Metadata object is assigned as input, it gets converted
        into an object of the right, more specific metadata class.
    """
    item_names = {
        obj_name[:-4]
        for obj_name in zyte_common_items.__dict__
        if (
            not (obj_name.startswith("Base") or obj_name.startswith("Auto"))
            and obj_name.endswith("Page")
            and obj_name != "Page"
        )
    }
    for item_name in item_names:
        cls = zyte_common_items.__dict__[item_name]
        metadata_cls = zyte_common_items.__dict__[f"{item_name}Metadata"]

        obj1 = cls.from_dict(
            {"url": "https://example.com", "metadata": {"dateDownloaded": "foo"}}
        )
        assert type(obj1.metadata) == metadata_cls
        assert obj1.metadata.dateDownloaded == "foo"

        obj2 = cls(url="https://example.com", metadata=Metadata(dateDownloaded="foo"))
        assert type(obj2.metadata) == metadata_cls
        assert obj2.metadata.dateDownloaded == "foo"
        obj2.metadata = Metadata(dateDownloaded="foo")
        assert type(obj2.metadata) == metadata_cls
        assert obj2.metadata.dateDownloaded == "foo"


def test_request():
    """Test request class conversion on assignment"""

    product_navigation = ProductNavigation(**_PRODUCT_NAVIGATION_MIN_KWARGS)
    product_navigation.subCategories = [
        Request(  # type: ignore[list-item]
            url="http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
            name="Mystery",
        ),
    ]
    assert product_navigation.subCategories[0] == ProbabilityRequest(
        url="http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        name="Mystery",
        metadata=ProbabilityMetadata(probability=1.0),
    )


def test_job_posting_all_fields():
    job_posting = JobPosting(**_JOB_POSTING_ALL_KWARGS)
    for field in list(_JOB_POSTING_ALL_KWARGS):
        assert getattr(job_posting, field) == _JOB_POSTING_ALL_KWARGS[field]


def test_job_posting_min_fields():
    job_posting = JobPosting(**_JOB_POSTING_MIN_KWARGS)
    for field in list(_JOB_POSTING_ALL_KWARGS):
        if field in _JOB_POSTING_MIN_KWARGS:
            continue
        assert getattr(job_posting, field) is None


def test_job_posting_missing_fields():
    for required_field in list(_JOB_POSTING_MIN_KWARGS):
        incomplete_kwargs: dict = copy(_JOB_POSTING_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            JobPosting(**incomplete_kwargs)


def test_social_media_post_all_fields():
    social_media_post = SocialMediaPost(**_SOCIAL_MEDIA_POST_ALL_KWARGS)
    for field in list(_SOCIAL_MEDIA_POST_ALL_KWARGS):
        assert getattr(social_media_post, field) == _SOCIAL_MEDIA_POST_ALL_KWARGS[field]


def test_social_media_post_min_fields():
    social_media_post = SocialMediaPost(**_SOCIAL_MEDIA_POST_MIN_KWARGS)
    for field in list(_SOCIAL_MEDIA_POST_ALL_KWARGS):
        if field in _SOCIAL_MEDIA_POST_MIN_KWARGS:
            continue
        assert getattr(social_media_post, field) is None


def test_social_media_post_missing_fields():
    for required_field in list(_SOCIAL_MEDIA_POST_MIN_KWARGS):
        incomplete_kwargs: dict = copy(_SOCIAL_MEDIA_POST_MIN_KWARGS)
        del incomplete_kwargs[required_field]
        with pytest.raises(TypeError):
            SocialMediaPost(**incomplete_kwargs)


@pytest.mark.parametrize(
    "cls,has_proba",
    (
        (Article, True),
        (ArticleFromList, True),
        (ArticleList, False),
        (ArticleNavigation, False),
        (BusinessPlace, True),
        (JobPosting, True),
        (Product, True),
        (ProductFromList, True),
        (ProductList, False),
        (ProductNavigation, False),
        (ProductVariant, False),
        (RealEstate, True),
    ),
)
def test_get_probability_request(cls, has_proba):
    data = {"url": "https://example.com"}

    item = cls.from_dict(data)
    assert item.get_probability() is None

    item = cls.from_dict({**data, "metadata": {"probability": 0.5}})
    if has_proba:
        assert item.get_probability() == 0.5
    else:
        assert item.get_probability() is None

    item = cls.from_dict({**data, "metadata": {"probability": 0.0}})
    if has_proba:
        assert item.get_probability() == 0.0
    else:
        assert item.get_probability() is None
