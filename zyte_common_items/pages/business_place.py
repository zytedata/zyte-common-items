from typing import List, Optional

import attrs
from web_poet import Returns, field

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
from zyte_common_items.items import BusinessPlace, BusinessPlaceMetadata
from zyte_common_items.processors import description_processor, rating_processor

from .base import BasePage, Page
from .mixins import HasMetadata


class BaseBusinessPlacePage(
    BasePage, Returns[BusinessPlace], HasMetadata[BusinessPlaceMetadata]
):
    """:class:`BasePage` subclass for :class:`BusinessPlace`."""

    class Processors(BasePage.Processors):
        aggregateRating = [rating_processor]
        description = [description_processor]


class BusinessPlacePage(
    Page, Returns[BusinessPlace], HasMetadata[BusinessPlaceMetadata]
):
    """:class:`Page` subclass for :class:`BusinessPlace`."""

    class Processors(Page.Processors):
        aggregateRating = [rating_processor]
        description = [description_processor]


@attrs.define
class AutoBusinessPlacePage(BaseBusinessPlacePage):
    business_place: BusinessPlace

    @field
    def actions(self) -> Optional[List[NamedLink]]:
        return self.business_place.actions

    @field
    def additionalProperties(self) -> Optional[List[AdditionalProperty]]:
        return self.business_place.additionalProperties

    @field
    def address(self) -> Optional[Address]:
        return self.business_place.address

    @field
    def aggregateRating(self) -> Optional[AggregateRating]:
        return self.business_place.aggregateRating

    @field
    def amenityFeatures(self) -> Optional[List[Amenity]]:
        return self.business_place.amenityFeatures

    @field
    def categories(self) -> Optional[List[str]]:
        return self.business_place.categories

    @field
    def containedInPlace(self) -> Optional[ParentPlace]:
        return self.business_place.containedInPlace

    @field
    def description(self) -> Optional[str]:
        return self.business_place.description

    @field
    def features(self) -> Optional[List[str]]:
        return self.business_place.features

    @field
    def images(self) -> Optional[List[Image]]:
        return self.business_place.images

    @field
    def isVerified(self) -> Optional[bool]:
        return self.business_place.isVerified

    @field
    def map(self) -> Optional[str]:
        return self.business_place.map

    @field
    def metadata(self) -> Optional[BusinessPlaceMetadata]:
        return self.business_place.metadata

    @field
    def name(self) -> Optional[str]:
        return self.business_place.name

    @field
    def openingHours(self) -> Optional[List[OpeningHoursItem]]:
        return self.business_place.openingHours

    @field
    def placeId(self) -> Optional[str]:
        return self.business_place.placeId

    @field
    def priceRange(self) -> Optional[str]:
        return self.business_place.priceRange

    @field
    def reservationAction(self) -> Optional[NamedLink]:
        return self.business_place.reservationAction

    @field
    def reviewSites(self) -> Optional[List[NamedLink]]:
        return self.business_place.reviewSites

    @field
    def starRating(self) -> Optional[StarRating]:
        return self.business_place.starRating

    @field
    def tags(self) -> Optional[List[str]]:
        return self.business_place.tags

    @field
    def telephone(self) -> Optional[str]:
        return self.business_place.telephone

    @field
    def timezone(self) -> Optional[str]:
        return self.business_place.timezone

    @field
    def url(self) -> Optional[str]:
        return self.business_place.url

    @field
    def website(self) -> Optional[str]:
        return self.business_place.website
