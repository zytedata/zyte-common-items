from typing import Dict, List, Optional

import attrs
from web_poet import ResponseUrl

from zyte_common_items.base import (
    AdditionalProperty,
    AggregateRating,
    Brand,
    Breadcrumb,
    Gtin,
    Image,
    Item,
    Metadata,
)
from zyte_common_items.util import export


@export
@attrs.define(slots=True, kw_only=True)
class _ProductBase(Item):
    additional_properties: Optional[List[AdditionalProperty]] = None
    availability: Optional[str] = None
    canonical_url: Optional[ResponseUrl] = None
    color: Optional[str] = None
    currency: Optional[str] = None
    currency_raw: Optional[str] = None
    gtin: Optional[List[Gtin]] = None
    images: Optional[List[Image]] = None
    main_image: Optional[Image] = None
    mpn: Optional[str] = None
    name: Optional[str] = None
    price: Optional[str] = None
    regular_price: Optional[str] = None
    size: Optional[str] = None
    sku: Optional[str] = None
    style: Optional[str] = None
    url: ResponseUrl = attrs.field(converter=ResponseUrl)


@export
@attrs.define(slots=True, kw_only=True)
class ProductVariant(_ProductBase):
    pass


@export
@attrs.define(slots=True, kw_only=True)
class Product(_ProductBase):
    aggregate_rating: Optional[AggregateRating] = None
    brand: Optional[Brand] = None
    breadcrumbs: Optional[List[Breadcrumb]] = None
    description: Optional[str] = None
    description_html: Optional[str] = None
    features: List[str] = None
    metadata: Metadata
    product_id: Optional[str] = None
    variants: Optional[List[ProductVariant]] = None
