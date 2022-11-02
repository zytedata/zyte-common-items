.. _page-object-api:

===============
Page object API
===============

Product
=======

.. autoclass:: zyte_common_items.ProductPage(**kwargs)
   :show-inheritance:


Product List
============

.. autoclass:: zyte_common_items.ProductListPage(**kwargs)
   :show-inheritance:


Custom page objects
===================

Subclass :class:`~zyte_common_items.Page` to create your own page object
classes.

.. autoclass:: zyte_common_items.Page(**kwargs)
   :show-inheritance:

   .. data:: metadata
      :type: zyte_common_items.Metadata

      Data extraction process metadata.

      :attr:`~zyte_common_items.Metadata.dateDownloaded` is set to the current
      UTC date and time.

      :attr:`~zyte_common_items.Metadata.probability` is not set.

   .. data:: url
      :type: web_poet.page_inputs.http.ResponseUrl

      Main URL from which the data has been extracted.
