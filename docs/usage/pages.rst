.. _page-objects:

============
Page objects
============

:ref:`Built-in page object classes <page-object-api>` are good base classes for
custom page object classes that implement website-specific :doc:`page objects
<web-poet:index>`.

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
        def name(self):
            return f"{self.product.brand.name} {self.product.name}"

        @field
        def foo(self):
            return "bar"

.. _extractors:

Extractors
==========

For some nested fields (:class:`~.ProductFromList`, :class:`~.ProductVariant`),
:ref:`base extractors <default-processors-nested>` exist that you can subclass
to write your own extractors.

They provide the following base line:

-   They declare the :ref:`item class <items>` that they return, allowing for
    their ``to_item`` method to automatically build an instance of it from
    ``@field``-decorated methods. See :ref:`fields`.

-   They also provide default :ref:`processors <processors>` for some
    item-specific fields.

See :ref:`extractor-api`.

.. _processors:

Field processors
================

This library provides some :ref:`field processors <processor-api>`
(:ref:`web-poet documentation <web-poet:field-processors>`) and complementary
:ref:`mixins <mixins>`, and built-in :ref:`page object classes
<page-object-api>` and :ref:`extractor classes <extractor-api>` use them by
default for :ref:`some fields <field-processor-map>`.

For most :ref:`built-in field processors <processor-api>`, your field must
return a :class:`~parsel.selector.Selector`,
:class:`~parsel.selector.SelectorList`, or :class:`~lxml.html.HtmlElement`
object (as opposed to :class:`str`, :class:`int`, etc.). Then the field
processor will take care of extracting the right data.

Here are some examples of inputs and matching field implementations that will
work on built-in page object and extractor classes:

+-----------------------------------------------+---------------------------------------------------+
| Input HTML fragment                           | Field implementation and output                   |
+-----------------------------------------------+---------------------------------------------------+
| .. code-block:: html                          | .. code-block:: python                            |
|                                               |                                                   |
|     <span class="reviews">                    |     @field                                        |
|       3.8 (7 reviews)                         |     def aggregateRating(self):                    |
|     </span>                                   |         return self.css(".reviews")               |
|                                               |                                                   |
|                                               | .. code-block:: python                            |
|                                               |                                                   |
|                                               |     Product(                                      |
|                                               |         aggregateRating=AggregateRating(          |
|                                               |             bestRating=None,                      |
|                                               |             ratingValue=3.8,                      |
|                                               |             reviewCount=7,                        |
|                                               |         ),                                        |
|                                               |     )                                             |
|                                               |                                                   |
|                                               | | Supports separate selectors per field.          |
|                                               | | See :func:`~.processors.rating_processor`.      |
|                                               |                                                   |
+-----------------------------------------------+---------------------------------------------------+
| .. code-block:: html                          | .. code-block:: python                            |
|                                               |                                                   |
|     <p class="brand">                         |     @field                                        |
|       <img alt='Some Brand'>                  |     def brand(self):                              |
|     </p>                                      |         return self.css(".brand")                 |
|                                               |                                                   |
|                                               | .. code-block:: python                            |
|                                               |                                                   |
|                                               |     Product(                                      |
|                                               |         brand="Some Brand",                       |
|                                               |     )                                             |
|                                               |                                                   |
+-----------------------------------------------+---------------------------------------------------+
| .. code-block:: html                          | .. code-block:: python                            |
|                                               |                                                   |
|     <div class="nav">                         |     @field                                        |
|       <ul>                                    |     def breadcrumbs(self):                        |
|         <li>                                  |         return self.css(".nav")                   |
|           <a href="/home">Home</a>            |                                                   |
|         </li>                                 | .. code-block:: python                            |
|         <li>                                  |                                                   |
|           <a href="/about">About</a>          |     Product(                                      |
|         </li>                                 |         breadcrumbs=[                             |
|       </ul>                                   |             Breadcrumb(                           |
|     </div>                                    |                 name="Home",                      |
|                                               |                 url="https://example.com/home",   |
|                                               |             ),                                    |
|                                               |             Breadcrumb(                           |
|                                               |                 name="About",                     |
|                                               |                 url="https://example.com/about",  |
|                                               |             ),                                    |
|                                               |         ],                                        |
|                                               |     )                                             |
|                                               |                                                   |
+-----------------------------------------------+---------------------------------------------------+
| .. code-block:: html                          | .. code-block:: python                            |
|                                               |                                                   |
|     <div class="desc">                        |     @field                                        |
|       <p>Ideal for <b>scraping</b> glass.</p> |     def descriptionHtml(self):                    |
|       <p>Durable and reusable.</p>            |         return self.css(".desc")                  |
|     </div>                                    |                                                   |
|                                               | .. code-block:: python                            |
|                                               |                                                   |
|                                               |     Product(                                      |
|                                               |         description=(                             |
|                                               |             "Ideal for scraping glass.\n"         |
|                                               |             "\n"                                  |
|                                               |             "Durable and reusable."               |
|                                               |         ),                                        |
|                                               |         descriptionHtml=(                         |
|                                               |             "<article>\n"                         |
|                                               |             "\n"                                  |
|                                               |             "<p>Ideal for "                       |
|                                               |             "<strong>scraping</strong> "          |
|                                               |             "glass.</p>\n"                        |
|                                               |             "\n"                                  |
|                                               |             "<p>Durable and reusable.</p>\n"      |
|                                               |             "\n"                                  |
|                                               |             "</article>"                          |
|                                               |         ),                                        |
|                                               |     )                                             |
|                                               |                                                   |
+-----------------------------------------------+---------------------------------------------------+
| .. code-block:: html                          | .. code-block:: python                            |
|                                               |                                                   |
|     <div class="price">                       |     @field                                        |
|       <del>13,2 €</del>                       |     def price(self):                              |
|       <b>10,2 €</b>                           |         return self.css(".price b")               |
|     </div>                                    |                                                   |
|                                               |     @field                                        |
|                                               |     def regularPrice(self):                       |
|                                               |         return self.css(".price del")             |
|                                               |                                                   |
|                                               | .. code-block:: python                            |
|                                               |                                                   |
|                                               |     Product(                                      |
|                                               |         currencyRaw="€",                          |
|                                               |         price="10.20",                            |
|                                               |         regularPrice="13.20",                     |
|                                               |     )                                             |
|                                               |                                                   |
+-----------------------------------------------+---------------------------------------------------+
