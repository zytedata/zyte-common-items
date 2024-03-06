import pkgutil
from datetime import datetime


def get_copyright(attribution, *, first_year):
    current_year = datetime.now().year
    years = (
        current_year if first_year == current_year else f"{first_year}-{current_year}"
    )
    return f"{years}, {attribution}"


def get_version_and_release():
    try:
        import zyte_common_items  # noqa: F401
    except ImportError:
        return "", ""
    version_bytes = pkgutil.get_data("zyte_common_items", "VERSION") or b""
    release = version_bytes.decode("ascii").strip()
    version_tuple = tuple(int(v) if v.isdigit() else v for v in release.split("."))
    version = ".".join(str(part) for part in version_tuple[:2])
    return version, release


project = "zyte-common-items"
copyright = get_copyright("Zyte Group Ltd", first_year=2022)
version, release = get_version_and_release()

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
]

html_theme = "sphinx_rtd_theme"

autodoc_member_order = "groupwise"
nitpick_ignore = [
    ("py:class", "itemadapter.ItemAdapter"),
    ("py:class", "web_poet.pages.ItemT"),
    ("py:class", "zyte_common_items.pages._BasePage"),
]

intersphinx_disabled_reftypes = []
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "lxml": ("https://lxml.de/apidoc/", None),
    "parsel": ("https://parsel.readthedocs.io/en/stable", None),
    "scrapy": ("https://docs.scrapy.org/en/stable", None),
    "scrapy-poet": ("https://scrapy-poet.readthedocs.io/en/stable", None),
    "web-poet": ("https://web-poet.readthedocs.io/en/stable", None),
    "zyte-parsers": ("https://zyte-parsers.readthedocs.io/en/stable", None),
}
