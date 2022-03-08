=================
zyte-common-items
=================

.. image:: https://img.shields.io/pypi/v/zyte-common-items.svg
   :target: https://pypi.python.org/pypi/zyte-common-items
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/zyte-common-items.svg
   :target: https://pypi.python.org/pypi/zyte-common-items
   :alt: Supported Python Versions

.. image:: https://github.com/zytedata/zyte-common-items/workflows/tox/badge.svg
   :target: https://github.com/zytedata/zyte-common-items/actions
   :alt: Build Status

.. image:: https://codecov.io/github/zytedata/zyte-common-items/coverage.svg?branch=master
   :target: https://codecov.io/gh/zytedata/zyte-common-items
   :alt: Coverage report

``zyte-common-items`` contains common item definitions used inside **Zyte**.
Such items can be extracted automatically using `Zyte Data API`_ and `Unified Schema`_.

License is BSD 3-clause.

* Source code: https://github.com/zytedata/zyte-common-items
* Issue tracker: https://github.com/zytedata/zyte-common-items/issues

.. _`Zyte Data API`: https://docs.zyte.com/zyte-api/get-started.html
.. _`Unified Schema`: https://docs.zyte.com/unified-schema.html


Quick Start
***********

Installation
============

.. code-block::

    pip install zyte-common-items

Requires **Python 3.7+**.


Usage
=====

You can choose different flavors of schema like ``zyte_data_api`` or ``unified_schema``.

You can instantiate the data container using any ``dict``-like data via the ``from_dict()`` method. An example use case would be reading the JSON data response from an API which can easily be converted into a ``dict``.

.. code-block:: python

    from zyte_common_items import zyte_data_api as zda

    data = {
        "url": "https://example.com/articles/fashion",
        "paginationNext": {
            "url": "https://example.com/articles/fashion?page=2",
            "text": "Next Page"
        },
        "articles": [
            {"url": "https://example.com/articles/fashion/article-1", "headline": "Article 1"},
            {"url": "https://example.com/articles/fashion/article-2", "headline": "Article 2"}
        ]
    }
    article_list = zda.ArticleList.from_dict(data)    

The amazing feature here is that the ``from_dict()`` method creates the correct sub-item class instance from the main item (see ``PaginationLink`` and ``ArticleFromList`` below).

.. code-block:: python

    print(article_list.url)
    # https://example.com/articles/fashion    

    print(article_list.paginationNext)
    # PaginationLink(url='https://example.com/articles/fashion?page=2', text='Next Page')    

    print(article_list.paginationPrevious)
    # None    

    print(len(article_list.articles))
    # 2    

    print(article_list.articles[0])
    # ArticleFromList(url='https://example.com/articles/fashion/article-1', headline='Article 1', articleBody=None, datePublished=None, datePublishedRaw=None, authors=[], mainImage=None, images=[], probability=1.0, inLanguage=None)

In addition, any unknown fields that are not part of the schema **won't cause an error**. This is intended to be compatible with field changes in the future which could cause backwards incompatibility. Instead, any unknown fields will be placed inside the ``_unknown_fields_dict`` attribute for safekeeping `(see example below)`:

.. code-block:: python

    from zyte_common_items import zyte_data_api as zda

    data = {
        "url": "https://example.com/articles/fashion",
        "unknown_field": True
    }
    article_list = zda.ArticleList.from_dict(data)

    print(article_list._unknown_fields_dict)
    # {'unknown_field': True}

However, if a known field has an incorrect data structure, an ``AttributeError`` is raised:

.. code-block:: python

    from zyte_common_items import zyte_data_api as zda

    data = {
        "url": "https://example.com/articles/fashion",
        "paginationNext": "incorrect data format on this field"
    }
    article_list = zda.ArticleList.from_dict(data)
    # raises an AttributeError

Lastly, you can create items in bulk using the ``from_list`` method (see below). This can be especially useful if you're processing lots of items from an API, file, database, etc.

.. code-block:: python

    from zyte_common_items import zyte_data_api as zda

    data_list = [
        {"url": "https://example.com/articles/fashion/article-1", "headline": "article-1"},
        {"url": "https://example.com/articles/fashion/article-2", "headline": "article-2"},
        {"url": "https://example.com/articles/fashion/article-3", "headline": "article-3"},
        {"url": "https://example.com/articles/fashion/article-4", "headline": "article-4"}
    ]
    articles = zda.Article.from_list(data_list)

    print(articles)
    #[Article(url='https://example.com/articles/fashion/article-1', headline='article-1', ...),
    # Article(url='https://example.com/articles/fashion/article-2', headline='article-2', ...),
    # Article(url='https://example.com/articles/fashion/article-3', headline='article-3', ...),
    # Article(url='https://example.com/articles/fashion/article-4', headline='article-4', ...)]


Developing
**********

Setup your local Python environment via:

1. ``pip install -r requirements-dev.txt``
2. ``pre-commit install``

Now everytime you perform a ``git commit``, these tools will run against the staged files:

* ``black``
* ``isort``
* ``flake8``

You can also directly invoke ``pre-commit run --all-files`` to run them without performing a commit.
