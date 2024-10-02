from typing import List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import ListMetadata, ProbabilityRequest, Request
from zyte_common_items.converters import (
    to_metadata_optional,
    to_probability_request_list_optional,
    url_to_str,
)


@attrs.define(kw_only=True)
class JobPostingNavigationMetadata(ListMetadata):
    """Metadata class for :data:`zyte_common_items.JobPostingNavigation.metadata`."""


@attrs.define(kw_only=True)
class JobPostingNavigation(Item):
    """Represents the navigational aspects of a job posting listing page on a
    job website."""

    #: Main URL from which the data is extracted.
    url: str = attrs.field(converter=url_to_str)

    #: List of job postings available on this page.
    items: Optional[List[ProbabilityRequest]] = attrs.field(
        default=None, converter=to_probability_request_list_optional, kw_only=True  # type: ignore[misc]
    )

    #: A link to the next page, if available.
    nextPage: Optional[Request] = None

    #: Number of the current page.
    #:
    #: It should only be extracted if the webpage shows a page number.
    #:
    #: It must be 1-based. For example, if the first page of a listing is
    #: numbered as 0 on the website, it should be extracted as `1` nonetheless.
    pageNumber: Optional[int] = None

    #: Data extraction process metadata.
    metadata: Optional[JobPostingNavigationMetadata] = attrs.field(
        default=None, converter=to_metadata_optional(JobPostingNavigationMetadata), kw_only=True  # type: ignore[misc]
    )
