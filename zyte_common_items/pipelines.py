from collections import deque
from typing import List, Optional

import attrs
from itemadapter import ItemAdapter as _ItemAdapter

from zyte_common_items import Product, ProductList
from zyte_common_items.adapter import ZyteItemAdapter
from zyte_common_items.base import Item


class ItemAdapter(_ItemAdapter):
    ADAPTER_CLASSES = deque([ZyteItemAdapter])


@attrs.define(kw_only=True)
class AEAdditionalProperty(Item):
    name: str
    value: Optional[str] = None


@attrs.define(kw_only=True)
class AEBreadcrumb(Item):
    name: Optional[str] = None
    link: Optional[str] = None


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


def _remove_fields(data, fields):
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
    if _is_truthy(data, "images"):
        images = []
        for image in data.pop("images"):
            if _is_truthy(image, "url"):
                images.append(image["url"])
        if images:
            data["images"] = images


def _convert_breadcrumbs(data):
    if _is_truthy_else_remove(data, "breadcrumbs"):
        for entry in data["breadcrumbs"]:
            if _is_truthy_else_remove(entry, "link"):
                entry["url"] = entry.pop("link")


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
        def convert(data):
            _remove_fields(data, ["currency", "features"])
            if "metadata" in data:
                _remove_fields(data["metadata"], ["dateDownloaded"])
                if _is_not_none(data["metadata"], "probability"):
                    data["probability"] = data["metadata"].pop("probability")
                _remove_fields(data, ["metadata"])
            _convert_offer(data)
            if _is_truthy_else_remove(data, "brand"):
                brand = data.pop("brand")
                if _is_truthy(brand, "name"):
                    data["brand"] = brand["name"]
            _convert_breadcrumbs(data)
            _convert_images(data)
            if _is_truthy_else_remove(data, "additionalProperties"):
                data["additionalProperty"] = data.pop("additionalProperties")

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


@attrs.define(kw_only=True)
class AEPaginationLink(Item):
    url: Optional[str] = None
    text: Optional[str] = None


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
        data = ItemAdapter(item).asdict()
        if "products" in data:
            for product in data["products"]:
                _remove_fields(data, ["currency"])
                _convert_offer(product)
                _convert_images(product)
                if _is_truthy_else_remove(product, "metadata"):
                    if _is_not_none(product["metadata"], "probability"):
                        product["probability"] = product["metadata"].pop("probability")
                    del product["metadata"]
                product.setdefault("probability", 1.0)
        _remove_fields(data, ["metadata", "categoryName"])
        _convert_breadcrumbs(data)
        return super().from_dict(data)


_CONVERSION_MAP = {
    Product: AEProduct,
    ProductList: AEProductList,
}


class AEPipeline:
    """Replaces standard items with matching items with the old Zyte Automatic
    Extraction schema.

    See https://docs.zyte.com/zyte-api/migration/zyte/autoextract.html.
    """

    def process_item(self, item, spider):
        if item.__class__ not in _CONVERSION_MAP:
            return item
        return _CONVERSION_MAP[item.__class__].from_item(item)  # type: ignore[attr-defined]
