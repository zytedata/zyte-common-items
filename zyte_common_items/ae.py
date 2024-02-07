from collections import deque
from typing import List, Optional
from warnings import warn

import attrs
from itemadapter import ItemAdapter as _ItemAdapter

from zyte_common_items import Article, ArticleList, JobPosting, Product, ProductList
from zyte_common_items.adapter import ZyteItemAdapter
from zyte_common_items.base import Item

warn(
    (
        "The zyte_common_items.ae module is a temporary module that helps "
        "speed up migrating from Zyte Automatic Extraction to Zyte API "
        "automatic extraction "
        "(https://docs.zyte.com/zyte-api/migration/zyte/autoextract.html). "
        "However, this module will eventually be removed. Please, update your "
        "code not to depend on this module anymore."
    ),
    DeprecationWarning,
    stacklevel=2,
)


class ItemAdapter(_ItemAdapter):
    ADAPTER_CLASSES = deque([ZyteItemAdapter])


def _convert_details_metadata(data):
    if "metadata" in data:
        _remove(data["metadata"], ["dateDownloaded"])
        if _is_not_none(data["metadata"], "probability"):
            data["probability"] = data["metadata"].pop("probability")
        _remove(data, ["metadata"])
    data.setdefault("probability", 1.0)


def _set_if_truthy(data, field, value):
    if value:
        data[field] = value


def _to_url_list(data, old_k, new_k):
    if _is_truthy_else_remove(data, old_k):
        entries = []
        for entry in data.pop(old_k):
            if _is_truthy(entry, "url"):
                entries.append(entry["url"])
        if entries:
            data[new_k] = entries


@attrs.define(kw_only=True)
class AEBreadcrumb(Item):
    name: Optional[str] = None
    link: Optional[str] = None


def _convert_authors(data):
    if _is_truthy_else_remove(data, "authors"):
        author = None
        author_list = []
        for _author in data.pop("authors") or []:
            if author is None and _is_truthy(_author, "nameRaw"):
                author = _author["nameRaw"]
            if _is_truthy(_author, "name"):
                author_list.append(_author["name"])
        _set_if_truthy(data, "author", author)
        _set_if_truthy(data, "authorList", author_list)


# https://docs.zyte.com/automatic-extraction/article.html#available-fields
@attrs.define(kw_only=True)
class AEArticle(Item):
    headline: Optional[str] = None
    datePublished: Optional[str] = None
    datePublishedRaw: Optional[str] = None
    dateModified: Optional[str] = None
    dateModifiedRaw: Optional[str] = None
    author: Optional[str] = None
    authorsList: List[str] = attrs.Factory(list)
    inLanguage: Optional[str] = None
    breadcrumbs: List[AEBreadcrumb] = attrs.Factory(list)
    mainImage: Optional[str] = None
    images: List[str] = attrs.Factory(list)
    description: Optional[str] = None
    articleBody: Optional[str] = None
    articleBodyHtml: Optional[str] = None
    articleBodyRaw: Optional[str] = None
    videoUrls: List[str] = attrs.Factory(list)
    audioUrls: List[str] = attrs.Factory(list)
    probability: float
    canonicalUrl: Optional[str] = None
    url: str

    @classmethod
    def from_item(cls, item: Item):
        assert isinstance(item, Article)
        data = ItemAdapter(item).asdict()
        _convert_details_metadata(data)
        _convert_authors(data)
        _convert_breadcrumbs(data)
        _convert_images(data)
        _to_url_list(data, "audios", "audioUrls")
        _to_url_list(data, "videos", "videoUrls")
        return super().from_dict(data)


# https://docs.zyte.com/automatic-extraction/article-list.html#individual-articles
@attrs.define(kw_only=True)
class AEArticleFromList(Item):
    headline: Optional[str] = None
    datePublished: Optional[str] = None
    datePublishedRaw: Optional[str] = None
    author: Optional[str] = None
    authorsList: List[str] = attrs.Factory(list)
    inLanguage: Optional[str] = None
    mainImage: Optional[str] = None
    images: List[str] = attrs.Factory(list)
    articleBody: Optional[str] = None
    url: Optional[str] = None
    probability: float


@attrs.define(kw_only=True)
class AEPaginationLink(Item):
    url: Optional[str] = None
    text: Optional[str] = None


def _convert_list_item_metadata(item):
    if _is_truthy_else_remove(item, "metadata"):
        if _is_not_none(item["metadata"], "probability"):
            item["probability"] = item["metadata"].pop("probability")
        del item["metadata"]
    item.setdefault("probability", 1.0)


# https://docs.zyte.com/automatic-extraction/article-list.html#available-fields
@attrs.define(kw_only=True)
class AEArticleList(Item):
    url: str
    articles: List[AEArticleFromList] = attrs.Factory(list)
    paginationNext: Optional[AEPaginationLink] = None
    paginationPrevious: Optional[AEPaginationLink] = None

    @classmethod
    def from_item(cls, item: Item):
        assert isinstance(item, ArticleList)
        data = ItemAdapter(item).asdict()
        if "articles" in data:
            for article in data["articles"]:
                _convert_authors(article)
                _convert_images(article)
                _convert_list_item_metadata(article)
        _remove(data, ["metadata"])
        return super().from_dict(data)


@attrs.define(kw_only=True)
class AELocation(Item):
    raw: Optional[str] = None


@attrs.define(kw_only=True)
class AEOrganization(Item):
    raw: Optional[str] = None


@attrs.define(kw_only=True)
class AESalary(Item):
    raw: Optional[str] = None
    value: Optional[float] = None
    currency: Optional[str] = None


def _rename(data, old_k, new_k):
    if _is_truthy_else_remove(data, old_k):
        data[new_k] = data.pop(old_k)


# https://docs.zyte.com/automatic-extraction/job-posting.html#available-fields
@attrs.define(kw_only=True)
class AEJobPosting(Item):
    title: Optional[str] = None
    datePosted: Optional[str] = None
    validThrough: Optional[str] = None
    description: Optional[str] = None
    descriptionHtml: Optional[str] = None
    employmentType: Optional[str] = None
    hiringOrganization: Optional[AEOrganization] = None
    baseSalary: Optional[AESalary] = None
    jobLocation: Optional[AELocation] = None
    probability: float
    url: str

    @classmethod
    def from_item(cls, item: Item):
        assert isinstance(item, JobPosting)
        data = ItemAdapter(item).asdict()
        _convert_details_metadata(data)
        _remove(data, ["datePublishedRaw"])
        _rename(data, "jobTitle", "title")
        _rename(data, "datePublished", "datePosted")
        if _is_truthy(data, "hiringOrganization"):
            _rename(data["hiringOrganization"], "name", "raw")
        if _is_truthy(data, "baseSalary"):
            _remove(data["baseSalary"], ["currency"])
            if _is_truthy_else_remove(data["baseSalary"], "valueMax"):
                data["baseSalary"]["value"] = float(data["baseSalary"].pop("valueMax"))
            _rename(data["baseSalary"], "currencyRaw", "currency")
        return super().from_dict(data)


@attrs.define(kw_only=True)
class AEAdditionalProperty(Item):
    name: str
    value: Optional[str] = None


@attrs.define(kw_only=True)
class AEGTIN(Item):
    type: str
    value: str


@attrs.define(kw_only=True)
class AEOffer(Item):
    price: Optional[str] = None
    currency: Optional[str] = None
    availability: Optional[str] = None
    regularPrice: Optional[str] = None


@attrs.define(kw_only=True)
class AERating(Item):
    ratingValue: Optional[float] = None
    bestRating: Optional[float] = None
    reviewCount: Optional[int] = None


def _remove(data, fields):
    for field in fields:
        if field in data:
            del data[field]


def _is_truthy(data, field):
    return field in data and data[field]


def _is_truthy_else_remove(data, field):
    if field not in data:
        return False
    if data[field]:
        return True
    else:
        del data[field]
        return False


def _is_not_none(data, field):
    return field in data and data[field] is not None


_OFFER_FIELD_MAP = {
    "price": "price",
    "regularPrice": "regularPrice",
    "availability": "availability",
    "currencyRaw": "currency",
}


def _convert_offer(data):
    offer = {}
    for old_k, new_k in _OFFER_FIELD_MAP.items():
        if _is_not_none(data, old_k):
            offer[new_k] = data.pop(old_k)
    if offer:
        data["offers"] = [offer]


def _convert_images(data):
    if _is_truthy_else_remove(data, "mainImage"):
        main_image = data.pop("mainImage")
        if _is_truthy(main_image, "url"):
            data["mainImage"] = main_image["url"]
    _to_url_list(data, "images", "images")


def _convert_breadcrumbs(data):
    if _is_truthy_else_remove(data, "breadcrumbs"):
        for entry in data["breadcrumbs"]:
            _rename(entry, "link", "url")


# https://docs.zyte.com/automatic-extraction/product.html#available-fields
@attrs.define(kw_only=True)
class AEProduct(Item):
    name: Optional[str] = None
    offers: List[AEOffer] = attrs.Factory(list)
    sku: Optional[str] = None
    mpn: Optional[str] = None
    gtin: List[AEGTIN] = attrs.Factory(list)
    brand: Optional[str] = None
    breadcrumbs: List[AEBreadcrumb] = attrs.Factory(list)
    mainImage: Optional[str] = None
    images: List[str] = attrs.Factory(list)
    description: Optional[str] = None
    descriptionHtml: Optional[str] = None
    aggregateRating: Optional[AERating] = None
    color: Optional[str] = None
    size: Optional[str] = None
    style: Optional[str] = None
    additionalProperty: List[AEAdditionalProperty] = attrs.Factory(list)
    hasVariants: List["AEProduct"] = attrs.Factory(list)
    probability: float
    canonicalUrl: Optional[str] = None
    url: str

    @classmethod
    def from_item(cls, item: Item):
        assert isinstance(item, Product)

        def convert(data):
            _remove(data, ["currency", "features"])
            _convert_details_metadata(data)
            _convert_offer(data)
            if _is_truthy_else_remove(data, "brand"):
                brand = data.pop("brand")
                if _is_truthy(brand, "name"):
                    data["brand"] = brand["name"]
            _convert_breadcrumbs(data)
            _convert_images(data)
            _rename(data, "additionalProperties", "additionalProperty")

        data = ItemAdapter(item).asdict()
        convert(data)
        if _is_truthy_else_remove(data, "variants"):
            for variant in data["variants"]:
                convert(variant)
                for field in ("probability", "url"):
                    if field not in variant:
                        variant[field] = data[field]
            data["hasVariants"] = data.pop("variants")
        return super().from_dict(data)


# https://docs.zyte.com/automatic-extraction/product-list.html#individual-products
@attrs.define(kw_only=True)
class AEProductFromList(Item):
    name: Optional[str] = None
    offers: List[AEOffer] = attrs.Factory(list)
    sku: Optional[str] = None
    brand: Optional[str] = None
    mainImage: Optional[str] = None
    images: List[str] = attrs.Factory(list)
    description: Optional[str] = None
    descriptionHtml: Optional[str] = None
    aggregateRating: Optional[AERating] = None
    probability: float
    url: Optional[str] = None


# https://docs.zyte.com/automatic-extraction/product-list.html#available-fields
@attrs.define(kw_only=True)
class AEProductList(Item):
    url: str
    products: List[AEProductFromList] = attrs.Factory(list)
    breadcrumbs: List[AEBreadcrumb] = attrs.Factory(list)
    paginationNext: Optional[AEPaginationLink] = None
    paginationPrevious: Optional[AEPaginationLink] = None

    @classmethod
    def from_item(cls, item: Item):
        assert isinstance(item, ProductList)
        data = ItemAdapter(item).asdict()
        if "products" in data:
            for product in data["products"]:
                _remove(product, ["currency"])
                _convert_offer(product)
                _convert_images(product)
                if _is_truthy_else_remove(product, "metadata"):
                    if _is_not_none(product["metadata"], "probability"):
                        product["probability"] = product["metadata"].pop("probability")
                    del product["metadata"]
                product.setdefault("probability", 1.0)
        _remove(data, ["metadata", "categoryName"])
        _convert_breadcrumbs(data)
        return super().from_dict(data)


_CONVERSION_MAP = {
    Article: AEArticle,
    ArticleList: AEArticleList,
    JobPosting: AEJobPosting,
    Product: AEProduct,
    ProductList: AEProductList,
}


def downgrade(item: Item) -> Item:
    if item.__class__ not in _CONVERSION_MAP:
        return item
    return _CONVERSION_MAP[item.__class__].from_item(item)  # type: ignore[attr-defined]
