=====
Usage
=====

Creating items from dictionaries
================================

You can create an :ref:`item <items>` from any :class:`dict`-like object via
the :meth:`~zyte_common_items.base.Item.from_dict` method.

For example, to create a :class:`~zyte_common_items.items.Product`:

>>> from zyte_common_items import Product
>>> data = {
...     'url': 'https://example.com/',
...     'mainImage': {
...         'url': 'https://example.com/image.png',
...     },
...     'gtin': [
...         {'type': 'gtin13', 'value': '9504000059446'},
...     ],
... }
>>> product = Product.from_dict(data)

:meth:`~zyte_common_items.base.Item.from_dict` applies the right classes to
nested data, such as :class:`~zyte_common_items.components.Image` and
:class:`~zyte_common_items.components.Gtin` for the input above.

>>> product.url
'https://example.com/'
>>> product.mainImage
Image(url='https://example.com/image.png')
>>> product.canonicalUrl
>>> product.gtin
[Gtin(type='gtin13', value='9504000059446')]


Creating items from lists
=========================

You can create items in bulk using the
:meth:`~zyte_common_items.base.Item.from_list` method:

>>> from zyte_common_items import Product
>>> data_list = [
...     {'url': 'https://example.com/1', 'name': 'Product 1'},
...     {'url': 'https://example.com/2', 'name': 'Product 2'},
...     {'url': 'https://example.com/3', 'name': 'Product 3'},
...     {'url': 'https://example.com/4', 'name': 'Product 4'}
... ]
>>> products = Product.from_list(data_list)
>>> len(products)
4
>>> products[0].url
'https://example.com/1'
>>> products[3].name
'Product 4'

This can be especially useful if you're processing lots of items from an API,
file, database, etc.


Handling unknown fields
=======================

:ref:`Items <items>` and :ref:`components <components>` do not allow attributes
beyond those they define:

>>> from zyte_common_items import Product
>>> product = Product(url="https://example.com", foo="bar")
Traceback (most recent call last):
...
TypeError: Product.__init__() got an unexpected keyword argument 'foo'
>>> product = Product(url="https://example.com")
>>> product.foo = "bar"
Traceback (most recent call last):
...
AttributeError: 'Product' object has no attribute 'foo'

However, when using :meth:`~zyte_common_items.base.Item.from_dict` and
:meth:`~zyte_common_items.base.Item.from_list`, unknown fields assigned to
items and components **won't cause an error**. Instead, they are placed inside
the :attr:`~zyte_common_items.base.Item._unknown_fields_dict` attribute:

>>> from zyte_common_items import Product
>>> data = {
...     'url': 'https://example.com/',
...     'unknown_field': True,
... }
>>> product = Product.from_dict(data)
>>> product._unknown_fields_dict
{'unknown_field': True}

This allows compatibility with future field changes in the input data, which
could cause backwards incompatibility issues.

Note, however, that unknown fields are only supported within items and
components. Input processing can still fail for other types of unexpected
input:

>>> from zyte_common_items import Product
>>> data = {
...     'url': 'https://example.com/',
...     'mainImage': 'not a dictionary',
... }
>>> product = Product.from_dict(data)
Traceback (most recent call last):
...
AttributeError: 'str' object has no attribute 'items'
>>> data = {
...     'url': 'https://example.com/',
...     'breadcrumbs': 3,
... }
>>> product = Product.from_dict(data)
Traceback (most recent call last):
...
TypeError: 'int' object is not iterable
