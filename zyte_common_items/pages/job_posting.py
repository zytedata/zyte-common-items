from typing import List, Optional

import attrs
from web_poet import Returns

from zyte_common_items.components import BaseSalary, HiringOrganization, JobLocation
from zyte_common_items.fields import auto_field
from zyte_common_items.items import JobPosting, JobPostingMetadata
from zyte_common_items.processors import (
    description_html_processor,
    description_processor,
)

from .base import BasePage, Page
from .mixins import DescriptionMixin, HasMetadata


class BaseJobPostingPage(
    BasePage, DescriptionMixin, Returns[JobPosting], HasMetadata[JobPostingMetadata]
):
    """:class:`BasePage` subclass for :class:`JobPosting`."""

    class Processors(BasePage.Processors):
        description = [description_processor]
        descriptionHtml = [description_html_processor]


class JobPostingPage(
    Page, DescriptionMixin, Returns[JobPosting], HasMetadata[JobPostingMetadata]
):
    """:class:`Page` subclass for :class:`JobPosting`."""

    class Processors(Page.Processors):
        description = [description_processor]
        descriptionHtml = [description_html_processor]


@attrs.define
class AutoJobPostingPage(BaseJobPostingPage):
    job_posting: JobPosting

    @auto_field
    def url(self) -> Optional[str]:
        return self.job_posting.url

    @auto_field
    def jobPostingId(self) -> Optional[str]:
        return self.job_posting.jobPostingId

    @auto_field
    def datePublished(self) -> Optional[str]:
        return self.job_posting.datePublished

    @auto_field
    def datePublishedRaw(self) -> Optional[str]:
        return self.job_posting.datePublishedRaw

    @auto_field
    def dateModified(self) -> Optional[str]:
        return self.job_posting.dateModified

    @auto_field
    def dateModifiedRaw(self) -> Optional[str]:
        return self.job_posting.dateModifiedRaw

    @auto_field
    def validThrough(self) -> Optional[str]:
        return self.job_posting.validThrough

    @auto_field
    def validThroughRaw(self) -> Optional[str]:
        return self.job_posting.validThroughRaw

    @auto_field
    def jobTitle(self) -> Optional[str]:
        return self.job_posting.jobTitle

    @auto_field
    def headline(self) -> Optional[str]:
        return self.job_posting.headline

    @auto_field
    def jobLocation(self) -> Optional[JobLocation]:
        return self.job_posting.jobLocation

    @auto_field
    def description(self) -> Optional[str]:
        return self.job_posting.description

    @auto_field
    def descriptionHtml(self) -> Optional[str]:
        return self.job_posting.descriptionHtml

    @auto_field
    def employmentType(self) -> Optional[str]:
        return self.job_posting.employmentType

    @auto_field
    def baseSalary(self) -> Optional[BaseSalary]:
        return self.job_posting.baseSalary

    @auto_field
    def requirements(self) -> Optional[List[str]]:
        return self.job_posting.requirements

    @auto_field
    def hiringOrganization(self) -> Optional[HiringOrganization]:
        return self.job_posting.hiringOrganization

    @auto_field
    def jobStartDate(self) -> Optional[str]:
        return self.job_posting.jobStartDate

    @auto_field
    def jobStartDateRaw(self) -> Optional[str]:
        return self.job_posting.jobStartDateRaw

    @auto_field
    def remoteStatus(self) -> Optional[str]:
        return self.job_posting.remoteStatus

    @auto_field
    def metadata(self) -> Optional[JobPostingMetadata]:
        return self.job_posting.metadata
