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

To allow itemadapter_ users, like Scrapy_, to interact with :ref:`items
<items>`, prepend :class:`~zyte_common_items.ZyteItemAdapter` or
:class:`~zyte_common_items.ZyteKeepEmptyAdapter` to
itemadapter.ItemAdapter.ADAPTER_CLASSES_ as early as possible in your code::

    from itemadapter import ItemAdapter
    from zyte_common_items import ZyteItemAdapter

    ItemAdapter.ADAPTER_CLASSES.appendleft(ZyteItemAdapter)


Alternatively, make your own subclass of :class:`itemadapter.ItemAdapter`::

    from itemadapter import ItemAdapter
    from zyte_common_items import ZyteItemAdapter

    class MyItemAdapter(ItemAdapter):
        ADAPTER_CLASSES = deque([ZyteItemAdapter]) + ItemAdapter.ADAPTER_CLASSES

Now you can use ``MyItemAdapter`` where you would use
:class:`itemadapter.ItemAdapter`.

.. _itemadapter: https://github.com/scrapy/itemadapter#itemadapter
.. _itemadapter.ItemAdapter.ADAPTER_CLASSES: https://github.com/scrapy/itemadapter#class-attribute-adapter_classes-collectionsdeque
.. _Scrapy: https://scrapy.org/
