from typing import List, Optional

import attrs
from web_poet import Returns, field

from zyte_common_items.components import BaseSalary, HiringOrganization, JobLocation
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

    @field
    def url(self) -> Optional[str]:
        return self.job_posting.url

    @field
    def jobPostingId(self) -> Optional[str]:
        return self.job_posting.jobPostingId

    @field
    def datePublished(self) -> Optional[str]:
        return self.job_posting.datePublished

    @field
    def datePublishedRaw(self) -> Optional[str]:
        return self.job_posting.datePublishedRaw

    @field
    def dateModified(self) -> Optional[str]:
        return self.job_posting.dateModified

    @field
    def dateModifiedRaw(self) -> Optional[str]:
        return self.job_posting.dateModifiedRaw

    @field
    def validThrough(self) -> Optional[str]:
        return self.job_posting.validThrough

    @field
    def validThroughRaw(self) -> Optional[str]:
        return self.job_posting.validThroughRaw

    @field
    def jobTitle(self) -> Optional[str]:
        return self.job_posting.jobTitle

    @field
    def headline(self) -> Optional[str]:
        return self.job_posting.headline

    @field
    def jobLocation(self) -> Optional[JobLocation]:
        return self.job_posting.jobLocation

    @field
    def description(self) -> Optional[str]:
        return self.job_posting.description

    @field
    def descriptionHtml(self) -> Optional[str]:
        return self.job_posting.descriptionHtml

    @field
    def employmentType(self) -> Optional[str]:
        return self.job_posting.employmentType

    @field
    def baseSalary(self) -> Optional[BaseSalary]:
        return self.job_posting.baseSalary

    @field
    def requirements(self) -> Optional[List[str]]:
        return self.job_posting.requirements

    @field
    def hiringOrganization(self) -> Optional[HiringOrganization]:
        return self.job_posting.hiringOrganization

    @field
    def jobStartDate(self) -> Optional[str]:
        return self.job_posting.jobStartDate

    @field
    def jobStartDateRaw(self) -> Optional[str]:
        return self.job_posting.jobStartDateRaw

    @field
    def remoteStatus(self) -> Optional[str]:
        return self.job_posting.remoteStatus

    @field
    def metadata(self) -> Optional[JobPostingMetadata]:
        return self.job_posting.metadata
