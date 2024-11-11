import re
from importlib import import_module

import pytest

AUTOCLASS_PATTERN = re.compile(r".. autoclass:: zyte_common_items\.(.+?)\(\*\*kwargs\)")
TOP_LEVEL_MODULE = import_module("zyte_common_items")
TOP_LEVEL_CLASS_NAMES = {
    name for name, obj in TOP_LEVEL_MODULE.__dict__.items() if isinstance(obj, type)
}


@pytest.mark.parametrize(
    ("submodule_name", "only_in_docs", "only_in_submodule"),
    (
        ("components", set(), set()),
        ("items", {"Item", "base.ProbabilityMixin"}, {"RequestListCaster"}),
        (
            "pages",
            {"pages.base._BasePage"},
            {"DescriptionMixin", "HasMetadata", "PriceMixin"},
        ),
    ),
)
def test_component_reference_entries(submodule_name, only_in_docs, only_in_submodule):
    with open(f"docs/reference/{submodule_name}.rst") as f:
        docs_page = f.read()
    docs_class_names = set()
    for match in AUTOCLASS_PATTERN.finditer(docs_page):
        class_name = match[1]
        if class_name in only_in_docs:
            continue
        docs_class_names.add(class_name)

    module_class_names = set()
    module = import_module(f"zyte_common_items.{submodule_name}")
    for name, obj in module.__dict__.items():
        if not isinstance(obj, type) or name in only_in_submodule:
            continue
        module_class_names.add(name)

    # All classes in code are also in the reference docs.
    assert docs_class_names == module_class_names

    # All classes in the nested module are also available as top-level imports.
    in_top_level = TOP_LEVEL_CLASS_NAMES & module_class_names
    assert in_top_level == module_class_names
    not_in_top_level = module_class_names - TOP_LEVEL_CLASS_NAMES
    assert not not_in_top_level
