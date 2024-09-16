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

.. autoclass:: zyte_common_items.ProductMetadata(**kwargs)
   :members: dateDownloaded, probability, validationMessages

Product list
============

.. autoclass:: zyte_common_items.ProductList(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.ProductFromList(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.ProductListMetadata(**kwargs)
   :members: dateDownloaded, validationMessages

Product navigation
==================

.. autoclass:: zyte_common_items.ProductNavigation(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.ProductNavigationMetadata(**kwargs)
   :members: dateDownloaded, validationMessages

Article
=======

.. autoclass:: zyte_common_items.Article(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.ArticleMetadata(**kwargs)
   :members: dateDownloaded, probability, validationMessages


Article list
============

.. autoclass:: zyte_common_items.ArticleList(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.ArticleFromList(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.ArticleListMetadata(**kwargs)
   :members: dateDownloaded, validationMessages

Article navigation
==================

.. autoclass:: zyte_common_items.ArticleNavigation(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.ArticleNavigationMetadata(**kwargs)
   :members: dateDownloaded, validationMessages

Business place
==============

.. autoclass:: zyte_common_items.BusinessPlace(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.BusinessPlaceMetadata(**kwargs)
   :members: dateDownloaded, probability, searchText, validationMessages


Real estate
===========

.. autoclass:: zyte_common_items.RealEstate(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.RealEstateMetadata(**kwargs)
   :members: dateDownloaded, probability, validationMessages

Job posting
===========

.. autoclass:: zyte_common_items.JobPosting(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.JobPostingMetadata(**kwargs)
   :members: dateDownloaded, probability, validationMessages


Social media post
=================

.. autoclass:: zyte_common_items.SocialMediaPost(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.SocialMediaPostMetadata(**kwargs)
   :members: dateDownloaded, probability, searchText, validationMessages

.. _request-template-api:

Search Request templates
========================

.. autoclass:: zyte_common_items.SearchRequestTemplate(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.SearchRequestTemplateMetadata(**kwargs)
   :members: dateDownloaded, probability, validationMessages

Custom attributes
=================

.. autoclass:: zyte_common_items.CustomAttributesValues(**kwargs)
   :show-inheritance:

.. autoclass:: zyte_common_items.CustomAttributesMetadata(**kwargs)
   :members:
   :inherited-members:

.. autoclass:: zyte_common_items.CustomAttributes(**kwargs)
   :members:
   :inherited-members:

Custom items
============

Subclass :class:`~zyte_common_items.Item` to create your own item classes.

.. autoclass:: zyte_common_items.base.ProbabilityMixin(**kwargs)
   :members:

.. autoclass:: zyte_common_items.Item(**kwargs)
   :members:
   :inherited-members:

   .. attribute:: _unknown_fields_dict
      :type: dict

      Contains unknown attributes fed into the item through :meth:`from_dict`
      or :meth:`from_list`.
