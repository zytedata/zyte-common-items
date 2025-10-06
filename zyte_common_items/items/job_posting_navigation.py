from typing import List, Optional

import attrs

from zyte_common_items.base import Item
from zyte_common_items.components import ListMetadata, ProbabilityRequest, Request
from zyte_common_items.converters import (
    to_metadata_optional,
    to_probability_request_list_optional,
    url_to_str_optional,
)


@attrs.define(kw_only=True)
class JobPostingNavigationMetadata(ListMetadata):
    """Metadata class for :data:`zyte_common_items.JobPostingNavigation.metadata`."""


@attrs.define(kw_only=True)
class JobPostingNavigation(Item):
    """Represents the navigational aspects of a job posting listing page on a
    job website."""

    url: str = attrs.field(converter=url_to_str_optional)
    """Main URL from which the data is extracted."""

    items: Optional[List[ProbabilityRequest]] = attrs.field(
        default=None,
        converter=to_probability_request_list_optional,
        kw_only=True,  # type: ignore[misc]
    )
    """List of job postings available on this page."""

    nextPage: Optional[Request] = None
    """A link to the next page, if available."""

    pageNumber: Optional[int] = None
    """Number of the current page.

    It should only be extracted if the webpage shows a page number.

    It must be 1-based. For example, if the first page of a listing is
    numbered as 0 on the website, it should be extracted as `1` nonetheless.
    """

    metadata: Optional[JobPostingNavigationMetadata] = attrs.field(
        default=None,
        converter=to_metadata_optional(JobPostingNavigationMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Data extraction process metadata."""
