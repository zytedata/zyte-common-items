from typing import List, Optional

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
    def actions(self) -> Optional[List[NamedLink]]:
        return self.business_place.actions

    @auto_field
    def additionalProperties(self) -> Optional[List[AdditionalProperty]]:
        return self.business_place.additionalProperties

    @auto_field
    def address(self) -> Optional[Address]:
        return self.business_place.address

    @auto_field
    def aggregateRating(self) -> Optional[AggregateRating]:
        return self.business_place.aggregateRating

    @auto_field
    def amenityFeatures(self) -> Optional[List[Amenity]]:
        return self.business_place.amenityFeatures

    @auto_field
    def categories(self) -> Optional[List[str]]:
        return self.business_place.categories

    @auto_field
    def containedInPlace(self) -> Optional[ParentPlace]:
        return self.business_place.containedInPlace

    @auto_field
    def description(self) -> Optional[str]:
        return self.business_place.description

    @auto_field
    def features(self) -> Optional[List[str]]:
        return self.business_place.features

    @auto_field
    def images(self) -> Optional[List[Image]]:
        return self.business_place.images

    @auto_field
    def isVerified(self) -> Optional[bool]:
        return self.business_place.isVerified

    @auto_field
    def map(self) -> Optional[str]:
        return self.business_place.map

    @auto_field
    def metadata(self) -> Optional[BusinessPlaceMetadata]:
        return self.business_place.metadata

    @auto_field
    def name(self) -> Optional[str]:
        return self.business_place.name

    @auto_field
    def openingHours(self) -> Optional[List[OpeningHoursItem]]:
        return self.business_place.openingHours

    @auto_field
    def placeId(self) -> Optional[str]:
        return self.business_place.placeId

    @auto_field
    def priceRange(self) -> Optional[str]:
        return self.business_place.priceRange

    @auto_field
    def reservationAction(self) -> Optional[NamedLink]:
        return self.business_place.reservationAction

    @auto_field
    def reviewSites(self) -> Optional[List[NamedLink]]:
        return self.business_place.reviewSites

    @auto_field
    def starRating(self) -> Optional[StarRating]:
        return self.business_place.starRating

    @auto_field
    def tags(self) -> Optional[List[str]]:
        return self.business_place.tags

    @auto_field
    def telephone(self) -> Optional[str]:
        return self.business_place.telephone

    @auto_field
    def timezone(self) -> Optional[str]:
        return self.business_place.timezone

    @auto_field
    def url(self) -> Optional[str]:
        return self.business_place.url

    @auto_field
    def website(self) -> Optional[str]:
        return self.business_place.website
