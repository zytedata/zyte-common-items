from datetime import datetime

import attrs
from web_poet import ItemPage, RequestUrl, Returns, WebPage, field

from .components import Metadata
from .items import Product, ProductList


class _BaseMixin:
    def _metadata(self) -> Metadata:
        return Metadata(
            dateDownloaded=f"{datetime.utcnow().isoformat(timespec='seconds')}Z",
            probability=1.0,
        )


@attrs.define
class BasePage(_BaseMixin, ItemPage):
    request_url: RequestUrl

    @field
    def url(self) -> str:
        return str(self.request_url)

    @field
    def metadata(self) -> Metadata:
        return self._metadata()


class BaseProductPage(BasePage, Returns[Product]):
    pass


class BaseProductListPage(BasePage, Returns[ProductList]):
    pass


@attrs.define
class Page(_BaseMixin, WebPage):
    @field
    def url(self) -> str:
        return str(self.response.url)

    @field
    def metadata(self) -> Metadata:
        return self._metadata()


class ProductPage(Page, Returns[Product]):
    pass


class ProductListPage(Page, Returns[ProductList]):
    pass
