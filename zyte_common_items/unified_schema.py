"""These are data containers which holds items conforming to the Unified Schema
as described in https://docs.zyte.com/unified-schema.html.

Since the schema of Zyte Data API is a subclass of Unified Schema,
we're using it as a baseclass. There are only a few changes to be made like:

    - new fields not existing in Zyte Data API
    - overriding fields which contains more subfields
"""

from typing import Any, List, Optional

import attr

import zyte_common_items.zyte_data_api as zda
from zyte_common_items import Item, common_fields
from zyte_common_items.util import export


@export
@attr.define(slots=True)
class Article(zda.Article):
    pass


@export
@attr.define(slots=True)
class RealEstate(zda.RealEstate):
    pass


@export
@attr.define(slots=True)
class RatingHistogram(Item):
    ratingOption: Optional[str] = None
    ratingCount: Optional[int] = None
    ratingPercentage: Optional[float] = None


@export
@attr.define(slots=True)
class Answer(Item):
    text: Optional[str] = None
    answerDate: Optional[str] = None
    answerDateRaw: Optional[str] = None
    author: Optional[common_fields.Author] = None


@export
@attr.define(slots=True)
class InteractionCounter(Item):
    interactionType: Optional[str] = None
    userInteractionCount: Optional[int] = None


@export
@attr.define(slots=True)
class Question(Item):
    text: Optional[str] = None
    questionDate: Optional[str] = None
    questionDateRaw: Optional[str] = None
    author: Optional[common_fields.Author] = None
    url: Optional[str] = None
    vote: Optional[int] = None
    numberOfAnswers: Optional[int] = None
    answers: List[Answer] = attr.factory(list)
    interactionCounter: List[InteractionCounter] = attr.factory(list)


@export
@attr.define(slots=True)
class QuantitativeValue(Item):
    maxValue: Optional[float] = None
    minValue: Optional[float] = None
    value: Optional[float] = None
    unitText: Optional[str] = None
    description: Optional[str] = None


@export
@attr.define(slots=True)
class QuantitativeValueSection(Item):
    name: Optional[str] = None
    content: Optional[QuantitativeValue] = None


@export
@attr.define(slots=True)
class Seller(Item):
    name: Optional[str] = None
    url: Optional[str] = None
    identifier: Optional[str] = None
    aggregateRating: Optional[common_fields.Rating] = None


@export
@attr.define(slots=True)
class ShippingInfo(Item):
    currency: str
    price: Optional[str] = None
    hasDeliveryMethod: Optional[str] = None
    minDays: Optional[int] = None
    maxDays: Optional[int] = None
    averageDays: Optional[float] = None
    description: Optional[str] = None
    originAddress: Optional[common_fields.Address] = None
    raw: Optional[str] = None


@export
@attr.define(slots=True)
class ItemCondition(Item):
    type: Optional[str] = None
    raw: Optional[str] = None


@export
@attr.define(slots=True)
class PricePerUnit(Item):
    unit: str
    price: Optional[str] = None
    currency: Optional[str] = None


@export
@attr.define(slots=True)
class Ownership(Item):
    type: str
    duration: Optional[str] = None


@export
@attr.define(slots=True)
class Offer(common_fields.Offer):
    inventoryLevel: Optional[QuantitativeValue] = None
    availability: Optional[str] = None
    currency: Optional[str] = None
    regularPrice: Optional[str] = None
    price: Optional[str] = None
    eligibleQuantity: Optional[QuantitativeValue] = None
    seller: Optional[Seller] = None
    shippingInfo: Optional[ShippingInfo] = None
    availableAtOrFrom: Optional[common_fields.Address] = None
    areaServed: Optional[common_fields.Address] = None
    itemCondition: Optional[ItemCondition] = None
    pricePerUnit: Optional[PricePerUnit] = None
    eligibleCustomerType: Optional[str] = None
    ownership: Optional[Ownership] = None
    additionalProperty: List[common_fields.AdditionalProperty] = attr.Factory(list)


@export
@attr.define(slots=True)
class Ranking(Item):
    category: str
    rank: int


@export
@attr.define(slots=True)
class Nutrition(Item):
    description: Optional[str] = None
    calories: Optional[QuantitativeValue] = None
    carbohydrateContent: Optional[QuantitativeValue] = None
    cholesterolContent: Optional[QuantitativeValue] = None
    fatContent: Optional[QuantitativeValue] = None
    fiberContent: Optional[QuantitativeValue] = None
    proteinContent: Optional[QuantitativeValue] = None
    saturatedFatContent: Optional[QuantitativeValue] = None
    sodiumContent: Optional[QuantitativeValue] = None
    sugarContent: Optional[QuantitativeValue] = None
    transFatContent: Optional[QuantitativeValue] = None
    unsaturatedFatContent: Optional[QuantitativeValue] = None
    waterContent: Optional[QuantitativeValue] = None
    vitaminsContent: List[QuantitativeValueSection] = attr.factory(list)
    mineralsContent: List[QuantitativeValueSection] = attr.factory(list)


@export
@attr.define(slots=True)
class ReviewRating(Item):
    ratingValue: float
    bestRating: Optional[float] = None
    worstRating: Optional[float] = None


@export
@attr.define(slots=True)
class Review(zda.Review):
    itemReviewed: Optional[str] = None
    reviewRating: Optional[ReviewRating] = None
    author: Optional[common_fields.Author] = None
    dateCreated: Optional[str] = None
    dateCreatedRaw: Optional[str] = None
    dateModified: Optional[str] = None
    dateModifiedRaw: Optional[str] = None
    url: Optional[str] = None
    isIncentivised: Optional[bool] = None


@export
@attr.define(slots=True)
class ProductReview(zda.Review):
    name: Optional[str] = None
    reviewBody: Optional[str] = None
    datepublished: Optional[str] = None
    datepublishedRaw: Optional[str] = None
    votedHelpful: Optional[int] = None
    votedUnhelpful: Optional[int] = None
    isIncentivised: Optional[bool] = None
    isVerified: Optional[bool] = None


@export
@attr.define(slots=True)
class BasicProduct(zda.BasicProduct):
    ratingHistogram: List[RatingHistogram] = attr.factory(list)
    questions: List[Question] = attr.factory(list)
    madeIn: Optional[str] = None
    offers: List[Offer] = attr.Factory(list)
    manufacturer: Optional[str] = None
    productionDate: Optional[str] = None
    productionDateRaw: Optional[str] = None
    height: Optional[QuantitativeValue] = None
    width: Optional[QuantitativeValue] = None
    depth: Optional[QuantitativeValue] = None
    weight: Optional[QuantitativeValue] = None
    volume: Optional[QuantitativeValue] = None
    releaseDate: Optional[str] = None
    releaseDateRaw: Optional[str] = None
    rankings: List[Ranking] = attr.Factory(list)
    nutrition: List[Nutrition] = attr.Factory(list)


@export
@attr.define(slots=True)
class RelatedProduct(Item):
    relationshipName: str
    products: List[BasicProduct] = attr.factory(list)


@export
@attr.define(slots=True)
class Product(BasicProduct):
    relatedProducts: List[RelatedProduct] = attr.Factory(list)
    hasVariants: List[BasicProduct] = attr.Factory(list)
    reviews: List[ProductReview] = attr.Factory(list)


@export
@attr.define(slots=True)
class Comment(zda.Comment):
    author: Optional[common_fields.Author] = None
    dateModified: Optional[str] = None
    dateModifiedRaw: Optional[str] = None
    edited: Optional[bool] = None
    identifier: Optional[str] = None
    locationCreated: Optional[common_fields.Address] = None
    pageUrl: Optional[str] = None
    parentIdentifier: Optional[str] = None
    replyCount: Optional[str] = None
    textHtml: Optional[str] = None
    textRaw: Optional[str] = None


@export
@attr.define(slots=True)
class ForumPost(zda.ForumPostList):
    posts: List[common_fields.Comment] = None


@export
@attr.define(slots=True)
class Organization(Item):
    name: Optional[str] = None
    location: Optional[common_fields.Address] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    raw: Optional[str] = None


@export
@attr.define(slots=True)
class Salary(common_fields.Salary):
    minValue: Optional[int] = None
    maxValue: Optional[int] = None


@export
@attr.define(slots=True)
class JobPosting(zda.JobPosting):
    jobLocation: Optional[common_fields.Address] = None
    datePostedRaw: Optional[str] = None
    validThroughRaw: Optional[str] = None
    hiringOrganization: Optional[Organization] = None
    baseSalary: Optional[Salary] = None


@export
@attr.define(slots=True)
class SearchResult(Item):
    description: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    type: Optional[str] = None
    synopsis: Optional[str] = None
    rank: Optional[int] = None


@export
@attr.define(slots=True)
class RelatedResult(Item):
    name: Optional[str] = None
    url: Optional[str] = None


@export
@attr.define(slots=True)
class CarouselItem(Item):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    url: Optional[str] = None
    mainImage: Optional[common_fields.Image] = None


@export
@attr.define(slots=True)
class RelatedSearch(Item):
    title: Optional[str] = None
    results = List[CarouselItem] = None


@export
@attr.define(slots=True)
class SearchInfoBox(Item):
    name: Optional[str] = None
    subtitle: Optional[str] = None
    mainImage: Optional[common_fields.Image] = None
    description: Optional[str] = None
    relatedResults: List[RelatedResult] = attr.Factory(list)
    additionalProperty: List[common_fields.AdditionalProperty] = attr.Factory(list)
    relatedSearches: List[RelatedSearch] = attr.Factory(list)


@export
@attr.define(slots=True)
class SearchResults(Item):
    url: str
    query: str
    identifier: Optional[str] = None
    numberOfItems: Optional[int] = None
    numberOfItemsRaw: Optional[str] = None
    results: List[SearchResult] = None
    page: Optional[int] = None
    didYouMean: Optional[int] = None
    resultsFor: Optional[int] = None
    infoBox: Optional[SearchInfoBox] = None


@export
@attr.define(slots=True)
class GeoCoordinates(Item):
    latitude: Optional[Any[str, float]] = None
    longitude: Optional[Any[str, float]] = None


@export
@attr.define(slots=True)
class RestaurantRating(Item):
    ratingValue: Optional[float] = None
    bestRating: Optional[float] = None
    reviewCount: Optional[int] = None
    reviewAspect: Optional[str] = None


@export
@attr.define(slots=True)
class MenuSection(Item):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[str] = None
    identifier: Optional[str] = None
    image: Optional[common_fields.Image] = None


@export
@attr.define(slots=True)
class RestaurantMenu(Item):
    name: Optional[str] = None
    sections: List[MenuSection] = attr.factory(list)
    menuRaw: Optional[str] = None
    menuUrl: Optional[str] = None


@export
@attr.define(slots=True)
class Fee(Item):
    deliveryFee: Optional[str] = None
    minimumDelivery: Optional[str] = None
    currency: Optional[str] = None
    raw: Optional[str] = None


@export
@attr.define(slots=True)
class OperatingHours(Item):
    day_range: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None


@export
@attr.define(slots=True)
class Restaurant(Item):
    address: Optional[common_fields.Address] = None
    geo: Optional[GeoCoordinates] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    website: Optional[str] = None
    rating: Optional[RestaurantRating] = None
    openingHours: List[OperatingHours] = attr.factory(list)
    openingHoursRaw: Optional[str] = None
    images: List[common_fields.Image] = attr.Factory(list)
    mainImage: Optional[common_fields.Image] = None
    additionalProperty: List[common_fields.AdditionalProperty] = attr.Factory(list)
    identifier: Optional[str] = None
    menu: Optional[RestaurantMenu] = None
    priceRange: Optional[str] = None
    currency: Optional[str] = None
    fees: Optional[Fee] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    cuisines: List[str] = attr.Factory(list)


@export
@attr.define(slots=True)
class MileageFromOdometer(common_fields.MileageFromOdometer):
    raw: Optional[str] = None


@export
@attr.define(slots=True)
class VehicleEngine(common_fields.VehicleEngine):
    engineDisplacement: Optional[QuantitativeValue] = None
    enginePower: Optional[QuantitativeValue] = None
    engineType: Optional[str] = None
    torque: Optional[QuantitativeValue] = None


@export
@attr.define(slots=True)
class FuelEfficiency(common_fields.FuelEfficiency):
    value: Optional[float] = None
    unitText: Optional[str] = None
    valueReference: Optional[str] = None


@export
@attr.define(slots=True)
class Vehicle(zda.Vehicle):
    ratingHistogram: List[RatingHistogram] = attr.factory(list)
    questions: List[Question] = attr.factory(list)
    madeIn: Optional[str] = None
    offers: List[Offer] = attr.Factory(list)
    gtin: List[common_fields.GTIN] = attr.Factory(list)
    manufacturer: Optional[str] = None
    productionDate: Optional[str] = None
    productionDateRaw: Optional[str] = None
    size: Optional[str] = None
    style: Optional[str] = None
    height: Optional[QuantitativeValue] = None
    width: Optional[QuantitativeValue] = None
    depth: Optional[QuantitativeValue] = None
    weight: Optional[QuantitativeValue] = None
    volume: Optional[QuantitativeValue] = None
    releaseDate: Optional[str] = None
    releaseDateRaw: Optional[str] = None
    rankings: List[Ranking] = attr.Factory(list)
    mileageFromOdometer: Optional[MileageFromOdometer] = None
    vehicleEngine: Optional[VehicleEngine] = None
    fuelEfficiency: List[FuelEfficiency] = attr.Factory(list)
