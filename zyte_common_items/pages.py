from datetime import datetime

import attrs
from web_poet import ItemPage, RequestUrl, Returns, WebPage, field
from web_poet.fields import FieldsMixin

from .components import Metadata
from .items import BusinessPlace, Product, ProductList


class _BaseMixin(FieldsMixin):
    @field
    def metadata(self) -> Metadata:
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


class BaseProductPage(BasePage, Returns[Product]):
    pass


class BaseProductListPage(BasePage, Returns[ProductList]):
    pass


class BaseBusinessPlacePage(BasePage, Returns[BusinessPlace]):
    pass


@attrs.define
class Page(_BaseMixin, WebPage):
    @field
    def url(self) -> str:
        return str(self.response.url)


class ProductPage(Page, Returns[Product]):
    pass


class ProductListPage(Page, Returns[ProductList]):
    pass


class BusinessPlacePage(Page, Returns[BusinessPlace]):
    pass
