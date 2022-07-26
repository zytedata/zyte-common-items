=====
Setup
=====

Installation
============

.. code-block:: bash

    pip install zyte-common-items


.. _configuration:

Configuration
=============

As early as possible in your code, prepend
:class:`~zyte_common_items.ZyteItemAdapter` to
itemadapter.ItemAdapter.ADAPTER_CLASSES_::

    from itemadapter import ItemAdapter
    from zyte_common_items import ZyteItemAdapter

    ItemAdapter.ADAPTER_CLASSES.appendleft(ZyteItemAdapter)

.. _itemadapter.ItemAdapter.ADAPTER_CLASSES: https://github.com/scrapy/itemadapter#class-attribute-adapter_classes-collectionsdeque