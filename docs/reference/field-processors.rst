.. _processor-api:

===================
Field processor API
===================

API reference of provided :ref:`field processors <processors>`.

.. _field-processor-map:

Field mapping
=============

The following table indicates which fields use which processors by default in
:ref:`built-in page object classes <page-objects>`:

==================================== ====================================
Fields                               Default processor
==================================== ====================================
``aggregateRating``                  :func:`~.rating_processor`
``brand``                            :func:`~.brand_processor`
``breadcrumbs``                      :func:`~.breadcrumbs_processor`
``description`` (excluding articles) :func:`~.description_processor`
``descriptionHtml``                  :func:`~.description_html_processor`
``gtin``                             :func:`~.gtin_processor`
``price``                            :func:`~.price_processor`
``regularPrice``                     :func:`~.simple_price_processor`
==================================== ====================================


Built-in field processors
=========================

.. autofunction:: zyte_common_items.processors.brand_processor

.. autofunction:: zyte_common_items.processors.breadcrumbs_processor

.. autofunction:: zyte_common_items.processors.description_processor

.. autofunction:: zyte_common_items.processors.description_html_processor

.. autofunction:: zyte_common_items.processors.gtin_processor

.. autofunction:: zyte_common_items.processors.price_processor

.. autofunction:: zyte_common_items.processors.rating_processor

.. autofunction:: zyte_common_items.processors.simple_price_processor
