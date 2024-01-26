import html
from datetime import datetime
from typing import Any, Generic, List, Optional, Type, TypeVar, Union

import attrs
import html_text
from clear_html import cleaned_node_to_text
from lxml.html import HtmlElement
from price_parser import Price
from web_poet import ItemPage, RequestUrl, Returns, WebPage, field
from web_poet.fields import FieldsMixin
from web_poet.pages import ItemT
from web_poet.utils import ensure_awaitable, get_generic_param

from .components import (
    AdditionalProperty,
    Address,
    AggregateRating,
    Amenity,
    ArticleListMetadata,
    ArticleMetadata,
    ArticleNavigationMetadata,
    Audio,
    Author,
    BaseSalary,
    Brand,
    Breadcrumb,
    BusinessPlaceMetadata,
    Gtin,
    HiringOrganization,
    Image,
    JobLocation,
    JobPostingMetadata,
    Link,
    NamedLink,
    OpeningHoursItem,
    ParentPlace,
    ProbabilityRequest,
    ProductListMetadata,
    ProductMetadata,
    ProductNavigationMetadata,
    Reactions,
    RealEstateArea,
    RealEstateMetadata,
    Request,
    SocialMediaPostAuthor,
    SocialMediaPostMetadata,
    StarRating,
    Url,
    Video,
    request_list_processor,
)
from .items import (
    Article,
    ArticleFromList,
    ArticleList,
    ArticleNavigation,
    BusinessPlace,
    JobPosting,
    Product,
    ProductFromList,
    ProductList,
    ProductNavigation,
    ProductVariant,
    RealEstate,
    SocialMediaPost,
)
from .processors import (
    brand_processor,
    breadcrumbs_processor,
    description_html_processor,
    description_processor,
    gtin_processor,
    price_processor,
    rating_processor,
    simple_price_processor,
)
from .util import format_datetime, metadata_processor

#: Generic type for metadata classes for specific item types.
MetadataT = TypeVar("MetadataT")


def _date_downloaded_now():
    return format_datetime(datetime.utcnow())


class HasMetadata(Generic[MetadataT]):
    """Inherit from this generic mixin to set the metadata class used by a page
    class."""

    @property
    def metadata_cls(self) -> Optional[Type[MetadataT]]:
        """Metadata class."""
        return _get_metadata_class(type(self))


def _get_metadata_class(cls: type) -> Optional[Type[MetadataT]]:
    return get_generic_param(cls, HasMetadata)


class PriceMixin(FieldsMixin):
    """Provides price-related field implementations."""

    _parsed_price: Optional[Price] = None

    async def _get_parsed_price(self) -> Optional[Price]:
        if self._parsed_price is None:
            # the price field wasn't executed or doesn't write _parsed_price
            price = getattr(self, "price", None)
            price = await ensure_awaitable(price)
            if self._parsed_price is None:
                # the price field doesn't write _parsed_price (or doesn't exist)
                self._parsed_price = Price(
                    amount=None, currency=None, amount_text=price
                )
        return self._parsed_price

    @field
    def currency(self) -> Optional[str]:
        return getattr(self, "CURRENCY", None)

    @field
    async def currencyRaw(self) -> Optional[str]:
        parsed_price = await self._get_parsed_price()
        if parsed_price:
            return parsed_price.currency
        return None


class DescriptionMixin(FieldsMixin):
    """Provides description and descriptionHtml field implementations."""

    UNSET = object()

    _descriptionHtml_node: Any = UNSET
    _description_node: Any = UNSET
    _description_str: Any = UNSET

    _description_default = False
    _descriptionHtml_default = False

    @staticmethod
    def wrap_description_into_html(description: str) -> str:
        r"""Convert plain text into an article HTML.

        The format tries to match clear_html.cleaned_node_to_html().

        >>> DescriptionMixin.wrap_description_into_html('')
        '<article>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('foo')
        '<article>\n\n<p>foo</p>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('foo\nbar')
        '<article>\n\n<p>foo</p>\n\n<p>bar</p>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('foo\n\nbar')
        '<article>\n\n<p>foo</p>\n\n<p>bar</p>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('\nfoo\n\nbar\n')
        '<article>\n\n<p>foo</p>\n\n<p>bar</p>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('foo\nbar\n\nbaz\n')
        '<article>\n\n<p>foo</p>\n\n<p>bar</p>\n\n<p>baz</p>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('2>1')
        '<article>\n\n<p>2&gt;1</p>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('<p>')
        '<article>\n\n<p>&lt;p&gt;</p>\n\n</article>'
        >>> DescriptionMixin.wrap_description_into_html('&lt;p&gt;')
        '<article>\n\n<p>&amp;lt;p&amp;gt;</p>\n\n</article>'
        """
        paras_wrapped = [
            f"\n<p>{html.escape(para)}</p>\n"
            for para in description.split("\n")
            if para
        ]
        return f"<article>\n{''.join(paras_wrapped)}\n</article>"

    async def _get_description(self) -> Optional[str]:
        if self._description_default:
            return None
        if self._description_str == self.UNSET:
            description = await ensure_awaitable(self.description)
            if self._description_str == self.UNSET:
                # the description field doesn't write _description_str
                self._description_str = description
        return self._description_str

    async def _get_description_html(self) -> Optional[HtmlElement]:
        if self._descriptionHtml_default:
            return None
        if self._descriptionHtml_node == self.UNSET:
            descriptionHtml = await ensure_awaitable(self.descriptionHtml)
            if self._descriptionHtml_node == self.UNSET:
                # the descriptionHtml field doesn't write _descriptionHtml_node
                self._descriptionHtml_node = descriptionHtml
        return self._descriptionHtml_node

    @field
    async def description(self) -> Optional[str]:
        self._description_default = True
        description_html = await self._get_description_html()
        if isinstance(description_html, HtmlElement):
            return cleaned_node_to_text(description_html)
        if isinstance(description_html, str):
            return html_text.extract_text(description_html)
        return None

    @field
    async def descriptionHtml(self) -> Union[HtmlElement, str, None]:
        self._descriptionHtml_default = True
        description = await self._get_description()
        if self._description_node not in {self.UNSET, None}:
            # we can use the element provided by the description field
            return self._description_node
        if isinstance(description, str):
            return self.wrap_description_into_html(description)
        return None


class _BasePage(ItemPage[ItemT], HasMetadata[MetadataT]):
    class Processors:
        metadata = [metadata_processor]

    @field
    def metadata(self) -> MetadataT:
        if self.metadata_cls is None:
            raise ValueError(f"{type(self)} doesn'have a metadata class configured.")
        value = self.metadata_cls()
        attributes = dir(value)
        if "dateDownloaded" in attributes:
            value.dateDownloaded = _date_downloaded_now()  # type: ignore
        if "probability" in attributes:
            value.probability = 1.0  # type: ignore
        return value

    def no_item_found(self) -> ItemT:
        """Return an item with the current url and probability=0,
        indicating that the passed URL doesn't contain the expected item.

        Use it in your .validate_input implementation.
        """
        if self.metadata_cls is None:
            raise ValueError(f"{type(self)} doesn'have a metadata class configured.")
        metadata = self.metadata_cls()
        metadata_attributes = dir(metadata)
        if "dateDownloaded" in metadata_attributes:
            metadata.dateDownloaded = _date_downloaded_now()  # type: ignore
        if "probability" in metadata_attributes:
            metadata.probability = 0.0  # type: ignore
        return self.item_cls(  # type: ignore
            url=self.url,  # type: ignore[attr-defined]
            metadata=metadata,
        )


@attrs.define
class BasePage(_BasePage):
    """Base class for page object classes that has
    :class:`~web_poet.page_inputs.http.RequestUrl` as a dependency."""

    class Processors(_BasePage.Processors):
        pass

    request_url: RequestUrl

    @field
    def url(self) -> str:
        return str(self.request_url)


class BaseArticlePage(BasePage, Returns[Article], HasMetadata[ArticleMetadata]):
    """:class:`BasePage` subclass for :class:`Article`."""

    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]


class BaseArticleListPage(
    BasePage, Returns[ArticleList], HasMetadata[ArticleListMetadata]
):
    """:class:`BasePage` subclass for :class:`ArticleList`."""

    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]


class BaseArticleNavigationPage(
    BasePage, Returns[ArticleNavigation], HasMetadata[ArticleNavigationMetadata]
):
    """:class:`BasePage` subclass for :class:`ArticleNavigation`."""


class BaseBusinessPlacePage(
    BasePage, Returns[BusinessPlace], HasMetadata[BusinessPlaceMetadata]
):
    """:class:`BasePage` subclass for :class:`BusinessPlace`."""

    class Processors(BasePage.Processors):
        aggregateRating = [rating_processor]
        description = [description_processor]


class BaseJobPostingPage(
    BasePage, DescriptionMixin, Returns[JobPosting], HasMetadata[JobPostingMetadata]
):
    """:class:`BasePage` subclass for :class:`JobPosting`."""

    class Processors(BasePage.Processors):
        description = [description_processor]
        descriptionHtml = [description_html_processor]


class BaseProductPage(
    BasePage,
    DescriptionMixin,
    PriceMixin,
    Returns[Product],
    HasMetadata[ProductMetadata],
):
    """:class:`BasePage` subclass for :class:`Product`."""

    class Processors(BasePage.Processors):
        aggregateRating = [rating_processor]
        brand = [brand_processor]
        breadcrumbs = [breadcrumbs_processor]
        description = [description_processor]
        descriptionHtml = [description_html_processor]
        gtin = [gtin_processor]
        price = [price_processor]
        regularPrice = [simple_price_processor]


class BaseProductListPage(
    BasePage, Returns[ProductList], HasMetadata[ProductListMetadata]
):
    """:class:`BasePage` subclass for :class:`ProductList`."""

    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]


class BaseProductNavigationPage(
    BasePage, Returns[ProductNavigation], HasMetadata[ProductNavigationMetadata]
):
    """:class:`BasePage` subclass for :class:`ProductNavigation`."""

    class Processors(BasePage.Processors):
        subCategories = [request_list_processor]
        items = [request_list_processor]


class BaseRealEstatePage(
    BasePage, Returns[RealEstate], HasMetadata[RealEstateMetadata]
):
    """:class:`BasePage` subclass for :class:`RealEstate`."""

    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]
        description = [description_processor]


class BaseSocialMediaPostPage(
    BasePage, Returns[SocialMediaPost], HasMetadata[SocialMediaPostMetadata]
):
    pass


@attrs.define
class Page(_BasePage, WebPage):
    """Base class for page object classes that has
    :class:`~web_poet.page_inputs.http.HttpResponse` as a dependency."""

    class Processors(_BasePage.Processors):
        pass

    @field
    def url(self) -> str:
        return str(self.response.url)


class ArticlePage(Page, Returns[Article], HasMetadata[ArticleMetadata]):
    """:class:`Page` subclass for :class:`Article`."""

    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]


class ArticleListPage(Page, Returns[ArticleList], HasMetadata[ArticleListMetadata]):
    """:class:`Page` subclass for :class:`ArticleList`."""

    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]


class ArticleNavigationPage(
    Page, Returns[ArticleNavigation], HasMetadata[ArticleNavigationMetadata]
):
    """:class:`Page` subclass for :class:`ArticleNavigation`."""


class BusinessPlacePage(
    Page, Returns[BusinessPlace], HasMetadata[BusinessPlaceMetadata]
):
    """:class:`Page` subclass for :class:`BusinessPlace`."""

    class Processors(Page.Processors):
        aggregateRating = [rating_processor]
        description = [description_processor]


class JobPostingPage(
    Page, DescriptionMixin, Returns[JobPosting], HasMetadata[JobPostingMetadata]
):
    """:class:`Page` subclass for :class:`JobPosting`."""

    class Processors(Page.Processors):
        description = [description_processor]
        descriptionHtml = [description_html_processor]


class ProductPage(
    Page, DescriptionMixin, PriceMixin, Returns[Product], HasMetadata[ProductMetadata]
):
    """:class:`Page` subclass for :class:`Product`."""

    class Processors(Page.Processors):
        aggregateRating = [rating_processor]
        brand = [brand_processor]
        breadcrumbs = [breadcrumbs_processor]
        description = [description_processor]
        descriptionHtml = [description_html_processor]
        gtin = [gtin_processor]
        price = [price_processor]
        regularPrice = [simple_price_processor]


class ProductListPage(Page, Returns[ProductList], HasMetadata[ProductListMetadata]):
    """:class:`Page` subclass for :class:`ProductList`."""

    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]


class ProductNavigationPage(
    Page, Returns[ProductNavigation], HasMetadata[ProductNavigationMetadata]
):
    """:class:`Page` subclass for :class:`ProductNavigation`."""


class RealEstatePage(Page, Returns[RealEstate], HasMetadata[RealEstateMetadata]):
    """:class:`Page` subclass for :class:`RealEstate`."""

    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]
        description = [description_processor]


class SocialMediaPostPage(
    Page, Returns[SocialMediaPost], HasMetadata[SocialMediaPostMetadata]
):
    pass


@attrs.define
class AutoProductPage(BaseProductPage):
    product: Product

    @field
    async def additionalProperties(self) -> Optional[List[AdditionalProperty]]:
        return self.product.additionalProperties

    @field
    async def aggregateRating(self) -> Optional[AggregateRating]:
        return self.product.aggregateRating

    @field
    async def availability(self) -> Optional[str]:
        return self.product.availability

    @field
    async def brand(self) -> Optional[Brand]:
        return self.product.brand

    @field
    async def breadcrumbs(self) -> Optional[List[Breadcrumb]]:
        return self.product.breadcrumbs

    @field
    async def canonicalUrl(self) -> Optional[str]:
        return self.product.canonicalUrl

    @field
    async def color(self) -> Optional[str]:
        return self.product.color

    @field
    async def currency(self) -> Optional[str]:
        return self.product.currency

    @field
    async def currencyRaw(self) -> Optional[str]:
        return self.product.currencyRaw

    @field
    async def description(self) -> Optional[str]:
        return self.product.description

    @field
    async def descriptionHtml(self) -> Optional[str]:
        return self.product.descriptionHtml

    @field
    async def features(self) -> Optional[List[str]]:
        return self.product.features

    @field
    async def gtin(self) -> Optional[List[Gtin]]:
        return self.product.gtin

    @field
    async def images(self) -> Optional[List[Image]]:
        return self.product.images

    @field
    async def mainImage(self) -> Optional[Image]:
        return self.product.mainImage

    @field
    async def metadata(self) -> Optional[ProductMetadata]:
        return self.product.metadata

    @field
    async def mpn(self) -> Optional[str]:
        return self.product.mpn

    @field
    async def name(self) -> Optional[str]:
        return self.product.name

    @field
    async def price(self) -> Optional[str]:
        return self.product.price

    @field
    async def productId(self) -> Optional[str]:
        return self.product.productId

    @field
    async def regularPrice(self) -> Optional[str]:
        return self.product.regularPrice

    @field
    async def size(self) -> Optional[str]:
        return self.product.size

    @field
    async def sku(self) -> Optional[str]:
        return self.product.sku

    @field
    async def style(self) -> Optional[str]:
        return self.product.style

    @field
    async def url(self) -> str:
        return self.product.url

    @field
    async def variants(self) -> Optional[List[ProductVariant]]:
        return self.product.variants


@attrs.define
class AutoProductListPage(BaseProductListPage):
    product_list: ProductList

    @field
    async def breadcrumbs(self) -> Optional[List[Breadcrumb]]:
        return self.product_list.breadcrumbs

    @field
    async def canonicalUrl(self) -> Optional[str]:
        return self.product_list.canonicalUrl

    @field
    async def categoryName(self) -> Optional[str]:
        return self.product_list.categoryName

    @field
    async def metadata(self) -> Optional[ProductListMetadata]:
        return self.product_list.metadata

    @field
    async def pageNumber(self) -> Optional[int]:
        return self.product_list.pageNumber

    @field
    async def paginationNext(self) -> Optional[Link]:
        return self.product_list.paginationNext

    @field
    async def products(self) -> Optional[List[ProductFromList]]:
        return self.product_list.products

    @field
    async def url(self) -> Optional[str]:
        return self.product_list.url


@attrs.define
class AutoProductNavigationPage(BaseProductNavigationPage):
    product_navigation: ProductNavigation

    @field
    async def categoryName(self) -> Optional[str]:
        return self.product_navigation.categoryName

    @field
    async def items(self) -> Optional[List[ProbabilityRequest]]:
        return self.product_navigation.items

    @field
    async def metadata(self) -> Optional[ProductNavigationMetadata]:
        return self.product_navigation.metadata

    @field
    async def nextPage(self) -> Optional[Request]:
        return self.product_navigation.nextPage

    @field
    async def pageNumber(self) -> Optional[int]:
        return self.product_navigation.pageNumber

    @field
    async def subCategories(self) -> Optional[List[ProbabilityRequest]]:
        return self.product_navigation.subCategories

    @field
    async def url(self) -> Optional[str]:
        return self.product_navigation.url


@attrs.define
class AutoArticlePage(BaseArticlePage):
    article: Article

    @field
    async def headline(self) -> Optional[str]:
        return self.article.headline

    @field
    async def datePublished(self) -> Optional[str]:
        return self.article.datePublished

    @field
    async def datePublishedRaw(self) -> Optional[str]:
        return self.article.datePublishedRaw

    @field
    async def dateModified(self) -> Optional[str]:
        return self.article.dateModified

    @field
    async def dateModifiedRaw(self) -> Optional[str]:
        return self.article.dateModifiedRaw

    @field
    async def authors(self) -> Optional[List[Author]]:
        return self.article.authors

    @field
    async def breadcrumbs(self) -> Optional[List[Breadcrumb]]:
        return self.article.breadcrumbs

    @field
    async def inLanguage(self) -> Optional[str]:
        return self.article.inLanguage

    @field
    async def mainImage(self) -> Optional[Image]:
        return self.article.mainImage

    @field
    async def images(self) -> Optional[List[Image]]:
        return self.article.images

    @field
    async def description(self) -> Optional[str]:
        return self.article.description

    @field
    async def articleBody(self) -> Optional[str]:
        return self.article.articleBody

    @field
    async def articleBodyHtml(self) -> Optional[str]:
        return self.article.articleBodyHtml

    @field
    async def videos(self) -> Optional[List[Video]]:
        return self.article.videos

    @field
    async def audios(self) -> Optional[List[Audio]]:
        return self.article.audios

    @field
    async def canonicalUrl(self) -> Optional[str]:
        return self.article.canonicalUrl

    @field
    async def url(self) -> Optional[str]:
        return self.article.url

    @field
    async def metadata(self) -> Optional[ArticleMetadata]:
        return self.article.metadata


@attrs.define
class AutoArticleListPage(BaseArticleListPage):
    article_list: ArticleList

    @field
    async def articles(self) -> Optional[List[ArticleFromList]]:
        return self.article_list.articles

    @field
    async def breadcrumbs(self) -> Optional[List[Breadcrumb]]:
        return self.article_list.breadcrumbs

    @field
    async def canonicalUrl(self) -> Optional[str]:
        return self.article_list.canonicalUrl

    @field
    async def metadata(self) -> Optional[ArticleListMetadata]:
        return self.article_list.metadata

    @field
    async def url(self) -> Optional[str]:
        return self.article_list.url


@attrs.define
class AutoArticleNavigationPage(BaseArticleNavigationPage):
    article_navigation: ArticleNavigation

    @field
    async def categoryName(self) -> Optional[str]:
        return self.article_navigation.categoryName

    @field
    async def items(self) -> Optional[List[ProbabilityRequest]]:
        return self.article_navigation.items

    @field
    async def metadata(self) -> Optional[ArticleNavigationMetadata]:
        return self.article_navigation.metadata

    @field
    async def nextPage(self) -> Optional[Request]:
        return self.article_navigation.nextPage

    @field
    async def pageNumber(self) -> Optional[int]:
        return self.article_navigation.pageNumber

    @field
    async def subCategories(self) -> Optional[List[ProbabilityRequest]]:
        return self.article_navigation.subCategories

    @field
    async def url(self) -> Optional[str]:
        return self.article_navigation.url


@attrs.define
class AutoBusinessPlacePage(BaseBusinessPlacePage):
    business_place: BusinessPlace

    @field
    async def actions(self) -> Optional[List[NamedLink]]:
        return self.business_place.actions

    @field
    async def additionalProperties(self) -> Optional[List[AdditionalProperty]]:
        return self.business_place.additionalProperties

    @field
    async def address(self) -> Optional[Address]:
        return self.business_place.address

    @field
    async def aggregateRating(self) -> Optional[AggregateRating]:
        return self.business_place.aggregateRating

    @field
    async def amenityFeatures(self) -> Optional[List[Amenity]]:
        return self.business_place.amenityFeatures

    @field
    async def categories(self) -> Optional[List[str]]:
        return self.business_place.categories

    @field
    async def containedInPlace(self) -> Optional[ParentPlace]:
        return self.business_place.containedInPlace

    @field
    async def description(self) -> Optional[str]:
        return self.business_place.description

    @field
    async def features(self) -> Optional[List[str]]:
        return self.business_place.features

    @field
    async def images(self) -> Optional[List[Image]]:
        return self.business_place.images

    @field
    async def isVerified(self) -> Optional[bool]:
        return self.business_place.isVerified

    @field
    async def map(self) -> Optional[str]:
        return self.business_place.map

    @field
    async def metadata(self) -> Optional[BusinessPlaceMetadata]:
        return self.business_place.metadata

    @field
    async def name(self) -> Optional[str]:
        return self.business_place.name

    @field
    async def openingHours(self) -> Optional[List[OpeningHoursItem]]:
        return self.business_place.openingHours

    @field
    async def placeId(self) -> Optional[str]:
        return self.business_place.placeId

    @field
    async def priceRange(self) -> Optional[str]:
        return self.business_place.priceRange

    @field
    async def reservationAction(self) -> Optional[NamedLink]:
        return self.business_place.reservationAction

    @field
    async def reviewSites(self) -> Optional[List[NamedLink]]:
        return self.business_place.reviewSites

    @field
    async def starRating(self) -> Optional[StarRating]:
        return self.business_place.starRating

    @field
    async def tags(self) -> Optional[List[str]]:
        return self.business_place.tags

    @field
    async def telephone(self) -> Optional[str]:
        return self.business_place.telephone

    @field
    async def timezone(self) -> Optional[str]:
        return self.business_place.timezone

    @field
    async def url(self) -> Optional[str]:
        return self.business_place.url

    @field
    async def website(self) -> Optional[str]:
        return self.business_place.website


@attrs.define
class AutoRealEstatePage(BaseRealEstatePage):
    real_estate: RealEstate

    @field
    async def additionalProperties(self) -> Optional[List[AdditionalProperty]]:
        return self.real_estate.additionalProperties

    @field
    async def address(self) -> Optional[Address]:
        return self.real_estate.address

    @field
    async def area(self) -> Optional[RealEstateArea]:
        return self.real_estate.area

    @field
    async def breadcrumbs(self) -> Optional[List[Breadcrumb]]:
        return self.real_estate.breadcrumbs

    @field
    async def currency(self) -> Optional[str]:
        return self.real_estate.currency

    @field
    async def currencyRaw(self) -> Optional[str]:
        return self.real_estate.currencyRaw

    @field
    async def datePublished(self) -> Optional[str]:
        return self.real_estate.datePublished

    @field
    async def datePublishedRaw(self) -> Optional[str]:
        return self.real_estate.datePublishedRaw

    @field
    async def description(self) -> Optional[str]:
        return self.real_estate.description

    @field
    async def images(self) -> Optional[List[Image]]:
        return self.real_estate.images

    @field
    async def mainImage(self) -> Optional[Image]:
        return self.real_estate.mainImage

    @field
    async def metadata(self) -> Optional[RealEstateMetadata]:
        return self.real_estate.metadata

    @field
    async def name(self) -> Optional[str]:
        return self.real_estate.name

    @field
    async def numberOfBathroomsTotal(self) -> Optional[int]:
        return self.real_estate.numberOfBathroomsTotal

    @field
    async def numberOfBedrooms(self) -> Optional[int]:
        return self.real_estate.numberOfBedrooms

    @field
    async def numberOfFullBathrooms(self) -> Optional[int]:
        return self.real_estate.numberOfFullBathrooms

    @field
    async def numberOfPartialBathrooms(self) -> Optional[int]:
        return self.real_estate.numberOfPartialBathrooms

    @field
    async def numberOfRooms(self) -> Optional[int]:
        return self.real_estate.numberOfRooms

    @field
    async def price(self) -> Optional[str]:
        return self.real_estate.price

    @field
    async def propertyType(self) -> Optional[str]:
        return self.real_estate.propertyType

    @field
    async def realEstateId(self) -> Optional[str]:
        return self.real_estate.realEstateId

    @field
    async def rentalPeriod(self) -> Optional[str]:
        return self.real_estate.rentalPeriod

    @field
    async def tradeType(self) -> Optional[str]:
        return self.real_estate.tradeType

    @field
    async def url(self) -> Optional[str]:
        return self.real_estate.url

    @field
    async def virtualTourUrl(self) -> Optional[str]:
        return self.real_estate.virtualTourUrl

    @field
    async def yearBuilt(self) -> Optional[int]:
        return self.real_estate.yearBuilt


@attrs.define
class AutoJobPostingPage(BaseJobPostingPage):
    job_posting: JobPosting

    @field
    async def url(self) -> Optional[str]:
        return self.job_posting.url

    @field
    async def jobPostingId(self) -> Optional[str]:
        return self.job_posting.jobPostingId

    @field
    async def datePublished(self) -> Optional[str]:
        return self.job_posting.datePublished

    @field
    async def datePublishedRaw(self) -> Optional[str]:
        return self.job_posting.datePublishedRaw

    @field
    async def dateModified(self) -> Optional[str]:
        return self.job_posting.dateModified

    @field
    async def dateModifiedRaw(self) -> Optional[str]:
        return self.job_posting.dateModifiedRaw

    @field
    async def validThrough(self) -> Optional[str]:
        return self.job_posting.validThrough

    @field
    async def validThroughRaw(self) -> Optional[str]:
        return self.job_posting.validThroughRaw

    @field
    async def jobTitle(self) -> Optional[str]:
        return self.job_posting.jobTitle

    @field
    async def headline(self) -> Optional[str]:
        return self.job_posting.headline

    @field
    async def jobLocation(self) -> Optional[JobLocation]:
        return self.job_posting.jobLocation

    @field
    async def description(self) -> Optional[str]:
        return self.job_posting.description

    @field
    async def descriptionHtml(self) -> Optional[str]:
        return self.job_posting.descriptionHtml

    @field
    async def employmentType(self) -> Optional[str]:
        return self.job_posting.employmentType

    @field
    async def baseSalary(self) -> Optional[BaseSalary]:
        return self.job_posting.baseSalary

    @field
    async def requirements(self) -> Optional[List[str]]:
        return self.job_posting.requirements

    @field
    async def hiringOrganization(self) -> Optional[HiringOrganization]:
        return self.job_posting.hiringOrganization

    @field
    async def jobStartDate(self) -> Optional[str]:
        return self.job_posting.jobStartDate

    @field
    async def jobStartDateRaw(self) -> Optional[str]:
        return self.job_posting.jobStartDateRaw

    @field
    async def remoteStatus(self) -> Optional[str]:
        return self.job_posting.remoteStatus

    @field
    async def metadata(self) -> Optional[JobPostingMetadata]:
        return self.job_posting.metadata


@attrs.define
class AutoSocialMediaPostPage(BaseSocialMediaPostPage):
    social_media_post: SocialMediaPost

    @field
    async def url(self) -> Optional[str]:
        return self.social_media_post.url

    @field
    async def postId(self) -> Optional[str]:
        return self.social_media_post.postId

    @field
    async def reactions(self) -> Optional[Reactions]:
        return self.social_media_post.reactions

    @field
    async def text(self) -> Optional[str]:
        return self.social_media_post.text

    @field
    async def datePublished(self) -> Optional[str]:
        return self.social_media_post.datePublished

    @field
    async def hashtags(self) -> Optional[List[str]]:
        return self.social_media_post.hashtags

    @field
    async def mediaUrls(self) -> Optional[List[Url]]:
        return self.social_media_post.mediaUrls

    @field
    async def author(self) -> Optional[SocialMediaPostAuthor]:
        return self.social_media_post.author

    @field
    async def metadata(self) -> Optional[SocialMediaPostMetadata]:
        return self.social_media_post.metadata
