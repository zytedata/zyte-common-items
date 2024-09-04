from typing import List, Optional

import attrs
from web_poet import Returns

from zyte_common_items.fields import auto_field
from zyte_common_items.items import Serp, SerpMetadata, SerpOrganicResult

from .base import BasePage, Page
from .mixins import HasMetadata


class BaseSerpPage(BasePage, Returns[Serp], HasMetadata[SerpMetadata]):
    pass


class SerpPage(Page, Returns[Serp], HasMetadata[SerpMetadata]):
    pass


@attrs.define
class AutoSerpPage(BaseSerpPage):
    serp: Serp

    @auto_field
    def organicResults(self) -> Optional[List[SerpOrganicResult]]:
        return self.serp.organicResults

    @auto_field
    def url(self) -> str:
        return self.serp.url

    @auto_field
    def pageNumber(self) -> Optional[int]:
        return self.serp.pageNumber

    @auto_field
    def metadata(self) -> Optional[SerpMetadata]:
        return self.serp.metadata
