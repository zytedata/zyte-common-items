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

Product List
============

.. autoclass:: zyte_common_items.ProductList(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.ProductFromList(**kwargs)
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
