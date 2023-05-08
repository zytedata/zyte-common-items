.. _page-object-api:

===============
Page object API
===============

Product
=======

.. autoclass:: zyte_common_items.BaseProductPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.ProductPage(**kwargs)
   :show-inheritance:


Product list
============

.. autoclass:: zyte_common_items.BaseProductListPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.ProductListPage(**kwargs)
   :show-inheritance:

Product navigation
==================

.. autoclass:: zyte_common_items.BaseProductNavigationPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.ProductNavigationPage(**kwargs)
   :show-inheritance:

Business place
==============

.. autoclass:: zyte_common_items.BaseBusinessPlacePage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.BusinessPlacePage(**kwargs)
   :show-inheritance:

Real estate
===========

.. autoclass:: zyte_common_items.BaseRealEstatePage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.RealEstatePage(**kwargs)
   :show-inheritance:


Custom page objects
===================

Subclass :class:`~zyte_common_items.Page` to create your own page object
classes that rely on :class:`~zyte_common_items.HttpResponse`.

If you do not want :class:`~zyte_common_items.HttpResponse` as input, you can
inherit from :class:`~zyte_common_items.BasePage` instead.

.. autoclass:: zyte_common_items.BasePage(**kwargs)
   :show-inheritance:

   Base class for page object classes that has
   :class:`~zyte_common_items.RequestUrl` as a dependency.

   .. data:: metadata
      :type: zyte_common_items.Metadata

      Data extraction process metadata.

      :attr:`~zyte_common_items.Metadata.dateDownloaded` is set to the current
      UTC date and time.

      :attr:`~zyte_common_items.Metadata.probability` is set to ``1.0``.

   .. data:: url
      :type: str

      Main URL from which the data has been extracted.

.. autoclass:: zyte_common_items.Page(**kwargs)
   :show-inheritance:

   Base class for page object classes that has
   :class:`~zyte_common_items.HttpResponse` as a dependency.

   .. data:: metadata
      :type: zyte_common_items.Metadata

      Data extraction process metadata.

      :attr:`~zyte_common_items.Metadata.dateDownloaded` is set to the current
      UTC date and time.

      :attr:`~zyte_common_items.Metadata.probability` is set to ``1.0``.

   .. data:: url
      :type: str

      Main URL from which the data has been extracted.
