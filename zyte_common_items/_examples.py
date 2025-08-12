from collections.abc import Sequence
from dataclasses import dataclass
from textwrap import indent


@dataclass
class PageObjectMethodExample:
    description: str
    html: str
    imports: Sequence[str]
    source_code: str
    expected: str

    def __str__(self):
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
            f"{'\n'.join(self.imports)}\n"
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
            f"{indent(self.source_code, " " * 4)}\n"
            f"```\n"
            f"\n"
            f"### Expected output (when applied to the example html)\n"
            f"\n"
            f"```\n"
            f"{self.expected}\n"
            f"```"
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
    expected=(
        "<article>\n"
        "\n"
        "<p>Paragraph 1</p>\n"
        "\n"
        "<p>Paragraph 2</p>\n"
        "\n"
        "</article>"
    ),
)
