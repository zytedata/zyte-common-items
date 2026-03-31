import attrs
from web_poet import Returns

from zyte_common_items.components import (
    AdditionalProperty,
    Address,
    Breadcrumb,
    Image,
    RealEstateArea,
)
from zyte_common_items.fields import auto_field
from zyte_common_items.items import RealEstate, RealEstateMetadata

from ..processors import breadcrumbs_processor, description_processor, images_processor
from .base import BasePage, Page
from .mixins import HasMetadata


class BaseRealEstatePage(
    BasePage, Returns[RealEstate], HasMetadata[RealEstateMetadata]
):
    """:class:`BasePage` subclass for :class:`RealEstate`."""

    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]
        description = [description_processor]
        images = [images_processor]


class RealEstatePage(Page, Returns[RealEstate], HasMetadata[RealEstateMetadata]):
    """:class:`Page` subclass for :class:`RealEstate`."""

    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]
        description = [description_processor]
        images = [images_processor]


@attrs.define
class AutoRealEstatePage(BaseRealEstatePage):
    real_estate: RealEstate

    @auto_field
    def additionalProperties(self) -> list[AdditionalProperty] | None:
        return self.real_estate.additionalProperties

    @auto_field
    def address(self) -> Address | None:
        return self.real_estate.address

    @auto_field
    def area(self) -> RealEstateArea | None:
        return self.real_estate.area

    @auto_field
    def breadcrumbs(self) -> list[Breadcrumb] | None:
        return self.real_estate.breadcrumbs

    @auto_field
    def currency(self) -> str | None:
        return self.real_estate.currency

    @auto_field
    def currencyRaw(self) -> str | None:
        return self.real_estate.currencyRaw

    @auto_field
    def datePublished(self) -> str | None:
        return self.real_estate.datePublished

    @auto_field
    def datePublishedRaw(self) -> str | None:
        return self.real_estate.datePublishedRaw

    @auto_field
    def description(self) -> str | None:
        return self.real_estate.description

    @auto_field
    def images(self) -> list[Image] | None:
        return self.real_estate.images

    @auto_field
    def mainImage(self) -> Image | None:
        return self.real_estate.mainImage

    @auto_field
    def metadata(self) -> RealEstateMetadata | None:
        return self.real_estate.metadata

    @auto_field
    def name(self) -> str | None:
        return self.real_estate.name

    @auto_field
    def numberOfBathroomsTotal(self) -> int | None:
        return self.real_estate.numberOfBathroomsTotal

    @auto_field
    def numberOfBedrooms(self) -> int | None:
        return self.real_estate.numberOfBedrooms

    @auto_field
    def numberOfFullBathrooms(self) -> int | None:
        return self.real_estate.numberOfFullBathrooms

    @auto_field
    def numberOfPartialBathrooms(self) -> int | None:
        return self.real_estate.numberOfPartialBathrooms

    @auto_field
    def numberOfRooms(self) -> int | None:
        return self.real_estate.numberOfRooms

    @auto_field
    def price(self) -> str | None:
        return self.real_estate.price

    @auto_field
    def propertyType(self) -> str | None:
        return self.real_estate.propertyType

    @auto_field
    def realEstateId(self) -> str | None:
        return self.real_estate.realEstateId

    @auto_field
    def rentalPeriod(self) -> str | None:
        return self.real_estate.rentalPeriod

    @auto_field
    def tradeType(self) -> str | None:
        return self.real_estate.tradeType

    @auto_field
    def url(self) -> str | None:
        return self.real_estate.url

    @auto_field
    def virtualTourUrl(self) -> str | None:
        return self.real_estate.virtualTourUrl

    @auto_field
    def yearBuilt(self) -> int | None:
        return self.real_estate.yearBuilt
