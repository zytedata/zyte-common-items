=====
Setup
=====

Installation
============

.. code-block:: bash

    pip install zyte-common-items


.. _configuration:
.. _scrapy-config:

Scrapy configuration
====================

If you use Scrapy, zyte-common-items provides some functionality that needs
configuring:

-   If using Scrapy_ 2.10 or higher, enable the add-on:

    .. code-block:: python
        :caption: settings.py

        ADDONS = {
            "zyte_common_items.Addon": 400,
        }

    The add-on:

    -   Appends :class:`~zyte_common_items.ZyteItemAdapter` to
        itemadapter.ItemAdapter.ADAPTER_CLASSES_ if neither
        :class:`~zyte_common_items.ZyteItemAdapter` nor
        :class:`~zyte_common_items.ZyteItemKeepEmptyAdapter` are already there.

    -   Sets :setting:`LOG_FORMATTER <scrapy:LOG_FORMATTER>` to
        :class:`~zyte_common_items.log_formatters.ZyteLogFormatter` if a custom
        log formatter is not already set (i.e. with ``addon`` priority, see
        :attr:`~scrapy.settings.SETTINGS_PRIORITIES`).

-   If using Scrapy_ 2.9 or lower, apply those configurations manually as
    needed.


.. _itemadapter-config:

itemadapter configuration
=========================

To allow itemadapter_ to interact with :ref:`items <items>`, prepend
:class:`~zyte_common_items.ZyteItemAdapter` or
:class:`~zyte_common_items.ZyteItemKeepEmptyAdapter` to
itemadapter.ItemAdapter.ADAPTER_CLASSES_ as early as possible in your code::

    from itemadapter import ItemAdapter
    from zyte_common_items import ZyteItemAdapter

    ItemAdapter.ADAPTER_CLASSES.appendleft(ZyteItemAdapter)


Alternatively, make your own subclass of :class:`itemadapter.ItemAdapter`::

    from collections import deque

    from itemadapter import ItemAdapter
    from zyte_common_items import ZyteItemAdapter

    class MyItemAdapter(ItemAdapter):
        ADAPTER_CLASSES = deque([ZyteItemAdapter]) + ItemAdapter.ADAPTER_CLASSES

Now you can use ``MyItemAdapter`` where you would use
:class:`itemadapter.ItemAdapter`.

.. _itemadapter: https://github.com/scrapy/itemadapter#itemadapter
.. _itemadapter.ItemAdapter.ADAPTER_CLASSES: https://github.com/scrapy/itemadapter#class-attribute-adapter_classes-collectionsdeque
.. _Scrapy: https://scrapy.org/
