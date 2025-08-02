from typing import List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import (
    BaseSalary,
    HiringOrganization,
    JobLocation,
    SearchMetadata,
)
from zyte_common_items.converters import to_metadata_optional, url_to_str


@attrs.define(kw_only=True)
class JobPostingMetadata(SearchMetadata):
    """Metadata class for :data:`zyte_common_items.JobPosting.metadata`."""


@attrs.define(kw_only=True)
class JobPosting(Item):
    """A job posting, typically seen on job posting websites or websites of
    companies that are hiring.

    :attr:`url` is the only required attribute.
    """

    url: str = attrs.field(converter=url_to_str)
    """The url of the final response, after any redirects."""

    jobPostingId: Optional[str] = None
    """The identifier of the job posting."""

    datePublished: Optional[str] = None
    """Publication date of the job posting.

    Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"

    With timezone, if available.
    """

    datePublishedRaw: Optional[str] = None
    """Same date as datePublished, but before parsing/normalization, i.e. as it
    appears on the website."""

    dateModified: Optional[str] = None
    """The date when the job posting was most recently modified.

    Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"

    With timezone, if available.
    """

    dateModifiedRaw: Optional[str] = None
    """Same date as dateModified, but before parsing/normalization, i.e. as it
    appears on the website."""

    validThrough: Optional[str] = None
    """The date after which the job posting is not valid, e.g. the end of an
    offer.

    Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"

    With timezone, if available.
    """

    validThroughRaw: Optional[str] = None
    """Same date as validThrough, but before parsing/normalization, i.e. as it
    appears on the website."""

    jobTitle: Optional[str] = None
    """The title of the job posting."""

    headline: Optional[str] = None
    """The headline of the job posting."""

    jobLocation: Optional[JobLocation] = None
    """A (typically single) geographic location associated with the job
    position."""

    description: Optional[str] = None
    """A description of the job posting including sub-headings, with newline
    separators.

    Format:

    - trimmed (no whitespace at the beginning or the end of the description
      string),
    - line breaks included,
    - no length limit,
    - no normalization of Unicode characters.
    """

    descriptionHtml: Optional[str] = None
    """Simplified HTML of the description, including sub-headings, image
    captions and embedded content."""

    employmentType: Optional[str] = None
    """Type of employment (e.g. full-time, part-time, contract, temporary,
    seasonal, internship)."""

    baseSalary: Optional[BaseSalary] = None
    """The base salary of the job or of an employee in the proposed role."""

    requirements: Optional[List[str]] = None
    """Candidate requirements for the job."""

    hiringOrganization: Optional[HiringOrganization] = None
    """Information about the organization offering the job position."""

    jobStartDate: Optional[str] = None
    """Job start date.

    Format: ISO 8601 format: "YYYY-MM-DDThh:mm:ssZ"

    With timezone, if available.
    """

    jobStartDateRaw: Optional[str] = None
    """Same date as jobStartDate, but before parsing/normalization, i.e. as it
    appears on the website."""

    remoteStatus: Optional[str] = None
    """Specifies the remote status of the position."""

    metadata: Optional[JobPostingMetadata] = attrs.field(
        default=None,
        converter=to_metadata_optional(JobPostingMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Contains metadata about the data extraction process."""
