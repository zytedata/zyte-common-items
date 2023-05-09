=========
Changelog
=========

0.5.0 (YYYY-MM-DD)
==================

* Now requires ``itemadapter >= 0.8.0``.

* Added :class:`~zyte_common_items.RealEstate`.

* Added the :meth:`zyte_common_items.BasePage.no_item_found` method.

* Improved the error message for invalid input.

* Added :class:`~zyte_common_items.ZyteItemKeepEmptyAdapter` and documented how
  to use it and :class:`~zyte_common_items.ZyteItemAdapter` in custom
  subclasses of :class:`itemadapter.ItemAdapter`.

0.4.0 (2023-03-27)
==================

* Added support for business places.


0.3.1 (2023-03-17)
==================

* Fixed fields from :class:`~zyte_common_items.BasePage` subclasses leaking
  across subclasses.
  (`#29 <https://github.com/zytedata/zyte-common-items/pull/29>`_,
  `#30 <https://github.com/zytedata/zyte-common-items/pull/30>`_)

* Improved how the :meth:`~zyte_common_items.Item.from_dict` and
  :meth:`~zyte_common_items.Item.from_list` methods report issues in the input
  data. (`#25 <https://github.com/zytedata/zyte-common-items/pull/25>`_)


0.3.0 (2023-02-03)
==================

* Added :ref:`page object classes <page-objects>` for e-commerce product detail
  and product list pages.


0.2.0 (2022-09-22)
==================

* Supports ``web_poet.RequestUrl`` and ``web_poet.ResponseUrl`` and
  automatically convert them into a string on URL fields like
  ``Product.url``.
* Bumps the ``web_poet`` dependency version from ``0.4.0`` to ``0.5.0``
  which fully supports type hints using the ``py.typed`` marker.
* This package now also supports type hints using the ``py.typed`` marker.
  This means mypy would properly use the type annotations in the items
  when using it in your project.
* Minor improvements in tests and annotations.


0.1.0 (2022-07-29)
==================

Initial release.
