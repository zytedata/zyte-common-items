from collections.abc import Sequence
from dataclasses import dataclass
from textwrap import indent
from typing import Any


@dataclass
class PageObjectMethodExample:
    description: str
    html: str
    imports: Sequence[str]
    source_code: str
    expected: Any

    def __str__(self):
        import_lines = "\n".join(self.imports)
        return (
            f"{self.description}\n"
            f"\n"
            f"### Example html\n"
            f"\n"
            f"```html\n"
            f"{self.html}\n"
            f"```\n"
            f"\n"
            f"### Imports for the example\n"
            f"\n"
            f"```python\n"
            f"{import_lines}\n"
            f"```\n"
            f"\n"
            f"### Example of use in a page object field (to extract data from the example html)\n"
            f"\n"
            f"\n"
            f"```python\n"
            f"# ... imports ...\n"
            f"\n"
            f"class Extractor:\n"
            f"    # ... other stuff ...\n"
            f"\n"
            f"{indent(self.source_code, ' ' * 4)}\n"
            f"```\n"
            f"\n"
            f"### Expected output (when applied to the example html)\n"
            f"\n"
            f"```\n"
            f"{self.expected}\n"
            f"```"
        )


_BREADCRUMBS_EXAMPLE_1 = PageObjectMethodExample(
    description=(
        "Extract Breadcrumbs from a Simple HTML Snippet\n\n"
        "In this example, the breadcrumb structure is straightforward with links and separator elements.\n"
    ),
    html=(
        "<html>\n"
        "  <body>\n"
        '    <div id="breadcrumbs">\n'
        '      <a href="/">Home</a>\n'
        "      <span> / </span>\n"
        '      <a href="/category">Category</a>\n'
        "      <span> / </span>\n"
        "      <span>Product</span>\n"
        "    </div>\n"
        "  </body>\n"
        "</html>\n"
    ),
    imports=["from zyte_parsers.breadcrumbs import extract_breadcrumbs"],
    source_code=(
        "def extract(self):\n"
        "    tree = self.selector.root\n"
        "    breadcrumbs = extract_breadcrumbs(tree, base_url=self.url)\n"
        '    return [{"name": bc.name, "url": bc.url} for bc in breadcrumbs]'
    ),
    expected=[
        {"name": "Home", "url": "http://example.com/"},
        {"name": "Category", "url": "http://example.com/category"},
        {"name": "Product", "url": None},
    ],
)

_BREADCRUMBS_EXAMPLE_2 = PageObjectMethodExample(
    description=(
        "Extract Breadcrumbs from a Single Text Node with Separators\n\n"
        "Some pages may provide breadcrumbs as a single text string with separators rather than distinct elements.\n"
    ),
    html=(
        "<html>\n"
        "  <body>\n"
        '    <div id="breadcrumbs">\n'
        "      Home / Category / Product\n"
        "    </div>\n"
        "  </body>\n"
        "</html>\n"
    ),
    imports=["from zyte_parsers.breadcrumbs import extract_breadcrumbs"],
    source_code=(
        "def extract(self):\n"
        "    tree = self.selector.root\n"
        "    breadcrumbs = extract_breadcrumbs(tree, base_url=self.url)\n"
        '    return [{"name": bc.name, "url": bc.url} for bc in breadcrumbs]'
    ),
    expected=[
        {"name": "Home", "url": None},
        {"name": "Category", "url": None},
        {"name": "Product", "url": None},
    ],
)


_DESCRIPTION_HTML_EXAMPLE = PageObjectMethodExample(
    description="Extract the cleaned html of a particular node",
    html=(
        "<html>\n"
        "  <body>\n"
        "    <header>\n"
        "      <h1>Page Header</h1>\n"
        "    </header>\n"
        '    <div id="description" style="color:blue">\n'
        "      <div>Paragraph 1</div>\n"
        "      <div>Paragraph 2</div>\n"
        "      <figcaption>Image description</figcaption>\n"
        "    </div>\n"
        "    <footer>\n"
        "      <p>Page Footer</p>\n"
        "    </footer>\n"
        "  </body>\n"
        "</html>\n"
    ),
    imports=["from clear_html.clean import clean_node, cleaned_node_to_html"],
    source_code=(
        "def extract(self):\n"
        '    candidates = self.selector.css("#description")\n'
        "    if not candidates:\n"
        "        return None\n"
        "    node = candidates[0].root\n"
        "    cleaned_node = clean_node(node)\n"
        "    cleaned_html = cleaned_node_to_html(cleaned_node)\n"
        "    return cleaned_html"
    ),
    expected=("<article>\n\n<p>Paragraph 1</p>\n\n<p>Paragraph 2</p>\n\n</article>"),
)

_GTIN_EXAMPLE_1 = PageObjectMethodExample(
    description=(
        "Extract GTIN (ISBN13) from a text containing an ISBN.\n"
        "\n"
        'The input contains a prefix ("ISBN13") and a valid 13-digit ISBN. The function removes the prefix, validates the ISBN, and classifies it as "isbn13".\n'
    ),
    html=(
        "<html>\n"
        "  <body>\n"
        '    <div id="product-info">ISBN13: 9783161484100</div>\n'
        "  </body>\n"
        "</html>\n"
    ),
    imports=["from zyte_parsers.gtin import extract_gtin"],
    source_code=(
        "def extract(self):\n"
        "    candidate = self.selector.xpath(\"//div[@id='product-info']/text()\").get()\n"
        "    gtin_obj = extract_gtin(candidate)\n"
        '    return [{"type": gtin_obj.type, "value": gtin_obj.value}]'
    ),
    expected=[
        {"type": "isbn13", "value": "9783161484100"},
    ],
)

_GTIN_EXAMPLE_2 = PageObjectMethodExample(
    description=(
        "Extract GTIN (UPC) from a text containing a product code\n\n"
        'This example uses a plain numeric string representing a 12-digit UPC. The function extracts and validates the code, classifying it as "upc".\n'
    ),
    html=(
        "<html>\n"
        "  <body>\n"
        '    <div id="product-info">Product code: 036000291452</div>\n'
        "  </body>\n"
        "</html>\n"
    ),
    imports=["from zyte_parsers.gtin import extract_gtin, Gtin"],
    source_code=(
        "def extract(self):\n"
        "    candidate = self.selector.xpath(\"//div[@id='product-info']/text()\").get()\n"
        "    gtin_obj = extract_gtin(candidate)\n"
        '    return [{"type": gtin_obj.type, "value": gtin_obj.value}]'
    ),
    expected=[
        {"type": "upc", "value": "036000291452"},
    ],
)

_GTIN_EXAMPLE_3 = PageObjectMethodExample(
    description=(
        "Generic Automatic Classification: Extract GTIN from embedded text\n\n"
        'Here, a GTIN is embedded within additional descriptive text. The extractor automatically identifies and validates the code (in this case, as "gtin8"), without needing an explicit prefix.\n'
    ),
    html=(
        "<html>\n"
        "  <body>\n"
        '    <div id="product-info">\n'
        "      Introducing our latest gadget! Look for the code 96385074 on the packaging.\n"
        "      It’s our special GTIN identifier for limited edition items.\n"
        "    </div>\n"
        "  </body>\n"
        "</html>\n"
    ),
    imports=["from zyte_parsers.gtin import extract_gtin, Gtin"],
    source_code=(
        "def extract(self):\n"
        "    candidate = self.selector.xpath(\"//div[@id='product-info']/text()\").get()\n"
        "    gtin_obj = extract_gtin(candidate)\n"
        '    return [{"type": gtin_obj.type, "value": gtin_obj.value}]'
    ),
    expected=[
        {"type": "gtin8", "value": "96385074"},
    ],
)
