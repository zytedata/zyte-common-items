from typing import List, Optional

import attrs
from itemadapter import ItemAdapter

from zyte_common_items import Product
from zyte_common_items.base import Item


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


@attrs.define(kw_only=True)
class AEProduct(Item):
    url: Optional[str] = None
    canonicalUrl: Optional[str] = None
    probability: Optional[float] = None
    name: Optional[str] = None
    offers: List[AEOffer] = attrs.Factory(list)
    sku: Optional[str] = None
    gtin: List[AEGTIN] = attrs.Factory(list)
    mpn: Optional[str] = None
    brand: Optional[str] = None
    breadcrumbs: List[AEBreadcrumb] = attrs.Factory(list)
    mainImage: Optional[str] = None
    images: List[str] = attrs.Factory(list)
    description: Optional[str] = None
    descriptionHtml: Optional[str] = None
    additionalProperty: List[AEAdditionalProperty] = attrs.Factory(list)
    aggregateRating: Optional[AERating] = None
    color: Optional[str] = None
    size: Optional[str] = None
    style: Optional[str] = None

    @classmethod
    def from_item(cls, item: Item):
        data = ItemAdapter(item).asdict()
        if "currency" in data:
            del data["currency"]
        if "features" in data:
            del data["features"]
        if "metadata" in data:
            if "dateDownloaded" in data["metadata"]:
                del data["metadata"]["dateDownloaded"]
            if "probability" in data["metadata"]:
                data["probability"] = data["metadata"].pop("probability")
            if not data["metadata"]:
                del data["metadata"]
        offer_fields = {
            "price": "price",
            "regularPrice": "regularPrice",
            "availability": "availability",
            "currencyRaw": "currency",
        }
        if any(k in data for k in offer_fields):
            offer = {}
            for old_k, new_k in offer_fields.items():
                if old_k in data:
                    offer[new_k] = data.pop(old_k)
            data["offers"] = [offer]
        if "brand" in data:
            brand = data.pop("brand")
            if "name" in brand:
                data["brand"] = brand["name"]
        if "breadcrumbs" in data:
            for entry in data["breadcrumbs"]:
                if "link" in entry:
                    entry["url"] = entry.pop("link")
        if "mainImage" in data:
            main_image = data.pop("mainImage")
            if "url" in main_image:
                data["mainImage"] = main_image["url"]
        if "images" in data:
            images = []
            for image in data.pop("images"):
                if "url" in image:
                    images.append(image["url"])
            if images:
                data["images"] = images
        if "additionalProperties" in data:
            data["additionalProperty"] = data.pop("additionalProperties")
        return super().from_dict(data)


_CONVERSION_MAP = {
    Product: AEProduct,
}


class AEPipeline:
    """Replaces standard items with matching items with the old Zyte Automatic
    Extraction schema.

    See https://docs.zyte.com/zyte-api/migration/zyte/autoextract.html.
    """

    def process_item(self, item, spider):
        if item.__class__ not in _CONVERSION_MAP:
            return item
        return _CONVERSION_MAP[item.__class__].from_item(item)
