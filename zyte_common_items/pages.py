from datetime import datetime

import attrs
from web_poet import ItemPage, ResponseUrl, Returns, field

from .components import Metadata
from .items import Product, ProductList


@attrs.define
class Page(ItemPage):
    _url: ResponseUrl

    @field
    def metadata(self) -> Metadata:
        return Metadata(
            dateDownloaded=f"{datetime.utcnow().isoformat(timespec='seconds')}Z",
            probability=1.0,
        )

    @field
    def url(self) -> ResponseUrl:
        return self._url


class ProductPage(Page, Returns[Product]):
    pass


class ProductListPage(Page, Returns[ProductList]):
    pass
