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
|     <span class="gtin">                       |     @field                                        |
|       978-1-933624-34-1                       |     def gtin(self):                               |
|     </span>                                   |         return self.css(".gtin")                  |
|                                               |                                                   |
|                                               | .. code-block:: python                            |
|                                               |                                                   |
|                                               |     Product(                                      |
|                                               |         gtin=[                                    |
|                                               |             ("isbn13", "9781933624341"),          |
|                                               |         ],                                        |
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
