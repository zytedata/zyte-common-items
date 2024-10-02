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

.. autoclass:: zyte_common_items.AutoProductPage(**kwargs)
   :show-inheritance:

Product list
============

.. autoclass:: zyte_common_items.BaseProductListPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.ProductListPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.AutoProductListPage(**kwargs)
   :show-inheritance:

Product navigation
==================

.. autoclass:: zyte_common_items.BaseProductNavigationPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.ProductNavigationPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.AutoProductNavigationPage(**kwargs)
   :show-inheritance:

Article
=======

.. autoclass:: zyte_common_items.BaseArticlePage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.ArticlePage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.AutoArticlePage(**kwargs)
   :show-inheritance:


Article list
============

.. autoclass:: zyte_common_items.BaseArticleListPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.ArticleListPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.AutoArticleListPage(**kwargs)
   :show-inheritance:


Article navigation
==================

.. autoclass:: zyte_common_items.BaseArticleNavigationPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.ArticleNavigationPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.AutoArticleNavigationPage(**kwargs)
   :show-inheritance:

Business place
==============

.. autoclass:: zyte_common_items.BaseBusinessPlacePage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.BusinessPlacePage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.AutoBusinessPlacePage(**kwargs)
   :show-inheritance:

Real estate
===========

.. autoclass:: zyte_common_items.BaseRealEstatePage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.RealEstatePage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.AutoRealEstatePage(**kwargs)
   :show-inheritance:

Job posting
===========

.. autoclass:: zyte_common_items.BaseJobPostingPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.JobPostingPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.AutoJobPostingPage(**kwargs)
   :show-inheritance:

Job posting navigation
======================

.. autoclass:: zyte_common_items.BaseJobPostingNavigationPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.JobPostingNavigationPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.AutoJobPostingNavigationPage(**kwargs)
   :show-inheritance:

Search engine results
=====================

.. autoclass:: zyte_common_items.BaseSerpPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.SerpPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.AutoSerpPage(**kwargs)
   :show-inheritance:

Social media post
=================

.. autoclass:: zyte_common_items.BaseSocialMediaPostPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.SocialMediaPostPage(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.AutoSocialMediaPostPage(**kwargs)
   :show-inheritance:

Request templates
=================

.. autoclass:: zyte_common_items.SearchRequestTemplatePage(**kwargs)
   :show-inheritance:

.. _mixins:

Mixins
======

.. autoclass:: zyte_common_items.pages.DescriptionMixin

   .. data:: description
      :type: str

      Plain-text description. The default implementation makes it from the
      ``descriptionHtml`` field if that is user-defined.

   .. data:: descriptionHtml
      :type: str

      HTML description. The default implementation makes it from the
      ``description`` field if that is user-defined.

.. autoclass:: zyte_common_items.pages.PriceMixin

   .. data:: currency
      :type: str

      Price currency ISO 4217 alphabetic code (e.g. ``"USD"``). The default
      implementation returns ``self.CURRENCY`` if this attribute is defined.

   .. data:: currencyRaw
      :type: str

      Price currency as it appears on the webpage (no post-processing), e.g.
      ``"$"``. The default implementation uses the data extracted by
      :func:`~zyte_common_items.processors.price_processor` from the ``price``
      field.

Custom page objects
===================

Subclass :class:`~zyte_common_items.Page` to create your own page object
classes that rely on :class:`~web_poet.page_inputs.http.HttpResponse`.

If you do not want :class:`~web_poet.page_inputs.http.HttpResponse` as input,
you can inherit from :class:`~zyte_common_items.BasePage` instead.

Your subclasses should also inherit generic classes
:class:`web_poet.pages.Returns` and :class:`zyte_common_items.HasMetadata` to
indicate their item and metadata classes.

.. autoclass:: zyte_common_items.pages.base._BasePage(**kwargs)

.. autoclass:: zyte_common_items.BasePage(**kwargs)
   :show-inheritance:
   :members: no_item_found

   .. data:: metadata

      Data extraction process metadata.

      :attr:`~zyte_common_items.Metadata.dateDownloaded` is set to the current
      UTC date and time.

      :attr:`~zyte_common_items.Metadata.probability` is set to ``1.0``.

   .. data:: url
      :type: str

      Main URL from which the data has been extracted.

.. autoclass:: zyte_common_items.Page(**kwargs)
   :show-inheritance:
   :members: no_item_found

   .. data:: metadata
      :type: zyte_common_items.Metadata

      Data extraction process metadata.

      :attr:`~zyte_common_items.Metadata.dateDownloaded` is set to the current
      UTC date and time.

      :attr:`~zyte_common_items.Metadata.probability` is set to ``1.0``.

   .. data:: url
      :type: str

      Main URL from which the data has been extracted.

.. autoclass:: zyte_common_items.HasMetadata
