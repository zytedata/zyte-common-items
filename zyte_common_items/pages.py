from datetime import datetime
from typing import Any, Generic, Optional, Type, TypeVar

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
    ArticleListMetadata,
    ArticleMetadata,
    ArticleNavigationMetadata,
    BusinessPlaceMetadata,
    JobPostingMetadata,
    ProductListMetadata,
    ProductMetadata,
    ProductNavigationMetadata,
    RealEstateMetadata,
    request_list_processor,
)
from .items import (
    Article,
    ArticleList,
    ArticleNavigation,
    BusinessPlace,
    JobPosting,
    Product,
    ProductList,
    ProductNavigation,
    RealEstate,
)
from .processors import (
    brand_processor,
    breadcrumbs_processor,
    description_html_processor,
    description_processor,
    price_processor,
    simple_price_processor,
)
from .util import format_datetime, metadata_processor, wrap_description_into_html

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

    _description_html: Any = UNSET
    _description_str: Any = UNSET

    _description_default = False
    _descriptionHtml_default = False

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
        if self._description_html == self.UNSET:
            descriptionHtml = await ensure_awaitable(self.descriptionHtml)
            if self._description_html == self.UNSET:
                # the descriptionHtml field doesn't write _description_html
                self._description_html = descriptionHtml
        return self._description_html

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
    async def descriptionHtml(self) -> Optional[str]:
        self._descriptionHtml_default = True
        description = await self._get_description()
        if isinstance(description, str):
            return wrap_description_into_html(description)
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
    class Processors(_BasePage.Processors):
        pass

    request_url: RequestUrl

    @field
    def url(self) -> str:
        return str(self.request_url)


class BaseArticlePage(BasePage, Returns[Article], HasMetadata[ArticleMetadata]):
    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]


class BaseArticleListPage(
    BasePage, Returns[ArticleList], HasMetadata[ArticleListMetadata]
):
    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]


class BaseArticleNavigationPage(
    BasePage, Returns[ArticleNavigation], HasMetadata[ArticleNavigationMetadata]
):
    pass


class BaseBusinessPlacePage(
    BasePage, Returns[BusinessPlace], HasMetadata[BusinessPlaceMetadata]
):
    pass


class BaseJobPostingPage(
    BasePage, Returns[JobPosting], HasMetadata[JobPostingMetadata]
):
    pass


class BaseProductPage(
    BasePage,
    DescriptionMixin,
    PriceMixin,
    Returns[Product],
    HasMetadata[ProductMetadata],
):
    class Processors(BasePage.Processors):
        brand = [brand_processor]
        breadcrumbs = [breadcrumbs_processor]
        description = [description_processor]
        descriptionHtml = [description_html_processor]
        price = [price_processor]
        regularPrice = [simple_price_processor]


class BaseProductListPage(
    BasePage, Returns[ProductList], HasMetadata[ProductListMetadata]
):
    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]


class BaseProductNavigationPage(
    BasePage, Returns[ProductNavigation], HasMetadata[ProductNavigationMetadata]
):
    class Processors(BasePage.Processors):
        subCategories = [request_list_processor]
        items = [request_list_processor]


class BaseRealEstatePage(
    BasePage, Returns[RealEstate], HasMetadata[RealEstateMetadata]
):
    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]


@attrs.define
class Page(_BasePage, WebPage):
    class Processors(_BasePage.Processors):
        pass

    @field
    def url(self) -> str:
        return str(self.response.url)


class ArticlePage(Page, Returns[Article], HasMetadata[ArticleMetadata]):
    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]


class ArticleListPage(Page, Returns[ArticleList], HasMetadata[ArticleListMetadata]):
    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]


class ArticleNavigationPage(
    Page, Returns[ArticleNavigation], HasMetadata[ArticleNavigationMetadata]
):
    pass


class BusinessPlacePage(
    Page, Returns[BusinessPlace], HasMetadata[BusinessPlaceMetadata]
):
    pass


class JobPostingPage(Page, Returns[JobPosting], HasMetadata[JobPostingMetadata]):
    pass


class ProductPage(
    Page, DescriptionMixin, PriceMixin, Returns[Product], HasMetadata[ProductMetadata]
):
    class Processors(Page.Processors):
        brand = [brand_processor]
        breadcrumbs = [breadcrumbs_processor]
        description = [description_processor]
        descriptionHtml = [description_html_processor]
        price = [price_processor]
        regularPrice = [simple_price_processor]


class ProductListPage(Page, Returns[ProductList], HasMetadata[ProductListMetadata]):
    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]


class ProductNavigationPage(
    Page, Returns[ProductNavigation], HasMetadata[ProductNavigationMetadata]
):
    pass


class RealEstatePage(Page, Returns[RealEstate], HasMetadata[RealEstateMetadata]):
    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]
