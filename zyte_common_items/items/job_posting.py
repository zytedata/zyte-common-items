from typing import List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    BaseSalary,
    HiringOrganization,
    JobLocation,
    Metadata,
)
from zyte_common_items.converters import to_metadata_optional, url_to_str


@attrs.define(kw_only=True)
class JobPostingMetadata(Metadata):
    """Metadata class for :data:`zyte_common_items.JobPosting.metadata`."""


@attrs.define(kw_only=True)
class JobPosting(Item):
    """A job posting, typically seen on job posting websites or websites of
    companies that are hiring.

    :attr:`url` is the only required attribute.
    """

    #: The url of the final response, after any redirects.
    url: str = attrs.field(converter=url_to_str)

    #: The identifier of the job posting.
    jobPostingId: Optional[str] = None

    #: Publication date of the job posting.
    #:
    #: Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"
    #:
    #: With timezone, if available.
    datePublished: Optional[str] = None

    #: Same date as datePublished, but before parsing/normalization, i.e. as it appears on the website.
    datePublishedRaw: Optional[str] = None

    #: The date when the job posting was most recently modified.
    #:
    #: Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"
    #:
    #: With timezone, if available.
    dateModified: Optional[str] = None

    #: Same date as dateModified, but before parsing/normalization, i.e. as it appears on the website.
    dateModifiedRaw: Optional[str] = None

    #: The date after which the job posting is not valid, e.g. the end of an offer.
    #:
    #: Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"
    #:
    #: With timezone, if available.
    validThrough: Optional[str] = None

    #: Same date as validThrough, but before parsing/normalization, i.e. as it appears on the website.
    validThroughRaw: Optional[str] = None

    #: The title of the job posting.
    jobTitle: Optional[str] = None

    #: The headline of the job posting.
    headline: Optional[str] = None

    #: A (typically single) geographic location associated with the job position.
    jobLocation: Optional[JobLocation] = None

    #: A description of the job posting including sub-headings, with newline separators.
    #:
    #: Format:
    #:
    #: - trimmed (no whitespace at the beginning or the end of the description string),
    #:
    #: - line breaks included,
    #:
    #: - no length limit,
    #:
    #: - no normalization of Unicode characters.
    description: Optional[str] = None

    #: Simplified HTML of the description, including sub-headings, image captions and embedded content.
    descriptionHtml: Optional[str] = None

    #: Type of employment (e.g. full-time, part-time, contract, temporary, seasonal, internship).
    employmentType: Optional[str] = None

    #: The base salary of the job or of an employee in the proposed role.
    baseSalary: Optional[BaseSalary] = None

    #: Candidate requirements for the job.
    requirements: Optional[List[str]] = None

    #: Information about the organization offering the job position.
    hiringOrganization: Optional[HiringOrganization] = None

    #: Job start date
    #:
    #: Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"
    #:
    #: With timezone, if available.
    jobStartDate: Optional[str] = None

    #: Same date as jobStartDate, but before parsing/normalization, i.e. as it appears on the website.
    jobStartDateRaw: Optional[str] = None

    #: Specifies the remote status of the position.
    remoteStatus: Optional[str] = None

    #: Contains metadata about the data extraction process.
    metadata: Optional[JobPostingMetadata] = attrs.field(
        default=None, converter=to_metadata_optional(JobPostingMetadata), kw_only=True  # type: ignore[misc]
    )
