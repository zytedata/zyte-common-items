from __future__ import annotations

from typing import List, Optional

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

    additionalProperties: Optional[List[AdditionalProperty]] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": (
                    "A list of name-value pair fields holding information pertaining to specific features. "
                    "Usually in a form of a specification table or freeform specification list, but in a way "
                    "that most if not all of the elements can be separated clearly into key/value pairs.\n\n"
                    "These fields are usually found in key/value pairs in sections or HTML elements with several of them, "
                    "where each element specifies attributes and characteristics of the product in a clear key/value format.\n\n"
                    "Another way these can be found is in tables, with a corresponding column for the name of the property (key) "
                    "and another column for the value of the property. What we try to capture here are the properties of the product "
                    "that are not extracted in the rest of the schema, but even if the properties appear in the rest of the schema, "
                    "extract them anyway as additionalProperties if they are clearly shown as key/value pairs, i.e. extract them even "
                    "if they'd be handled by other fields.\n\n"
                    "Always preserve all the properties that are presented in this way in the page. There should never be an empty or "
                    "null key (name of the property) or value.\n\n"
                    "Generally speaking, the additional properties will usually come in a list whose elements are mostly key/value "
                    "specifications, i.e. has several elements in a distinguishable key/value form, or as a table with a column for "
                    "the key and a column for the value. So, if there's a list whose majority of elements are not in key/value form, "
                    "but a few are, you won't cherry pick these elements as additionalProperties. In other words, you will extract "
                    "additionalProperties if many elements are in key/value form in a common parent in the HTML.\n\n"
                    "If the name or the value is not explicitly provided in the HTML structure, it is not considered an additionalProperty."
                ),
            },
        },
    )
    """List of name-value pais of data about a specific, otherwise unmapped
    feature.

    Additional properties usually appear in product pages in the form of a
    specification table or a free-form specification list.

    Additional properties that require 1 or more extra requests may not be
    extracted.

    See also ``features``.
    """

    aggregateRating: Optional[AggregateRating] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "The overall product rating, based on a collection of reviews or ratings."
            }
        },
    )
    """Aggregate data about reviews and ratings."""

    availability: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "enum": ["InStock", "OutOfStock"],
                "llmDescription": 'Product availability, "InStock" when it\'s available, and "OutOfStock" when it\'s not available. For node selection, try to find the nodes of the HTML that indicate a positive or negative availability of the product.',
            }
        },
    )
    """Availability status.

    The value is expected to be one of: ``"InStock"``, ``"OutOfStock"``.
    """

    brand: Optional[Brand] = None
    """Brand or manufacturer of the product."""

    breadcrumbs: Optional[List[Breadcrumb]] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "A list of breadcrumbs (a specific navigation element) with optional `name` and `url` fields. Always prioritize the list of breadcrumbs that is more complete, i.e. the one with higher number of elements that details all the levels/categories of the product.",
                "llmHint": f"# Recommendations on How to Extract Breadcrumbs\n\n## Recommended Approach\n\nYou should try to use `zyte_parsers.breadcrumbs.extract_breadcrumbs`, as it provides a standardized approach for identifying, cleaning, and structuring breadcrumb navigation data from various HTML inputs.\n\nHowever, if you need to implement a custom extraction method, you are allowed to not use the provided function. Explain why you decide to use or not use the function in your explanation.\n\n---\n\n## What It Can Extract\n\nThe `extract_breadcrumbs` function extracts the following breadcrumb elements:\n\n1. **Clickable Breadcrumb Items**\n   - Detects `<a>` elements that typically contain the breadcrumb link along with their associated text.\n\n2. **Textual Breadcrumb Items**\n   - It can extract breadcrumb names from plain text nodes, even when they are not wrapped in a link.\n\n3. **Compound Breadcrumbs from Single Nodes**\n   - In cases where a single element contains multiple breadcrumb names separated by common delimiters, the function splits them into separate items.\n\n---\n\n## What It Can't Extract / Limitations\n\n1. **Non-Standard Breadcrumb Structures**\n   - If the breadcrumb navigation does not follow typical HTML patterns (for example, if it relies heavily on JavaScript rendering or uses unconventional elements), the extraction may fail or be incomplete.\n\n2. **Deeply Nested Breadcrumbs**\n   - The extraction is performed with a configurable maximum search depth (default is 10). Breadcrumb items nested deeper than this limit might be missed.\n\n3. **Custom Separators**\n   - The function depends on a predefined set of separator characters. If a site uses custom or unusual delimiters, the splitting logic may not work as expected.\n\n4. **Dropdown Menus and Complex Markup**\n   - Breadcrumbs embedded in dynamic dropdowns or elements with complex class attributes (e.g., those related to dropdown menus) may be intentionally skipped to avoid incorrect extractions.\n\n---\n\n## Examples\n\n### Example 1\n\n{_BREADCRUMBS_EXAMPLE_1}\n\n### Example 2\n\n{_BREADCRUMBS_EXAMPLE_2}\n\n",
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

    color: Optional[str] = attrs.field(
        default=None,
        metadata={"json_schema_extra": {"llmDescription": "Color of the product."}},
    )
    """Color.

    It is extracted as displayed (e.g. ``"white"``).

    See also ``size``, ``style``.
    """

    currency: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "Price currency converted to the 3 letter currency code (ISO 4217 standard)."
            }
        },
    )
    """Price currency `ISO 4217`_ alphabetic code (e.g. ``"USD"``).

    See also ``currencyRaw``.

    .. _ISO 4217: https://en.wikipedia.org/wiki/ISO_4217
    """

    currencyRaw: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": 'The currency of the product price, as given on the website, without extra normalization (for example, both "$" and "USD" are possible currencies). This is usually the currency that appears next to the price visually on the web site, and it is commonly a symbol but can also appear normalized already next to the price. Do not include non-currencies like "-"'
            }
        },
    )
    """Price currency as it appears on the webpage (no post-processing), e.g.
    ``"$"``.

    See also ``currency``.
    """

    description: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "The complete product description",
                "llmHint": "You MUST use the method `extract_text` from the `html_text` library to extract this value.",
            }
        },
    )
    """Plain-text description.

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
                "llmDescription": "Html containing the complete product description. The output of this field should be HTML, so the HTML of the description, not just the description. The html should always be the outer html of the node, and I expect the output of this field to start with some html tags, and end with the same tags. The HTML should be valid, so it should not contain any unclosed tags, etc.",
                "llmHint": (
                    f"# Recommendations on How to Extract HTML\n"
                    f"\n"
                    f"It is strongly recommended to use `clear_html` to extract the HTML. This library provides a standardized way to clean and normalize HTML documents. It removes unwanted elements while preserving essential content and embeddings, making it easier to extract meaningful text or clean HTML markup for further processing.\n"
                    f"\n"
                    f"## What It's Used For\n"
                    f"\n"
                    f"- **HTML Cleaning**: Normalize and clean HTML trees by removing inline styles, unnecessary tags (e.g., `<figcaption>`), and extraneous attributes.\n"
                    f"- **Embeddings Preservation**: Preserve specific HTML embeddings through a whitelist.\n"
                    f"- **Output Conversion**: Generate clean HTML or plain text from processed HTML nodes.\n"
                    f"\n"
                    f"Important note: `clear_html` already wraps the HTML in `<article>` tags, so you shouldn't really add this with code.\n"
                    f"\n"
                    f"---\n"
                    f"\n"
                    f"## Example\n"
                    f"\n"
                    f"{_DESCRIPTION_HTML_EXAMPLE}\n"
                ),
            }
        },
    )
    """HTML description.

    See ``description`` for extraction details.

    The format is not the raw HTML from the source webpage. See the `HTML
    normalization specification`_ for details.

    .. _HTML normalization specification: https://docs.zyte.com/automatic-extraction/article.html#format-of-articlebodyhtml-field
    """

    features: Optional[List[str]] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "A list of features of the Product. The features of a Product can be found generally on the product page arranged in a list, each of the elements of which is a feature of the product. The list is usually bulleted, but not necessarily. The features extracted here should appear in the page in a way that are easily parseable with code, so elements from e.g. free text or descriptions that would need semantic understanding or very complex parsing are not considered these features. Each of the features are usually each in a single element or bullet point. Always extract the features even if they appear or they'd be in other fields, as long as they're systematically shown in the page as described (e.g. as elements in a list, structured, etc.), so it does not matter if they are already extracted in other fields.",
            }
        },
    )
    """List of features.

    They are usually listed as bullet points in product webpages.

    See also ``additionalProperties``.
    """

    gtin: Optional[List[Gtin]] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "List of standardized GTIN product identifiers associated with the product, which are unique for the product across different sellers.",
                "llmHint": f'# Recommendations on How to Extract GTIN\n\nIt is recommended to use `zyte_parsers.gtin.extract_gtin` for extracting and validating GTIN identifiers. This function provides a standardized approach for identifying, cleaning, and validating GTINs within text-based inputs.\n\n## What It Can Extract\n\nThe `extract_gtin` function extracts and validates the following types of identifiers:\n\n- **ISBN10 and ISBN13** \u2013 for books and publications.\n- **ISSN** \u2013 for periodicals.\n- **ISMN** \u2013 for printed music.\n- **UPC** \u2013 a 12-digit code used in retail.\n- **GTIN8, GTIN13, GTIN14** \u2013 common formats for product identification.\n- **EAN13** \u2013 recognized via the same mechanisms as ISBN13 or GTIN13.\n\nThe function automatically cleans the input (removing extraneous characters and known prefixes like "ISBN13") and uses libraries (such as `stdnum` and `gtin.validator`) to validate and classify the identifier.\n\n## What It Can\'t Extract / Limitations\n\n- **Non-numeric or mixed codes**: If a candidate code includes letters interleaved with digits or is formatted in an unexpected way, it might be rejected.\n- **Multiple codes**: The function is designed to extract a single GTIN from the input. If the text contains several codes, it will only return one (typically the first valid extraction).\n- **Malformed or incomplete identifiers**: Codes that do not pass the validation rules (for instance, due to incorrect check digits or wrong length) will not be recognized.\n- **Alphanumeric SKUs**: Some SKU values that look like GTINs but include letters in between numbers may be discarded to avoid false positives.\n\n---\n\n# Examples\n\n## Example 1\n\n{_GTIN_EXAMPLE_1}\n\n## Example 2\n\n{_GTIN_EXAMPLE_2}\n\n## Example 3\n\n{_GTIN_EXAMPLE_3}\n',
            }
        },
    )
    """List of standardized GTIN_ product identifiers associated with the
    product, which are unique for the product across different sellers.

    See also: ``mpn``, ``productId``, ``sku``.

    .. _GTIN: https://en.wikipedia.org/wiki/Global_Trade_Item_Number
    """

    images: Optional[List[Image]] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "A list with all the images of the product",
            }
        },
    )
    """All product images.

    The main image (see ``mainImage``) should be first in the list.

    Images only displayed as part of the product description are excluded.
    """

    mainImage: Optional[Image] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "Main image of the product",
            }
        },
    )
    """Main image of the product."""

    metadata: Optional[ProductMetadata] = attrs.field(
        default=None,
        converter=to_metadata_optional(ProductMetadata),  # type: ignore[misc]
        kw_only=True,
    )
    """Data extraction process metadata."""

    mpn: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "The Manufacturer Part Number (MPN) of the product. It is issued by the manufacturer, and is the same across different e-commerce websites.",
            }
        },
    )
    """`Manufacturer part number (MPN)`_.

    A product should have the same MPN across different e-commerce websites.

    See also: ``gtin``, ``productId``, ``sku``.

    .. _Manufacturer part number (MPN): https://en.wikipedia.org/wiki/Part_number
    """

    name: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "The name of the product",
            }
        },
    )
    """Product name as it appears on the webpage (no post-processing)."""

    price: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "The price at which the product is being offered right now. If there are any discounts, pick the price with discounts applied.\nThe value should always be lower than `regularPrice`, and if it's the same, then we should only output `price`, not `regularPrice`. So if a price is present, we should always output it in this attribute.\nBoth `price` and `regularPrice` should be coherent, so both should be either with VAT or without VAT. The versions with VAT are always preferred.\nThe final extracted string should not contain the currency code, currency denomination, or currency symbol -- just the price value itself.\n\nFormat:\n- no thousands separator\n- full stop as decimal separator\n- if page shows no decimals, extract with two decimals, e.g. XY.00",
            }
        },
    )
    """Price at which the product is being offered.

    It is a string with the price amount, with a full stop as decimal
    separator, and no thousands separator or currency (see ``currency`` and
    ``currencyRaw``), e.g. ``"10500.99"``.

    If ``regularPrice`` is not ``None``, ``price`` should always be lower than
    ``regularPrice``.
    """

    productId: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "The unique identifier of the product.",
            }
        },
    )
    """Product identifier, unique within an e-commerce website.

    It may come in the form of an SKU or any other identifier, a hash, or even
    a URL.

    See also: ``gtin``, ``mpn``, ``sku``.
    """

    regularPrice: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "The price at which the product was being offered (by the same retailer) and which is presented as a reference to the current price. It may be represented by original price, list price or maximum retail price for which the product is sold. This field is only returned if it is explicitly mentioned in the offer or the product page.\nNote that reference price from other retailers or other websites is not considered a regular price. In other words, a regular price is the price that the product was being offered by the same retailer but without any discounts applied.\nThe value should always be higher than `price`, and if it's the same, then we should only output `price`, not `regularPrice`.\nIt can only exist if `price` exists.\nBoth `price` and `regularPrice` should be coherent, so both should be either with VAT or without VAT. The versions with VAT are always preferred.\nThe final extracted string should not contain the currency code, currency denomination, or currency symbol -- just the price value itself.\n\nFormat:\n- no thousands separator,\n- full stop as decimal separator.\n- if page shows no decimals, extract with two decimals, e.g. XY.00",
            }
        },
    )
    """Price at which the product was being offered in the past, and which is
    presented as a reference next to the current price.

    It may be labeled as the original price, the list price, or the maximum
    retail price for which the product is sold.

    See ``price`` for format details.

    If ``regularPrice`` is not ``None``, it should always be higher than
    ``price``.
    """

    size: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": 'The size of the product. Some examples: "XL", "32Wx34L", "Large", "750x450x800", "10m", "Height: 48cm - 86cm, Width: 204cm, Depth: 93cm" etc.).\n\nThis is a string that specifies the imformation of the size of the product itself.\n\nBy order of preference (higher priority at the top), the size you will select will be:\n\n- The one indicated by the default selected variant (e.g. size picker button or dropdown)\n- The one that holds the most specific size information (e.g. "750x450x800" is more specific than "Large").\n- The one that clarifies better the dimensions (e.g. "45H x 30W x 20D" is more clarifying than "45x30x20").\n- The most obvious one (e.g. introduced by a label like "Size", "Dimensions", etc.).\n\nGenerally, unless you really need to, you will not parse the size information from the name of the product. E.g. if there\'s a product whose name is "Large Stove", you will consider "Large" here parsed from the name **as a very last resort** to extract the size information, and only if you cannot find any other size information in the page."\n',
            }
        },
    )
    """Size or dimensions.

    Pertinent to products such as garments, shoes, accessories, etc.

    It is extracted as displayed (e.g. ``"XL"``).

    See also ``color``, ``style``.
    """

    sku: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "product SKU or other unique identifier",
            }
        },
    )
    """`Stock keeping unit (SKU)`_ identifier, i.e. a merchant-specific product
    identifier.

    See also: ``gtin``, ``mpn``, ``productId``.

    .. _Stock keeping unit (SKU): https://en.wikipedia.org/wiki/Stock_keeping_unit
    """

    style: Optional[str] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": 'Style of the product. It can also be referred as pattern/finish on the product page. Example values: "Polka dots", "Striped", "Nickel finish with Translucent glass", etc.',
            }
        },
    )
    """Style.

    Pertinent to products such as garments, shoes, accessories, etc.

    It is extracted as displayed (e.g. ``"polka dots"``).

    See also ``color``, ``size``.
    """

    url: str = attrs.field(converter=url_to_str)
    """Main URL from which the data has been extracted.

    See also ``canonicalUrl``.
    """

    variants: Optional[List[ProductVariant]] = attrs.field(
        default=None,
        metadata={
            "json_schema_extra": {
                "llmDescription": "The list with all the variations of products dimensions (size) and colors.\nIf the page only shows one size and/or color, it's not considered a variant.\nIf there's a lack of size or color variants, any other variations in the product's related size or color should be considered as variants.\nThe different variants of the product are usually selectable as interactive elements on the product page, like buttons, dropdowns or radio buttons, and they usually (but not always) come in lists within sections.\nImportant: The list of variants should only be populated if there are different sizes or colors to choose from. So a variant only exists if for the same attribute (color, size, or related attribute) there are different options for the main product shown in the page.\nAlso, variants list should not contain duplicated variants, i.e. no two elements in the list should have the same values for all attributes.\n\nEvery element of the list is a different variant. One variant can have some empty attributes (null/None), but elements should have at least one non-null element and should never be empty strings for any attribute.\n\nOther products, recommended products, product add-ons, bundle elements, etc. are not considered variants.\nBe sure to always deduplicate variants, so no two elements in the list should have the same values for all attributes.\n\nAnother important detail: Just combining the color and size attributes is not enough to determine a variant, because it may not exist. Most of the time, the needed info for the page to change the HTML when a variant is pressed (and shows then the actual existing variant) is in the HTML, but not always. So you should try to extract the variant information from the HTML, and if you can't find it, then you can combine them blindly, but always try to extract the variant information from the scripts or doing some AJAX requests, as e.g. a particular color does not have a particular size, but this is only shown in the HTML when the variant is selected.\n",
            }
        },
    )
    """List of variants.

    When slightly different versions of a product are displayed on the same
    product page, allowing you to choose a specific product version from a
    selection, each of those product versions are considered a product
    variant.

    Product variants usually differ in ``color`` or ``size``.

    The following items are *not* considered product variants:

    -   Different products within the same bundle of products.
    -   Product add-ons, e.g. premium upgrades of a base product.

    Only variant-specific data is extracted as product variant details. For
    example, if variant-specific versions of the product description do not
    exist in the source webpage, the description attributes of the product
    variant are *not* filled with the base product description.

    Extracted product variants may not include those that are not visible in
    the source webpage.

    Product variant details may not include those that require multiple
    additional requests (e.g. 1 or more requests per variant).
    """


@attrs.define(kw_only=True)
class ProductVariant(Item):
    """:class:`Product` variant.

    See :attr:`Product.variants`, :class:`ProductVariantExtractor`,
    :class:`ProductVariantSelectorExtractor`.
    """

    additionalProperties: Optional[List[AdditionalProperty]] = None
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

    See also ``size``, ``style``.
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

    gtin: Optional[List[Gtin]] = None
    """List of standardized GTIN_ product identifiers associated with the
    product, which are unique for the product across different sellers.

    See also: ``mpn``, ``productId``, ``sku``.

    .. _GTIN: https://en.wikipedia.org/wiki/Global_Trade_Item_Number
    """

    images: Optional[List[Image]] = None
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

    See also ``color``, ``style``.
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

    See also ``color``, ``size``.
    """

    url: Optional[str] = attrs.field(
        default=None, converter=url_to_str_optional, kw_only=True
    )
    """Main URL from which the product variant data could be extracted."""
