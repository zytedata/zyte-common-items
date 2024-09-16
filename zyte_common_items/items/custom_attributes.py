from typing import Any, Dict, List, Optional

import attrs

from zyte_common_items.base import Item


class CustomAttributesValues(Dict[str, Any]):
    """Container for custom attribute values."""

    pass


@attrs.define
class CustomAttributesMetadata(Item):
    """Custom attribute extraction metadata."""

    #: Total number of used input tokens, excluding our internal fixed prompt with the
    #: LLM instruction, when using the "generate" method.
    inputTokens: Optional[int] = None
    #: Total number of used output tokens, when using the "generate" method.
    outputTokens: Optional[int] = None
    #: Total number of input tokens used for the text of the web page, excluding the
    #: schema and our internal fixed prompt with the LLM instruction, when using the
    #: "generate" method. Already included in ``inputTokens``.
    textInputTokens: Optional[int] = None
    #: Maximum number of allowed input tokens for the model, when using the "generate"
    #: method.
    maxInputTokens: Optional[int] = None
    #: ``textInputTokens`` before the text was truncated to fit into the input limits,
    #: either set via ``maxInputTokens`` or due to the model limitation returned in
    #: ``maxInputTokens``, when using the "generate" method.
    textInputTokensBeforeTruncation: Optional[int] = None
    #: A list of all attributes dropped from the output due to a risk of PII
    #: (Personally Identifiable Information) extraction.
    excludedPIIAttributes: Optional[List[str]] = None
    #: * The ``extraction/unparsable-response`` error is given when the LLM response
    #:   could not be parsed or recovered. If this error happens, we suggest
    #:   simplifying the task or reducing the number of attributes.
    #: * The ``extraction/schema-size-exceeded`` error is given when the schema did not
    #:   fit into the input limits, leaving no space for the input text, and therefore
    #:   the LLM could not be used. If this error happens, we suggest either making the
    #:   schema smaller (fewer attributes and/or shorter descriptions), or increasing
    #:   ``maxInputTokens``.
    error: Optional[str] = None


@attrs.define
class CustomAttributes(Item):
    """Extracted custom attribute values and metadata."""

    #: Custom attribute values
    values: CustomAttributesValues

    #: Custom attribute extraction metadata
    metadata: CustomAttributesMetadata
