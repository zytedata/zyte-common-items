import attrs
from web_poet import Returns

from zyte_common_items.components import (
    AdditionalProperty,
    Address,
    AggregateRating,
    Amenity,
    Image,
    NamedLink,
    OpeningHoursItem,
    ParentPlace,
    StarRating,
)
from zyte_common_items.fields import auto_field
from zyte_common_items.items import BusinessPlace, BusinessPlaceMetadata
from zyte_common_items.processors import (
    description_processor,
    images_processor,
    rating_processor,
)

from .base import BasePage, Page
from .mixins import HasMetadata


class BaseBusinessPlacePage(
    BasePage, Returns[BusinessPlace], HasMetadata[BusinessPlaceMetadata]
):
    """:class:`BasePage` subclass for :class:`BusinessPlace`."""

    class Processors(BasePage.Processors):
        aggregateRating = [rating_processor]
        description = [description_processor]
        images = [images_processor]


class BusinessPlacePage(
    Page, Returns[BusinessPlace], HasMetadata[BusinessPlaceMetadata]
):
    """:class:`Page` subclass for :class:`BusinessPlace`."""

    class Processors(Page.Processors):
        aggregateRating = [rating_processor]
        description = [description_processor]
        images = [images_processor]


@attrs.define
class AutoBusinessPlacePage(BaseBusinessPlacePage):
    business_place: BusinessPlace

    @auto_field
    def actions(self) -> list[NamedLink] | None:
        return self.business_place.actions

    @auto_field
    def additionalProperties(self) -> list[AdditionalProperty] | None:
        return self.business_place.additionalProperties

    @auto_field
    def address(self) -> Address | None:
        return self.business_place.address

    @auto_field
    def aggregateRating(self) -> AggregateRating | None:
        return self.business_place.aggregateRating

    @auto_field
    def amenityFeatures(self) -> list[Amenity] | None:
        return self.business_place.amenityFeatures

    @auto_field
    def categories(self) -> list[str] | None:
        return self.business_place.categories

    @auto_field
    def containedInPlace(self) -> ParentPlace | None:
        return self.business_place.containedInPlace

    @auto_field
    def description(self) -> str | None:
        return self.business_place.description

    @auto_field
    def features(self) -> list[str] | None:
        return self.business_place.features

    @auto_field
    def images(self) -> list[Image] | None:
        return self.business_place.images

    @auto_field
    def isVerified(self) -> bool | None:
        return self.business_place.isVerified

    @auto_field
    def map(self) -> str | None:
        return self.business_place.map

    @auto_field
    def metadata(self) -> BusinessPlaceMetadata | None:
        return self.business_place.metadata

    @auto_field
    def name(self) -> str | None:
        return self.business_place.name

    @auto_field
    def openingHours(self) -> list[OpeningHoursItem] | None:
        return self.business_place.openingHours

    @auto_field
    def placeId(self) -> str | None:
        return self.business_place.placeId

    @auto_field
    def priceRange(self) -> str | None:
        return self.business_place.priceRange

    @auto_field
    def reservationAction(self) -> NamedLink | None:
        return self.business_place.reservationAction

    @auto_field
    def reviewSites(self) -> list[NamedLink] | None:
        return self.business_place.reviewSites

    @auto_field
    def starRating(self) -> StarRating | None:
        return self.business_place.starRating

    @auto_field
    def tags(self) -> list[str] | None:
        return self.business_place.tags

    @auto_field
    def telephone(self) -> str | None:
        return self.business_place.telephone

    @auto_field
    def timezone(self) -> str | None:
        return self.business_place.timezone

    @auto_field
    def url(self) -> str | None:
        return self.business_place.url

    @auto_field
    def website(self) -> str | None:
        return self.business_place.website
