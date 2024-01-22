.. _page-objects:

============
Page objects
============

The :ref:`provided page object classes <page-object-api>` are good base classes
for custom page object classes that implement website-specific :doc:`page
objects <web-poet:index>`.

They provide the following base line:

-   They declare the :ref:`item class <items>` that they return, allowing for
    their ``to_item`` method to automatically build an instance of it from
    ``@field``-decorated methods. See :ref:`fields`.

-   They provide a default implementation for their
    :attr:`~zyte_common_items.Page.metadata` and
    :attr:`~zyte_common_items.Page.url` fields.

-   They also provide a default implementation for some item-specific fields in
    pages that have those (except for ``description`` in the pages for
    :class:`~zyte_common_items.Article` which has different requirements):

    - :attr:`~zyte_common_items.pages.PriceMixin.currency`
    - :attr:`~zyte_common_items.pages.PriceMixin.currencyRaw`
    - :attr:`~zyte_common_items.pages.DescriptionMixin.description`
    - :attr:`~zyte_common_items.pages.DescriptionMixin.descriptionHtml`

The following code shows a :class:`~zyte_common_items.ProductPage` subclass
whose ``to_item`` method returns an instance of
:class:`~zyte_common_items.Product` with
:attr:`~zyte_common_items.Product.metadata`, a
:attr:`~zyte_common_items.Product.name`, and a
:attr:`~zyte_common_items.Product.url`:

.. code-block:: python

    import attrs
    from zyte_common_items import ProductPage

    class CustomProductPage(ProductPage):

        @field
        def name(self):
            return self.css("h1::text").get()

Page object classes with the ``Auto`` prefix can be used to easily define page
object classes that get an :ref:`item <items>` as a dependency from another
page object class, can generate an identical item by default, and can also
easily override specific fields of the item, or even return a new item with
extra fields. For example:

.. code-block:: python

    import attrs
    from zyte_common_items import AutoProductPage, Product, Returns, field

    @attrs.define
    class ExtendedProduct(Product):
        foo: str

    class ExtendedProductPage(AutoProductPage, Returns[ExtendedProduct]):

        @field
        async def name(self):
            return f"{self.product.brand.name} {self.product.name}"

        @field
        async def foo(self):
            return "bar"

Field processors
================

Some of these base classes include a ``Processors`` subclass that enables
:ref:`default processors <web-poet:field-processors>` for some fields.

All ``aggregateRating`` fields have the following processor enabled:

.. autofunction:: zyte_common_items.processors.rating_processor

All ``brand`` fields have the following processor enabled:

.. autofunction:: zyte_common_items.processors.brand_processor

All ``breadcrumbs`` fields have the following processor enabled:

.. autofunction:: zyte_common_items.processors.breadcrumbs_processor

All ``description`` fields except in pages for
:class:`~zyte_common_items.Article` have the following processor enabled:

.. autofunction:: zyte_common_items.processors.description_processor

All ``descriptionHtml`` fields have the following processor enabled:

.. autofunction:: zyte_common_items.processors.description_html_processor

All ``gtin`` fields have the following processor enabled:

.. autofunction:: zyte_common_items.processors.gtin_processor

All ``price`` fields have the following processor enabled:

.. autofunction:: zyte_common_items.processors.price_processor

All ``regularPrice`` fields have the following processor enabled:

.. autofunction:: zyte_common_items.processors.simple_price_processor

These processors can also be used in the user code.
