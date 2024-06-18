from typing import Callable, List, Optional

from web_poet import ItemPage, field
from web_poet.fields import get_fields_dict


def auto_field(
    method=None,
    *,
    cached: bool = False,
    meta: Optional[dict] = None,
    out: Optional[List[Callable]] = None,
):
    """Decorator that works like :func:`web_poet.fields.field` but sets
    ``auto_field`` to ``True`` by default in *meta*.

    .. code-block:: python

        from zyte_common_items import AutoProductPage
        from zyte_common_items.fields import auto_field


        class ProductPage(AutoProductPage):
            @auto_field
            def name(self):
                return super().name
    """
    meta = meta or {}
    meta.setdefault("auto_field", True)
    return field(method, cached=cached, meta=meta, out=out)


def is_auto_field(cls: ItemPage, field: str):
    """Return ``True`` if the field named *field* of the *cls* page object
    class has ``auto_field`` set to ``True`` in its field metadata.

    All fields defined in :ref:`auto page object classes <auto>` meet this
    condition.
    """
    fields_dict = get_fields_dict(cls)
    field_meta = fields_dict[field].meta or {}
    return field_meta.get("auto_field", False)
