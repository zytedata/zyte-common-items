from typing import List, Optional

import attrs
from web_poet import Returns, field

from zyte_common_items.components import (
    AdditionalProperty,
    Address,
    Breadcrumb,
    Image,
    RealEstateArea,
)
from zyte_common_items.items import RealEstate, RealEstateMetadata

from ..processors import breadcrumbs_processor, description_processor
from .base import BasePage, Page
from .mixins import HasMetadata


class BaseRealEstatePage(
    BasePage, Returns[RealEstate], HasMetadata[RealEstateMetadata]
):
    """:class:`BasePage` subclass for :class:`RealEstate`."""

    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]
        description = [description_processor]


class RealEstatePage(Page, Returns[RealEstate], HasMetadata[RealEstateMetadata]):
    """:class:`Page` subclass for :class:`RealEstate`."""

    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]
        description = [description_processor]


@attrs.define
class AutoRealEstatePage(BaseRealEstatePage):
    real_estate: RealEstate

    @field
    def additionalProperties(self) -> Optional[List[AdditionalProperty]]:
        return self.real_estate.additionalProperties

    @field
    def address(self) -> Optional[Address]:
        return self.real_estate.address

    @field
    def area(self) -> Optional[RealEstateArea]:
        return self.real_estate.area

    @field
    def breadcrumbs(self) -> Optional[List[Breadcrumb]]:
        return self.real_estate.breadcrumbs

    @field
    def currency(self) -> Optional[str]:
        return self.real_estate.currency

    @field
    def currencyRaw(self) -> Optional[str]:
        return self.real_estate.currencyRaw

    @field
    def datePublished(self) -> Optional[str]:
        return self.real_estate.datePublished

    @field
    def datePublishedRaw(self) -> Optional[str]:
        return self.real_estate.datePublishedRaw

    @field
    def description(self) -> Optional[str]:
        return self.real_estate.description

    @field
    def images(self) -> Optional[List[Image]]:
        return self.real_estate.images

    @field
    def mainImage(self) -> Optional[Image]:
        return self.real_estate.mainImage

    @field
    def metadata(self) -> Optional[RealEstateMetadata]:
        return self.real_estate.metadata

    @field
    def name(self) -> Optional[str]:
        return self.real_estate.name

    @field
    def numberOfBathroomsTotal(self) -> Optional[int]:
        return self.real_estate.numberOfBathroomsTotal

    @field
    def numberOfBedrooms(self) -> Optional[int]:
        return self.real_estate.numberOfBedrooms

    @field
    def numberOfFullBathrooms(self) -> Optional[int]:
        return self.real_estate.numberOfFullBathrooms

    @field
    def numberOfPartialBathrooms(self) -> Optional[int]:
        return self.real_estate.numberOfPartialBathrooms

    @field
    def numberOfRooms(self) -> Optional[int]:
        return self.real_estate.numberOfRooms

    @field
    def price(self) -> Optional[str]:
        return self.real_estate.price

    @field
    def propertyType(self) -> Optional[str]:
        return self.real_estate.propertyType

    @field
    def realEstateId(self) -> Optional[str]:
        return self.real_estate.realEstateId

    @field
    def rentalPeriod(self) -> Optional[str]:
        return self.real_estate.rentalPeriod

    @field
    def tradeType(self) -> Optional[str]:
        return self.real_estate.tradeType

    @field
    def url(self) -> Optional[str]:
        return self.real_estate.url

    @field
    def virtualTourUrl(self) -> Optional[str]:
        return self.real_estate.virtualTourUrl

    @field
    def yearBuilt(self) -> Optional[int]:
        return self.real_estate.yearBuilt
