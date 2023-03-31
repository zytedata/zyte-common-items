from typing import List, Optional, Union

import attrs
import pytest

from zyte_common_items import Item, Product, is_data_container


class NotConsideredAnItem:
    """It has to inherit from Item to be considered one."""

    pass


@attrs.define
class SubItem(Item):
    name: str


@attrs.define
class BigItem(Item):
    sub_item: Optional[SubItem] = None


def test_is_data_container():
    """It should be able to discern if a given class/instance is a data container
    that is defined inside this repository.
    """
    assert is_data_container(Item)
    assert is_data_container(SubItem)
    assert is_data_container(Item())
    assert is_data_container(SubItem(name="test"))

    assert not is_data_container(NotConsideredAnItem)
    assert not is_data_container(NotConsideredAnItem())


def test_from_dict():
    """Tests the annotation-aware behavior for correcty deriving the correct type
    in the sub fields.
    """

    assert BigItem(sub_item=None).sub_item is None

    item = BigItem.from_dict({"sub_item": {"name": "hello"}})
    type(item.sub_item) == SubItem  # noqa: B015


def test_from_dict_bad_annotation():
    """Items with fields annotated with a Union of multiple different types should
    error out.
    """

    @attrs.define
    class A(Item):
        a: Union[int, str]

    pattern = (
        r"^tests\.\S+\.A\.a is annotated with typing\.Union\[int, str\]\. "
        r"Fields should only be annotated with one type \(or optional\)\.$"
    )
    with pytest.raises(ValueError, match=pattern):
        A.from_dict({"a": 1})


def test_from_dict_non_dict():
    @attrs.define
    class A(Item):
        a: str

    pattern = r"Expected a dict with fields from tests\.\S+?\.A, got 'a'\."
    with pytest.raises(ValueError, match=pattern):
        A.from_dict("a")  # type: ignore


def test_from_dict_non_dict_field():
    @attrs.define
    class B(Item):
        b: str

    @attrs.define
    class A(Item):
        a: B

    pattern = r"Expected a to be a dict with fields from tests\.\S+?\.B, got 'b'\."
    with pytest.raises(ValueError, match=pattern):
        A.from_dict({"a": "b"})


def test_from_dict_from_list_non_list_field():
    @attrs.define
    class A(Item):
        a: List[str]

    pattern = r"Expected a to be a list, got 'b'\."
    with pytest.raises(ValueError, match=pattern):
        A.from_dict({"a": "b"})


def test_from_dict_from_list_non_dict_field():
    @attrs.define
    class B(Item):
        b: str

    @attrs.define
    class A(Item):
        a: List[B]

    pattern = r"Expected a\[0\] to be a dict with fields from tests\.\S+?\.B, got 'b'\."
    with pytest.raises(ValueError, match=pattern):
        A.from_dict({"a": ["b"]})


def test_item_unknown_input():
    product = Product.from_dict(
        dict(
            a="b",
            additionalProperties=[{"name": "a", "value": "b", "max": 10}],
            aggregateRating=dict(worstRating=0),
            url="https://example.com/?product=product22",
        )
    )
    assert product._unknown_fields_dict["a"] == "b"
    assert product.aggregateRating._unknown_fields_dict["worstRating"] == 0
    assert product.additionalProperties[0]._unknown_fields_dict["max"] == 10


def test_item_attribute_error():
    foo = SubItem(name="foo")
    with pytest.raises(AttributeError):
        foo.value = "bar"  # type: ignore[attr-defined]


def test_item_unknown_field_init():
    with pytest.raises(TypeError):
        SubItem(name="foo", value="bar")  # type: ignore[call-arg]
