from typing import Any, Dict, List, Optional

import attrs

from zyte_common_items.base import Item


class CustomAttributesValues(Dict[str, Any]):
    """Container for custom attribute values."""

    pass


@attrs.define
class CustomAttributesMetadata(Item):
    """Custom attribute extraction metadata."""

    error: Optional[str] = None
    inputTokens: Optional[int] = None
    outputTokens: Optional[int] = None
    maxInputTokens: Optional[int] = None
    textInputTokens: Optional[int] = None
    textInputTokensBeforeTruncation: Optional[int] = None
    excludedPIIAttributes: Optional[List[str]] = None
