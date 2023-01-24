=========
Changelog
=========

TBD
===

* Use ``web_poet.Unset`` sentinel value which represents fields which hasn't been
  assigned with any value. This is to differentiate values which are ``None``.

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
