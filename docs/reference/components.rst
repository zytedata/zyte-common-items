.. _components:

==========
Components
==========

These classes are used to map data within :ref:`items <items>`, and are not
tied to any specific item type.

.. autoclass:: zyte_common_items.AdditionalProperty(**kwargs)
   :members:

.. autoclass:: zyte_common_items.Address(**kwargs)
   :members:

.. autoclass:: zyte_common_items.AggregateRating(**kwargs)
   :members:

.. autoclass:: zyte_common_items.Amenity(**kwargs)
   :members:

.. autoclass:: zyte_common_items.Audio(**kwargs)
   :members: url

.. autoclass:: zyte_common_items.Author(**kwargs)
   :members:

.. autoclass:: zyte_common_items.BaseSalary(**kwargs)
   :members: raw, valueMin, valueMax, rateType, currency, currencyRaw

.. autoclass:: zyte_common_items.Brand(**kwargs)
   :members:

.. autoclass:: zyte_common_items.Breadcrumb(**kwargs)
   :members:

.. autoclass:: zyte_common_items.Gtin(**kwargs)
   :members:

.. autoclass:: zyte_common_items.Header(**kwargs)
   :members:

.. autoclass:: zyte_common_items.HiringOrganization(**kwargs)
   :members: name, nameRaw, id

.. autoclass:: zyte_common_items.Image(**kwargs)
   :members: url

.. autoclass:: zyte_common_items.JobLocation(**kwargs)
   :members: raw

.. autoclass:: zyte_common_items.Link(**kwargs)
   :members:

.. autoclass:: zyte_common_items.NamedLink(**kwargs)
   :members:

.. autoclass:: zyte_common_items.OpeningHoursItem(**kwargs)
   :members:

.. autoclass:: zyte_common_items.ParentPlace(**kwargs)
   :members:

.. autoclass:: zyte_common_items.ProbabilityMetadata(**kwargs)
   :members:

.. autoclass:: zyte_common_items.ProbabilityRequest(**kwargs)
   :members:

.. autoclass:: zyte_common_items.Reactions(**kwargs)
   :members:

.. autoclass:: zyte_common_items.RealEstateArea(**kwargs)
   :members:

.. autoclass:: zyte_common_items.Request(**kwargs)
   :members:

.. autoclass:: zyte_common_items.SerpOrganicResult(**kwargs)
   :members:

.. autoclass:: zyte_common_items.SocialMediaPostAuthor(**kwargs)
   :members:

.. autoclass:: zyte_common_items.StarRating(**kwargs)
   :members:

.. autoclass:: zyte_common_items.Url(**kwargs)
   :members: url
.. autoclass:: zyte_common_items.Video(**kwargs)
   :members: url

.. _components-metadata:

Item metadata components
========================

.. autoclass:: zyte_common_items.Metadata(**kwargs)
   :show-inheritance:
   :members: dateDownloaded, probability, searchText, validationMessages

.. autoclass:: zyte_common_items.components.metadata.ProbabilityMetadata(**kwargs)
   :show-inheritance:
   :members: probability

.. autoclass:: zyte_common_items.components.metadata.ListMetadata(**kwargs)
   :show-inheritance:
   :members: dateDownloaded, validationMessages, get_date_downloaded_parsed

.. autoclass:: zyte_common_items.components.metadata.DetailsMetadata(**kwargs)
   :show-inheritance:
   :members: probability, dateDownloaded, validationMessages, get_date_downloaded_parsed

.. autoclass:: zyte_common_items.components.metadata.BaseMetadata(**kwargs)
   :show-inheritance:
   :members: cast


Typing
======

.. autoclass:: zyte_common_items.components.metadata.MetadataT()

.. autoclass:: zyte_common_items.components.request.RequestT()
