from typing import Optional

import attrs


@attrs.define(kw_only=True)
class SerpOrganicResult:
    """Data from a non-paid result of a search engine results page."""

    #: Result excerpt.
    description: Optional[str] = None

    #: Result title.
    name: Optional[str] = None

    #: Result URL.
    url: Optional[str] = None

    #: Result position among other organic results from the same search engine
    #: results page.
    #:
    #: This is the rank within a specific page, not within an entire search.
    #: That is, the first result of any page, even if it not the first page of
    #: a search, must be 1.
    rank: Optional[int] = None
