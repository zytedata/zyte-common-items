"""Test metadata expectations."""


def test_type_classes():
    """For every type-specific page there must be a matching metadata class."""
    import zyte_common_items

    pages = {
        obj_name
        for obj_name in zyte_common_items.__dict__
        if (
            not obj_name.startswith("Base")
            and obj_name.endswith("Page")
            and obj_name != "Page"
        )
    }
    for page in pages:
        base = page[:-4]
        metadata = f"{base}Metadata"
        assert metadata in zyte_common_items.__dict__
