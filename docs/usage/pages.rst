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
    ``@field``-decorated methods. See :ref:`web-poet-fields`.

-   They provide a default implementation for their
    :attr:`~zyte_common_items.Page.metadata` and
    :attr:`~zyte_common_items.Page.url` fields.

The following code shows a :class:`~zyte_common_items.ProductPage` subclass
whose ``to_item`` method returns an instance of
:class:`~zyte_common_items.Product` with
:attr:`~zyte_common_items.Product.metadata`, a
:attr:`~zyte_common_items.Product.name`, and a
:attr:`~zyte_common_items.Product.url`:

.. code-block:: python

   import attrs
   from zyte_common_items import ProductPage

    @attrs.define
    class CustomProductPage(ProductPage):

        @field
        def name(self):
            return self.css("h1::text").get()
