.. _item-api:

========
Item API
========

Product
=======

.. autoclass:: zyte_common_items.Product(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.ProductVariant(**kwargs)
   :members:
   :inherited-members:

Product list
============

.. autoclass:: zyte_common_items.ProductList(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.ProductFromList(**kwargs)
   :members:
   :inherited-members:

Product navigation
==================

.. autoclass:: zyte_common_items.ProductNavigation(**kwargs)
   :members:
   :inherited-members:

Article
=======

.. autoclass:: zyte_common_items.Article(**kwargs)
   :members:
   :inherited-members:

Article list
============

.. autoclass:: zyte_common_items.ArticleList(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.ArticleFromList(**kwargs)
   :members:
   :inherited-members:

Article navigation
==================

.. autoclass:: zyte_common_items.ArticleNavigation(**kwargs)
   :members:
   :inherited-members:

Business place
==============

.. autoclass:: zyte_common_items.BusinessPlace(**kwargs)
   :members:
   :inherited-members:

Real estate
===========

.. autoclass:: zyte_common_items.RealEstate(**kwargs)
   :members:
   :inherited-members:

Job posting
===========

.. autoclass:: zyte_common_items.JobPosting(**kwargs)
   :members:
   :inherited-members:

Custom items
============

Subclass :class:`~zyte_common_items.Item` to create your own item classes.

.. autoclass:: zyte_common_items.Item(**kwargs)
   :members:

   .. attribute:: _unknown_fields_dict
      :type: dict

      Contains unknown attributes fed into the item through :meth:`from_dict`
      or :meth:`from_list`.
