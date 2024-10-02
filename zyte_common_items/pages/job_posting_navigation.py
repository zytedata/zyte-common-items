from typing import List, Optional

import attrs
from web_poet import Returns

from zyte_common_items.components import ProbabilityRequest, Request
from zyte_common_items.fields import auto_field
from zyte_common_items.items import JobPostingNavigation, JobPostingNavigationMetadata
from zyte_common_items.processors import probability_request_list_processor

from .base import BasePage, Page
from .mixins import HasMetadata


class BaseJobPostingNavigationPage(
    BasePage, Returns[JobPostingNavigation], HasMetadata[JobPostingNavigationMetadata]
):
    """:class:`BasePage` subclass for :class:`JobPostingNavigation`."""

    class Processors(BasePage.Processors):
        subCategories = [probability_request_list_processor]
        items = [probability_request_list_processor]


class JobPostingNavigationPage(
    Page, Returns[JobPostingNavigation], HasMetadata[JobPostingNavigationMetadata]
):
    """:class:`Page` subclass for :class:`JobPostingNavigation`."""


@attrs.define
class AutoJobPostingNavigationPage(BaseJobPostingNavigationPage):
    job_posting_navigation: JobPostingNavigation

    @auto_field
    def items(self) -> Optional[List[ProbabilityRequest]]:
        return self.job_posting_navigation.items

    @auto_field
    def metadata(self) -> Optional[JobPostingNavigationMetadata]:
        return self.job_posting_navigation.metadata

    @auto_field
    def nextPage(self) -> Optional[Request]:
        return self.job_posting_navigation.nextPage

    @auto_field
    def pageNumber(self) -> Optional[int]:
        return self.job_posting_navigation.pageNumber

    @auto_field
    def url(self) -> Optional[str]:
        return self.job_posting_navigation.url
