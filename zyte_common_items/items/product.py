from __future__ import annotations

from typing import Optional

import attrs

from zyte_common_items._examples import (
    _BREADCRUMBS_EXAMPLE_1,
    _BREADCRUMBS_EXAMPLE_2,
    _DESCRIPTION_HTML_EXAMPLE,
    _GTIN_EXAMPLE_1,
    _GTIN_EXAMPLE_2,
    _GTIN_EXAMPLE_3,
)
from zyte_common_items.base import Item
from zyte_common_items.components import (
    AdditionalProperty,
    AggregateRating,
    Brand,
    Breadcrumb,
    DetailsMetadata,
    Gtin,
    Image,
)
from zyte_common_items.converters import (
    to_metadata_optional,
    url_to_str,
    url_to_str_optional,
)


@attrs.define(kw_only=True)
class ProductMetadata(DetailsMetadata):
    """Metadata class for :data:`zyte_common_items.Product.metadata`."""


@attrs.define(kw_only=True)
class Product(Item):
    """Product from an e-commerce website.

    :attr:`url` is the only required attribute.
    """

    additionalProperties: Optional[list[AdditionalProperty]] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmHint": (
                    "There should never be an empty or null key or value. If "
                    "the name or the value is not explicitly provided in the "
                    "HTML structure, it is not considered an "
                    "additional property.\n"
                    "\n"
                    "Only extract additional properties from HTML elements "
                    "that contain mostly key/value specifications, i.e. have "
                    "several elements in a distinguishable key/value form, or "
                    "as a table with a column for the key and a column for "
                    "the value. So, if there's a list where most elements are "
                    "not in key/value form, but a few are, you won't cherry "
                    "pick these elements as additional properties. In other "
                    "words, you will extract additional properties if many "
                    "elements are in key/value form in a common parent in the "
                    "HTML."
                ),
            },
        },
    )
    """List of name-value pairs of product data.

    Additional properties usually appear in product pages in the form of a
    specification table or a free-form specification list that can be easily
    turned into key-value pairs, where keys indicate the name of a property and
    values indicate the value of that property.

    Additional properties that require 1 or more extra requests may not be
    extracted.

    See also ``features``.
    """

    aggregateRating: Optional[AggregateRating] = None
    """Aggregate data about reviews and ratings."""

    availability: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmHint": "For node selection, try to find the nodes of the HTML that indicate a positive or negative availability of the product.",
            }
        },
    )
    """Product availability status.

    The value is expected to be one of: ``"InStock"``, ``"OutOfStock"``.
    """

    brand: Optional[Brand] = None
    """Brand or manufacturer of the product."""

    breadcrumbs: Optional[list[Breadcrumb]] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmHint": (
                    f"Always prioritize the list of breadcrumbs that is more "
                    f"complete, i.e. the one with higher number of elements "
                    f"that details all the levels/categories of the product.\n"
                    f"\n"
                    f"# Recommendations on How to Extract Breadcrumbs\n"
                    f"\n"
                    f"## Recommended Approach\n"
                    f"\n"
                    f"You should try to use "
                    f"`zyte_parsers.breadcrumbs.extract_breadcrumbs`, as it "
                    f"provides a standardized approach for identifying, "
                    f"cleaning, and structuring breadcrumb navigation data "
                    f"from various HTML inputs.\n"
                    f"\n"
                    f"However, if you need to implement a custom extraction "
                    f"method, you are allowed to not use the provided "
                    f"function. Explain why you decide to use or not use the "
                    f"function in your explanation.\n"
                    f"\n"
                    f"---\n"
                    f"\n"
                    f"## What It Can Extract\n"
                    f"\n"
                    f"The `extract_breadcrumbs` function extracts the "
                    f"following breadcrumb elements:\n"
                    f"\n"
                    f"1. **Clickable Breadcrumb Items**\n"
                    f"   - Detects `<a>` elements that typically contain the "
                    f"breadcrumb link along with their associated text.\n"
                    f"\n"
                    f"2. **Textual Breadcrumb Items**\n"
                    f"   - It can extract breadcrumb names from plain text "
                    f"nodes, even when they are not wrapped in a link.\n"
                    f"\n"
                    f"3. **Compound Breadcrumbs from Single Nodes**\n"
                    f"   - In cases where a single element contains multiple "
                    f"breadcrumb names separated by common delimiters, the "
                    f"function splits them into separate items.\n"
                    f"\n"
                    f"---\n"
                    f"\n"
                    f"## What It Can't Extract / Limitations\n"
                    f"\n"
                    f"1. **Non-Standard Breadcrumb Structures**\n"
                    f"   - If the breadcrumb navigation does not follow "
                    f"typical HTML patterns (for example, if it relies "
                    f"heavily on JavaScript rendering or uses unconventional "
                    f"elements), the extraction may fail or be incomplete.\n"
                    f"\n"
                    f"2. **Deeply Nested Breadcrumbs**\n"
                    f"   - The extraction is performed with a configurable "
                    f"maximum search depth (default is 10). Breadcrumb items "
                    f"nested deeper than this limit might be missed.\n"
                    f"\n"
                    f"3. **Custom Separators**\n"
                    f"   - The function depends on a predefined set of "
                    f"separator characters. If a site uses custom or unusual "
                    f"delimiters, the splitting logic may not work as "
                    f"expected.\n"
                    f"\n"
                    f"4. **Dropdown Menus and Complex Markup**\n"
                    f"   - Breadcrumbs embedded in dynamic dropdowns or "
                    f"elements with complex class attributes (e.g., those "
                    f"related to dropdown menus) may be intentionally skipped "
                    f"to avoid incorrect extractions.\n"
                    f"\n"
                    f"---\n"
                    f"\n"
                    f"## Examples\n"
                    f"\n"
                    f"### Example 1\n"
                    f"\n"
                    f"{_BREADCRUMBS_EXAMPLE_1}\n"
                    f"\n"
                    f"### Example 2\n"
                    f"\n"
                    f"{_BREADCRUMBS_EXAMPLE_2}"
                ),
            }
        },
    )
    """Webpage `breadcrumb trail`_.

    .. _Breadcrumb trail: https://en.wikipedia.org/wiki/Breadcrumb_navigation
    """

    canonicalUrl: Optional[str] = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
    """Canonical form of the URL, as indicated by the website.

    See also ``url``.
    """

    color: Optional[str] = None
    """Color of the product.

    It is extracted as displayed (e.g. ``"white"``).

    See also: ``size``, ``style``.
    """

    currency: Optional[str] = None
    """Price currency `ISO 4217`_ alphabetic code (e.g. ``"USD"``).

    See also ``currencyRaw``.

    .. _ISO 4217: https://en.wikipedia.org/wiki/ISO_4217
    """

    currencyRaw: Optional[str] = None
    """Price currency as it appears on the webpage (no post-processing).

    This is usually the currency that appears next to the price visually on the
    webpage. It is commonly a symbol but can also appear normalized already
    next to the price. For example, both "$" and "USD" are possible values.

    Non-currencies, such as ``"-"``, should not be extracted as currencyRaw.

    See also ``currency``.
    """

    description: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmHint": (
                    "You MUST use the method `extract_text` from the "
                    "`html_text` library to extract this value."
                ),
            }
        },
    )
    """Plain-text, complete product description.

    If the description is split across different parts of the source webpage,
    only the main part, containing the most useful pieces of information,
    should be extracted into this attribute.

    It may contain data found in other attributes (``features``,
    ``additionalProperties``).

    Format-wise:

    -   Line breaks and non-ASCII characters are allowed.
    -   There is no length limit for this attribute, the content should not be
        truncated.
    -   There should be no whitespace at the beginning or end.

    See also ``descriptionHtml``.
    """

    descriptionHtml: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmHint": (
                    f"The output of this field should be HTML, so the HTML of "
                    f"the description, not just the description.\n"
                    f"\n"
                    f"The HTML should always be the outer HTML of the node, "
                    f"and I expect the output of this field to start with "
                    f"some HTML tags, and end with the same tags.\n"
                    f"\n"
                    f"The HTML should be valid, so it should not contain any "
                    f"unclosed tags, etc.\n"
                    f"\n"
                    f"# Recommendations on How to Extract HTML\n"
                    f"\n"
                    f"It is strongly recommended to use `clear_html` to "
                    f"extract the HTML. This library provides a standardized "
                    f"way to clean and normalize HTML documents. It removes "
                    f"unwanted elements while preserving essential content "
                    f"and embeddings, making it easier to extract meaningful "
                    f"text or clean HTML markup for further processing.\n"
                    f"\n"
                    f"## What It's Used For\n"
                    f"\n"
                    f"- **HTML Cleaning**: Normalize and clean HTML trees by "
                    f"removing inline styles, unnecessary tags (e.g., "
                    f"`<figcaption>`), and extraneous attributes.\n"
                    f"- **Embeddings Preservation**: Preserve specific HTML "
                    f"embeddings through a whitelist.\n"
                    f"- **Output Conversion**: Generate clean HTML or plain "
                    f"text from processed HTML nodes.\n"
                    f"\n"
                    f"Important note: `clear_html` already wraps the HTML in "
                    f"`<article>` tags, so you shouldn't really add this with "
                    f"code.\n"
                    f"\n"
                    f"---\n"
                    f"\n"
                    f"## Example\n"
                    f"\n"
                    f"{_DESCRIPTION_HTML_EXAMPLE}"
                ),
            }
        },
    )
    """HTML containing the complete product description.

    See ``description`` for extraction details.

    The format is not the raw HTML from the source webpage. See the `HTML
    normalization specification`_ for details.

    .. _HTML normalization specification: https://docs.zyte.com/automatic-extraction/article.html#format-of-articlebodyhtml-field
    """

    features: Optional[list[str]] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmHint": (
                    "Features can generally be found arranged in a list. Each "
                    "of the features are usually each in a single element or "
                    "bullet point.\n"
                    "\n"
                    "The list is usually bulleted, but not necessarily.\n"
                    "\n"
                    "The extracted features should appear in the page in a "
                    "way that are easily parseable with code, so elements "
                    "from e.g. free text or descriptions that would need "
                    "semantic understanding or very complex parsing are not "
                    "considered these features.\n"
                    "\n"
                    "Always extract the features, even if they appear or "
                    "they would be in other product fields, as long as they "
                    "are systematically shown in the page as described (e.g. "
                    "as elements in a list, structured, etc.), so it does not "
                    "matter if they are already extracted in other product "
                    "fields."
                ),
            }
        },
    )
    """List of product features.

    They are usually listed as bullet points in product webpages.

    See also ``additionalProperties``.
    """

    gtin: Optional[list[Gtin]] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmHint": (
                    f"# Recommendations on How to Extract GTIN\n"
                    f"\n"
                    f"It is recommended to use "
                    f"`zyte_parsers.gtin.extract_gtin` for extracting and "
                    f"validating GTIN identifiers. This function provides a "
                    f"standardized approach for identifying, cleaning, and "
                    f"validating GTINs within text-based inputs.\n"
                    f"\n"
                    f"## What It Can Extract\n"
                    f"\n"
                    f"The `extract_gtin` function extracts and validates the "
                    f"following types of identifiers:\n"
                    f"\n"
                    f"- **ISBN10 and ISBN13** \u2013 for books and "
                    f"publications.\n"
                    f"- **ISSN** \u2013 for periodicals.\n"
                    f"- **ISMN** \u2013 for printed music.\n"
                    f"- **UPC** \u2013 a 12-digit code used in retail.\n"
                    f"- **GTIN8, GTIN13, GTIN14** \u2013 common formats for "
                    f"product identification.\n"
                    f"- **EAN13** \u2013 recognized via the same mechanisms "
                    f"as ISBN13 or GTIN13.\n"
                    f"\n"
                    f"The function automatically cleans the input (removing "
                    f'extraneous characters and known prefixes like "ISBN13") '
                    f"and uses libraries (such as `stdnum` and "
                    f"`gtin.validator`) to validate and classify the "
                    f"identifier.\n"
                    f"\n"
                    f"## What It Can't Extract / Limitations\n"
                    f"\n"
                    f"- **Non-numeric or mixed codes**: If a candidate code "
                    f"includes letters interleaved with digits or is "
                    f"formatted in an unexpected way, it might be rejected.\n"
                    f"- **Multiple codes**: The function is designed to "
                    f"extract a single GTIN from the input. If the text "
                    f"contains several codes, it will only return one "
                    f"(typically the first valid extraction).\n"
                    f"- **Malformed or incomplete identifiers**: Codes that "
                    f"do not pass the validation rules (for instance, due to "
                    f"incorrect check digits or wrong length) will not be "
                    f"recognized.\n"
                    f"- **Alphanumeric SKUs**: Some SKU values that look like "
                    f"GTINs but include letters in between numbers may be "
                    f"discarded to avoid false positives.\n"
                    f"\n"
                    f"---\n"
                    f"\n"
                    f"# Examples\n"
                    f"\n"
                    f"## Example 1\n"
                    f"\n"
                    f"{_GTIN_EXAMPLE_1}\n"
                    f"\n"
                    f"## Example 2\n"
                    f"\n"
                    f"{_GTIN_EXAMPLE_2}\n"
                    f"\n"
                    f"## Example 3\n"
                    f"\n"
                    f"{_GTIN_EXAMPLE_3}"
                ),
            }
        },
    )
    """List of standardized GTIN_ product identifiers associated with the
    product, which are unique for the product across different sellers.

    See also: ``mpn``, ``productId``, ``sku``.

    .. _GTIN: https://en.wikipedia.org/wiki/Global_Trade_Item_Number
    """

    images: Optional[list[Image]] = None
    """All product images.

    The main image (see ``mainImage``) should be first in the list.

    Images only displayed as part of the product description are excluded.
    """

    mainImage: Optional[Image] = None
    """Main image of the product."""

    metadata: Optional[ProductMetadata] = attrs.field(
        default=None,
        converter=to_metadata_optional(ProductMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Data extraction process metadata."""

    mpn: Optional[str] = None
    """`Manufacturer part number (MPN)`_ of the product.

    The MPN is issued by the manufacturer, so a product should have the same
    MPN across different e-commerce websites.

    See also: ``gtin``, ``productId``, ``sku``.

    .. _Manufacturer part number (MPN): https://en.wikipedia.org/wiki/Part_number
    """

    name: Optional[str] = None
    """Product name as it appears on the webpage (no post-processing)."""

    price: Optional[str] = None
    """Price at which the product is being offered at the moment.

    It must be formatted with a full stop as decimal separator and no thousands
    separator or currency, e.g. ``"10500.99"``.

    If there are any discounts, this is the price with discounts applied.

    If the price is indicated with and without value-added tax (VAT), this
    is the price *with* VAT.

    See also: ``regularPrice``, ``currency``, ``currencyRaw``.
    """

    productId: Optional[str] = None
    """Product identifier, unique within an e-commerce website.

    It may come in the form of an SKU or any other identifier, a hash, or even
    a URL.

    See also: ``gtin``, ``mpn``, ``sku``.
    """

    regularPrice: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmHint": (
                    "If you would extract a regularPrice that is equal or "
                    "higher than `price`, extract `regularPrice` as `None` "
                    "instead.\n"
                    "\n"
                    "The final extracted string should not contain the currency code, currency denomination, or currency symbol -- just the price value itself.\n\nFormat:\n- no thousands separator,\n- full stop as decimal separator.\n- if page shows no decimals, extract with two decimals, e.g. XY.00"
                ),
            }
        },
    )
    """Price shown on the webpage as a price at which the product has been
    offered in the past by the same retailer, presented as a reference next to
    the current price.

    It may be labeled as the original price, the price before discount, the
    list price, or the maximum retail price for which the product is sold.

    It must be formatted with a full stop as decimal separator and no thousands
    separator or currency, e.g. ``"15000.99"``.

    ``regularPrice`` must be ``None`` if ``price`` is ``None``. If not
    ``None``, ``regularPrice`` must be higher than ``price``.

    If ``price`` is extracted with value-added tax (VAT), ``regularPrice`` must
    be extracted with VAT. If ``price`` is extracted without VAT,
    ``regularPrice`` must be extracted without VAT.

    See also: ``price``, ``currency``, ``currencyRaw``.
    """

    size: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmHint": (
                    "By order of preference (higher priority at the top), the "
                    "size you will select will be:\n"
                    "\n"
                    "- The one indicated by the default selected variant "
                    "(e.g. size picker button or dropdown)\n"
                    "- The one that holds the most specific size information "
                    '(e.g. "750x450x800" is more specific than "Large").\n'
                    "- The one that clarifies better the dimensions (e.g. "
                    '"45H x 30W x 20D" is more clarifying than "45x30x20").\n'
                    "- The most obvious one (e.g. introduced by a label like "
                    '"Size", "Dimensions", etc.).\n'
                    "\n"
                    "Generally, unless you really need to, you will not parse "
                    "the size information from the name of the product. E.g. "
                    'if there is a product whose name is "Large Stove", you '
                    'will consider "Large" here parsed from the name **as a '
                    "very last resort** to extract the size information, and "
                    "only if you cannot find any other size information in "
                    "the page."
                ),
            }
        },
    )
    """Size, dimensions or volume of the product.

    It is extracted as displayed (e.g. ``"XL"``, ``"32Wx34L"``, ``"Large"``,
    ``"750x450x800"``, ``"10m"``, ``"Height: 48cm - 86cm, Width: 204cm, Depth:
    93cm"``).

    See also: ``color``, ``style``.
    """

    sku: Optional[str] = None
    """`Stock keeping unit (SKU)`_ identifier, i.e. a merchant-specific product
    identifier.

    See also: ``gtin``, ``mpn``, ``productId``.

    .. _Stock keeping unit (SKU): https://en.wikipedia.org/wiki/Stock_keeping_unit
    """

    style: Optional[str] = None
    """Style, pattern or finish of the product.

    It is extracted as displayed (e.g. ``"polka dots"``, ``"Striped"``,
    ``"Nickel finish with Translucent glass"``).

    See also: ``color``, ``size``.
    """

    url: str = attrs.field(converter=url_to_str)
    """Main URL from which the data has been extracted.

    See also ``canonicalUrl``.
    """

    variants: Optional[list[ProductVariant]] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmHint": (
                    "The different variants of the product are usually "
                    "selectable as interactive elements on the product page, "
                    "like buttons, dropdowns or radio buttons, and they "
                    "usually (but not always) come in lists within sections.\n"
                    "\n"
                    "Variants must have at least one non-null field, and "
                    "their fields must never be empty strings.\n"
                    "\n"
                    "Another important detail: Just combining attributes "
                    "(e.g. color and size) is not enough to determine a "
                    "variant, because certain combinations may not exist.\n"
                    "\n"
                    "Most of the time, the needed info for the page to change "
                    "the HTML when a variant is pressed (and shows then the "
                    "actual existing variant) is in the HTML, but not always. "
                    "So you should try to extract the variant information "
                    "from the HTML, and if you cannot find it, then you can "
                    "combine variant attributes blindly, but always try to "
                    "extract the variant information from the scripts or "
                    "doing some AJAX requests, as e.g. a particular color "
                    "does not have a particular size, but this is only shown "
                    "in the HTML when the variant is selected."
                ),
            }
        },
    )
    """List of product variants.

    When slightly different versions of a product are displayed on the same
    product page, allowing you to choose a specific product version from a
    selection, each of those product versions are considered a product variant.

    Product variants usually differ in ``color`` or ``size``.

    The following items are *not* considered product variants:

    -   Other products.

    -   Recommended products.

    -   Different products within the same bundle of products.

    -   Product add-ons, e.g. premium upgrades of a base product.

    If only one “variant” is shown in the page, it is not considered a product
    variant.

    Only variant-specific data is extracted as product variant details. For
    example, if variant-specific versions of the product description do not
    exist in the source webpage, the description attributes of the product
    variant are *not* filled with the base product description.

    Extracted product variants may not include those that are not visible in
    the source webpage.

    Product variant details may not include those that require multiple
    additional requests (e.g. 1 or more requests per variant).

    There must not be duplicate variants.
    """


@attrs.define(kw_only=True)
class ProductVariant(Item):
    """:class:`Product` variant.

    See :attr:`Product.variants`, :class:`ProductVariantExtractor`,
    :class:`ProductVariantSelectorExtractor`.
    """

    additionalProperties: Optional[list[AdditionalProperty]] = None
    """List of name-value pais of data about a specific, otherwise unmapped
    feature.

    Additional properties usually appear in product pages in the form of a
    specification table or a free-form specification list.

    Additional properties that require 1 or more extra requests may not be
    extracted.

    See also ``features``.
    """

    availability: Optional[str] = None
    """Availability status.

    The value is expected to be one of: ``"InStock"``, ``"OutOfStock"``.
    """

    canonicalUrl: Optional[str] = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
    """Canonical form of the URL, as indicated by the website.

    See also ``url``.
    """

    color: Optional[str] = None
    """Color.

    It is extracted as displayed (e.g. ``"white"``).

    See also: ``size``, ``style``.
    """

    currency: Optional[str] = None
    """Price currency `ISO 4217`_ alphabetic code (e.g. ``"USD"``).

    See also ``currencyRaw``.

    .. _ISO 4217: https://en.wikipedia.org/wiki/ISO_4217
    """

    currencyRaw: Optional[str] = None
    """Price currency as it appears on the webpage (no post-processing), e.g.
    ``"$"``.

    See also ``currency``.
    """

    gtin: Optional[list[Gtin]] = None
    """List of standardized GTIN_ product identifiers associated with the
    product, which are unique for the product across different sellers.

    See also: ``mpn``, ``productId``, ``sku``.

    .. _GTIN: https://en.wikipedia.org/wiki/Global_Trade_Item_Number
    """

    images: Optional[list[Image]] = None
    """All product images.

    The main image (see ``mainImage``) should be first in the list.

    Images only displayed as part of the product description are excluded.
    """

    mainImage: Optional[Image] = None
    """Main product image."""

    mpn: Optional[str] = None
    """`Manufacturer part number (MPN)`_.

    A product should have the same MPN across different e-commerce websites.

    See also: ``gtin``, ``productId``, ``sku``.

    .. _Manufacturer part number (MPN): https://en.wikipedia.org/wiki/Part_number
    """

    name: Optional[str] = None
    """Name as it appears on the webpage (no post-processing)."""

    price: Optional[str] = None
    """Price at which the product is being offered.

    It is a string with the price amount, with a full stop as decimal
    separator, and no thousands separator or currency (see ``currency`` and
    ``currencyRaw``), e.g. ``"10500.99"``.

    If ``regularPrice`` is not ``None``, ``price`` should always be lower than
    ``regularPrice``.
    """

    productId: Optional[str] = None
    """Product identifier, unique within an e-commerce website.

    It may come in the form of an SKU or any other identifier, a hash, or even
    a URL.

    See also: ``gtin``, ``mpn``, ``sku``.
    """

    regularPrice: Optional[str] = None
    """Price at which the product was being offered in the past, and which is
    presented as a reference next to the current price.

    It may be labeled as the original price, the list price, or the maximum
    retail price for which the product is sold.

    See ``price`` for format details.

    If ``regularPrice`` is not ``None``, it should always be higher than
    ``price``.
    """

    size: Optional[str] = None
    """Size or dimensions.

    Pertinent to products such as garments, shoes, accessories, etc.

    It is extracted as displayed (e.g. ``"XL"``).

    See also: ``color``, ``style``.
    """

    sku: Optional[str] = None
    """`Stock keeping unit (SKU)`_ identifier, i.e. a merchant-specific product
    identifier.

    See also: ``gtin``, ``mpn``, ``productId``.

    .. _Stock keeping unit (SKU): https://en.wikipedia.org/wiki/Stock_keeping_unit
    """

    style: Optional[str] = None
    """Style.

    Pertinent to products such as garments, shoes, accessories, etc.

    It is extracted as displayed (e.g. ``"polka dots"``).

    See also: ``color``, ``size``.
    """

    url: Optional[str] = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
    """Main URL from which the product variant data could be extracted."""
