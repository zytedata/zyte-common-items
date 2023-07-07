from datetime import datetime
from typing import Generic, Type, TypeVar, get_args

import attrs
from web_poet import ItemPage, RequestUrl, Returns, WebPage, field
from web_poet.pages import ItemT

from .components import (
    ArticleListMetadata,
    ArticleMetadata,
    ArticleNavigationMetadata,
    BusinessPlaceMetadata,
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
    Product,
    ProductList,
    ProductNavigation,
    RealEstate,
)
from .processors import breadcrumbs_processor
from .util import format_datetime, metadata_processor

#: Generic type for metadata classes for specific item types.
MetadataT = TypeVar("MetadataT")


def _date_downloaded_now():
    return format_datetime(datetime.utcnow())


class HasMetadata(Generic[MetadataT]):
    """Inherit from this generic mixin to set the metadata class used by a page
    class."""

    @property
    def metadata_cls(self) -> Type[MetadataT]:
        """Metadata class."""
        return _get_metadata_class(self)


def _get_metadata_class(obj):
    for base in getattr(obj.__class__, "__orig_bases__", []):
        origin = getattr(base, "__origin__", None)
        if not origin:
            continue
        if origin != HasMetadata:
            continue
        return get_args(base)[0]
    return None


class _BasePage(ItemPage[ItemT], HasMetadata[MetadataT]):
    class Processors:
        metadata = [metadata_processor]

    @field
    def metadata(self) -> MetadataT:
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


class BaseProductPage(BasePage, Returns[Product], HasMetadata[ProductMetadata]):
    class Processors(BasePage.Processors):
        breadcrumbs = [breadcrumbs_processor]


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


class ProductPage(Page, Returns[Product], HasMetadata[ProductMetadata]):
    class Processors(Page.Processors):
        breadcrumbs = [breadcrumbs_processor]


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
