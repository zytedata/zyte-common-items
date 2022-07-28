.. _items:

=====
Items
=====

Product
=======

.. class:: zyte_common_items.Product(**kwargs)
.. autoclass:: zyte_common_items.items.Product(**kwargs)
   :members:
   :inherited-members:

.. class:: zyte_common_items.ProductVariant(**kwargs)
.. autoclass:: zyte_common_items.items.ProductVariant(**kwargs)
   :members:
   :inherited-members:

Product List
============

.. class:: zyte_common_items.ProductList(**kwargs)
.. autoclass:: zyte_common_items.items.ProductList(**kwargs)
   :members:
   :inherited-members:

.. class:: zyte_common_items.ProductFromList(**kwargs)
.. autoclass:: zyte_common_items.items.ProductFromList(**kwargs)
   :members:
   :inherited-members:


Custom items
============

Subclass :class:`~zyte_common_items.base.Item` to create your own item classes.

.. class:: zyte_common_items.Item(**kwargs)
.. autoclass:: zyte_common_items.base.Item(**kwargs)
   :members:

   .. attribute:: _unknown_fields_dict
      :type: dict

      Contains unknown attributes fed into the item through :meth:`from_dict`
      or :meth:`from_list`.
