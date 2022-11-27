from datetime import datetime

import attrs
from web_poet import ItemPage, ResponseUrl, Returns, WebPage, field

from .components import Metadata
from .items import Product, ProductList


class _BaseMixin:
    def _get_response_url(self):
        raise NotImplementedError

    @field
    def metadata(self) -> Metadata:
        return Metadata(
            dateDownloaded=f"{datetime.utcnow().isoformat(timespec='seconds')}Z",
            probability=1.0,
        )

    @field
    def url(self) -> str:
        return str(self._get_response_url())


@attrs.define
class BasePage(_BaseMixin, ItemPage):
    _url: ResponseUrl

    def _get_response_url(self):
        return self._url


class BaseProductPage(BasePage, Returns[Product]):
    pass


class BaseProductListPage(BasePage, Returns[ProductList]):
    pass


@attrs.define
class Page(_BaseMixin, WebPage):
    def _get_response_url(self):
        return self.response.url


class ProductPage(Page, Returns[Product]):
    pass


class ProductListPage(Page, Returns[ProductList]):
    pass
