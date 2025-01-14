=========
Changelog
=========

0.27.0 (2025-01-DD)
===================

* The :class:`~zyte_common_items.pipelines.DropLowProbabilityItemPipeline` now
  supports nested items, i.e. :class:`dict` objects with items as values.

* Added an add-on to make :ref:`Scrapy configuration <scrapy-config>` easier.

* :class:`~zyte_common_items.Metadata` now also has all fields from
  :class:`~zyte_common_items.SerpMetadata`.

* Messages about dropped items, e.g. due to low probability, are now logged as
  information and not as warnings.

.. _0.26.2:

0.26.2 (2024-11-12)
===================

* | Fixed the package build missing all nested packages:
  | ``zyte_common_items.components``
  | ``zyte_common_items.items``
  | ``zyte_common_items.pages``

0.26.1 (2024-11-12)
===================

.. note:: This version was yanked, see :ref:`0.26.2`.

* Migrated from ``setup.py`` to ``pyproject.toml``.

* Fixed :meth:`Serp.from_dict <.Serp.from_dict>` returning an instance where
  :attr:`~.Serp.organicResults` list items were :class:`dict` instead of
  instances of :class:`~.SerpOrganicResult`.

0.26.0 (2024-11-11)
===================

* Added :class:`~.ForumThread` and related classes.

0.25.0 (2024-11-11)
===================

* Removed Python 3.8 support, added Python 3.13 support.

* **Backward-incompatible change:**
  :class:`~zyte_common_items.SearchRequestTemplatePage` now subclasses
  :class:`~zyte_common_items.Page`, adding a dependency on
  :class:`~web_poet.page_inputs.http.HttpResponse`. A new
  :class:`~zyte_common_items.BaseSearchRequestTemplatePage` that subclasses
  :class:`~zyte_common_items.BasePage` has been added as well.

  .. tip:: Where a dependency on
    :class:`~web_poet.page_inputs.http.HttpResponse` is not needed,
    :class:`~zyte_common_items.BaseSearchRequestTemplatePage` is a better
    replacement for the :class:`~zyte_common_items.SearchRequestTemplatePage`
    class from zyte-common-items 0.24.0 and lower, as it only depends on
    :class:`~web_poet.page_inputs.http.RequestUrl`.

* The ``keyword`` parameter of :meth:`SearchRequestTemplate.request()
  <zyte_common_items.SearchRequestTemplate.request>` has been deprecated in
  favor of ``query``. As a result, Jinja templates in
  :class:`~zyte_common_items.SearchRequestTemplate` field values should now use
  the ``query`` variable (e.g. ``{{ query|quote_plus }}``) instead of the
  ``keyword`` variable.

* Unexpected variables in Jinja templates of
  :class:`~zyte_common_items.SearchRequestTemplate` field values (e.g.
  ``{{ foo }}``), which used to be silently removed, will now trigger an
  :exc:`~jinja2.exceptions.UndefinedError` exception when calling
  :meth:`SearchRequestTemplate.request()
  <zyte_common_items.SearchRequestTemplate.request>`.

* Fixed coverage data generation during tests.

0.24.0 (2024-10-02)
===================

* Added :class:`~.JobPostingNavigation` and related classes.

0.23.0 (2024-09-19)
===================

* Added :class:`~.CustomAttributes` and related classes.

0.22.0 (2024-09-09)
===================

* Added :class:`~.Serp` and related classes.

0.21.0 (2024-08-27)
===================

* The new :func:`~zyte_common_items.processors.images_processor`, used by
  default in ``images`` fields, can convert a string, a list of strings or a
  list of dicts into an :class:`~zyte_common_items.Image` list. Strings become
  :attr:`Image.url <zyte_common_items.Image.url>`. Dicts get their ``url`` key
  mapped as :attr:`Image.url <zyte_common_items.Image.url>`.

* :func:`~zyte_common_items.processors.brand_processor` now converts strings
  into :class:`~zyte_common_items.Brand` objects with the input string as
  :attr:`Brand.name <zyte_common_items.Brand.name>`.

* :func:`~zyte_common_items.processors.price_processor` and
  :func:`~zyte_common_items.processors.simple_price_processor` now convert
  numeric values into strings with 2 decimal positions.

* :func:`~zyte_common_items.processors.metadata_processor` no longer assumes
  that the input metadata is not ``None``.

0.20.0 (2024-06-19)
===================

* Now fields of :ref:`auto page object classes <auto>` have ``auto_field`` set
  to ``True`` in their field metadata, to make it easier to check if a page
  object subclass is overriding a given field.

0.19.0 (2024-04-24)
===================

* Now requires ``attrs >= 22.2.0``.

* New deprecations:

  * ``zyte_common_items.components.request_list_processor`` (use
    ``zyte_common_items.processors.probability_request_list_processor``)
  * ``zyte_common_items.items.RequestListCaster`` (use
    ``zyte_common_items.converters.to_probability_request_list``)
  * ``zyte_common_items.util.metadata_processor`` (use
    ``zyte_common_items.processors.metadata_processor``)

* Added :class:`~.pipelines.DropLowProbabilityItemPipeline` that drops items
  with the ``probability`` value lower than a set threshold.

* Added the :class:`~.BaseMetadata`, :class:`~.ListMetadata`, and
  :class:`~.DetailsMetadata` classes (they were previously private).

* Added the :attr:`.ListMetadata.validationMessages` attribute.

* Added the :meth:`.ListMetadata.get_date_downloaded_parsed` method.

* Added the :mod:`zyte_common_items.converters` module with useful attrs
  converters.

* Reorganized the module structure.

* Documentation improvements.

* Test and CI fixes and improvements.

0.18.0 (2024-03-15)
===================

* Initial support for :ref:`request templates <request-templates>`, starting
  with search requests.

0.17.1 (2024-03-13)
===================

* Added Python 3.12 support.

* :func:`~zyte_common_items.processors.description_processor` and
  :func:`~zyte_common_items.processors.description_html_processor` now
  raise an exception when they receive an unsupported input value such as a
  non-HtmlElement node.

* Documentation improvements.

0.17.0 (2024-02-14)
===================

* Implement the ``zyte_common_items.ae`` module and the
  ``zyte_common_items.pipelines.AEPipeline`` item pipeline to make it easier to
  `migrate from Zyte Automatic Extraction to Zyte API automatic extraction
  <https://docs.zyte.com/zyte-api/migration/zyte/autoextract.html>`_.


0.16.0 (2024-02-06)
===================

* ``Auto``-prefixed versions of :ref:`page objects <page-objects>`, such as
  :meth:`~zyte_common_items.AutoProductPage`, now have all their fields defined
  as synchronous instead of asynchronous.

0.15.0 (2024-01-30)
===================

* Now requires ``zyte-parsers >= 0.5.0``.

* Added :class:`~.SocialMediaPost` and related classes.

* Added :class:`~.ProductFromListExtractor`,
  :class:`~.ProductFromListSelectorExtractor`,
  :class:`~.ProductVariantExtractor` and
  :class:`~.ProductVariantSelectorExtractor`.

* Added :func:`zyte_common_items.processors.rating_processor` and enabled it
  for the ``aggregateRating`` fields in the page classes for
  :class:`~.BusinessPlace` and :class:`~.Product`.

* Improved the documentation about the processors.

0.14.0 (2024-01-16)
===================

* Now requires ``zyte-parsers >= 0.4.0``.

* Added :func:`zyte_common_items.processors.gtin_processor` and enabled it for
  the ``gtin`` fields in the page classes for
  :class:`~zyte_common_items.Product`.

* Improved the API documentation.

0.13.0 (2023-11-09)
===================

* Added ``Auto``-prefixed versions of :ref:`page objects <page-objects>`, such
  as :meth:`~zyte_common_items.AutoProductPage`, that return data from Zyte API
  automatic extraction from their fields by default, and can be used to more
  easily override that data with custom parsing logic.


0.12.0 (2023-10-27)
===================

* Added :meth:`~zyte_common_items.base.ProbabilityMixin.get_probability` helper
  method in item classes (e.g. :class:`~zyte_common_items.Product`,
  :class:`~zyte_common_items.Article`) and
  :class:`~zyte_common_items.ProbabilityRequest`.


0.11.0 (2023-09-08)
===================

* Now requires ``clear-html >= 0.4.0``.

* Added :func:`zyte_common_items.processors.description_processor` and enabled
  it for the ``description`` fields in the page classes for
  :class:`~zyte_common_items.BusinessPlace`,
  :class:`~zyte_common_items.JobPosting`, :class:`~zyte_common_items.Product`
  and :class:`~zyte_common_items.RealEstate`.

* Added :func:`zyte_common_items.processors.description_html_processor` and
  enabled it for the ``descriptionHtml`` fields in the page classes for
  :class:`~zyte_common_items.JobPosting` and
  :class:`~zyte_common_items.Product`.

* Added default implementations for the ``description`` (in the page classes
  for :class:`~zyte_common_items.BusinessPlace`,
  :class:`~zyte_common_items.JobPosting`, :class:`~zyte_common_items.Product`
  and :class:`~zyte_common_items.RealEstate`) and ``descriptionHtml`` (in the
  page classes for :class:`~zyte_common_items.JobPosting` and
  :class:`~zyte_common_items.Product`) fields: if one of these fields is
  user-defined, another one will use it.

* :func:`~zyte_common_items.processors.price_processor` and
  :func:`~zyte_common_items.processors.simple_price_processor` now keep at
  least two decimal places when formatting the result.


0.10.0 (2023-08-24)
===================

* Now requires ``price-parser >= 0.3.4`` (a new dependency) and
  ``zyte-parsers >= 0.3.0`` (a version increase).

* Added :func:`zyte_common_items.processors.price_processor` and enabled
  it for the ``price`` fields.

* Added :func:`zyte_common_items.processors.simple_price_processor` and enabled
  it for the ``regularPrice`` fields.

* Added default implementations for the ``currency`` (uses the ``CURRENCY``
  attribute on the page class) and ``currencyRaw`` (uses the data extracted by
  the ``price`` field) fields.

0.9.0 (2023-08-03)
==================

* Now requires ``web-poet >= 0.14.0``.

* Fixed detection of the :class:`~.HasMetadata` base class.

0.8.0 (2023-07-27)
==================

* Updated minimum versions for the following requirements:

  * ``attrs >= 22.1.0``
  * ``web-poet >= 0.9.0``
  * ``zyte-parsers >= 0.2.0``

* Added :class:`~zyte_common_items.JobPosting` and related classes.

* Added :func:`zyte_common_items.processors.brand_processor` and enabled
  it for the ``brand`` fields.

* Added :meth:`zyte_common_items.Request.to_scrapy` to convert
  :class:`zyte_common_items.Request` instances to :class:`scrapy.http.Request`
  instances.

0.7.0 (2023-07-11)
==================

* Now requires ``zyte-parsers``.

* Added navigation classes: :class:`~zyte_common_items.ArticleNavigation`,
  :class:`~zyte_common_items.ProductNavigation`, the page classes that produce
  them, and other related classes.

* Improved the metadata field handling, also fixing some bugs:

  * Added :ref:`item-specific metadata classes <components-metadata>`. The
    ``metadata`` item fields were changed to use them.
  * **Backward-incompatible change**: the ``DateDownloadedMetadata`` class was
    removed. The item-specific ones are now used instead.
  * **Backward-incompatible change**:
    :class:`~zyte_common_items.ArticleFromList` no longer has a ``probability``
    field and instead has a ``metadata`` field like all other similar classes.
  * **Backward-incompatible change**: while in most items the old and the new
    type of the ``metadata`` field have the same fields, the one in
    :class:`~zyte_common_items.Article` now has ``probability``, the one in
    :class:`~zyte_common_items.ProductList` no longer has ``probability``, and
    the one in :class:`~zyte_common_items.ProductFromList` no longer has
    ``dateDownloaded``.
  * The default ``probability`` value is now ``1.0`` instead of ``None``.
  * Added the :class:`~zyte_common_items.HasMetadata` mixin which is used
    similarly to :class:`~web_poet.pages.Returns` to set the page metadata
    class.
  * Metadata objects assigned to the ``metadata`` fields of the items or
    returned from the ``metadata()`` methods of the pages are now converted to
    suitable classes.

* Added :func:`zyte_common_items.processors.breadcrumbs_processor` and enabled
  it for the ``breadcrumbs`` fields.

0.6.0 (2023-07-05)
==================

* Added :class:`~zyte_common_items.Article` and
  :class:`~zyte_common_items.ArticleList`.

* Added support for Python 3.11 and dropped support for Python 3.7.

0.5.0 (2023-05-10)
==================

* Now requires ``itemadapter >= 0.8.0``.

* Added :class:`~zyte_common_items.RealEstate`.

* Added the :meth:`zyte_common_items.BasePage.no_item_found` and
  :meth:`zyte_common_items.Page.no_item_found` methods.

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
