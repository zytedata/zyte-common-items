from datetime import datetime

import attrs
from web_poet import ItemPage, ResponseUrl, Returns, WebPage, field

from .components import Metadata
from .items import Product, ProductList


@attrs.define
class BasePage(ItemPage):
    _url: ResponseUrl

    @field
    def metadata(self) -> Metadata:
        return Metadata(
            dateDownloaded=f"{datetime.utcnow().isoformat(timespec='seconds')}Z",
            probability=1.0,
        )

    @field
    def url(self) -> str:
        return str(self._url)


class BaseProductPage(BasePage, Returns[Product]):
    pass


class BaseProductListPage(BasePage, Returns[ProductList]):
    pass


@attrs.define
class Page(WebPage):
    @field
    def metadata(self) -> Metadata:
        return Metadata(
            dateDownloaded=f"{datetime.utcnow().isoformat(timespec='seconds')}Z",
            probability=1.0,
        )

    @field
    def url(self) -> str:
        return str(self.response.url)


class ProductPage(Page, Returns[Product]):
    pass


class ProductListPage(Page, Returns[ProductList]):
    pass
