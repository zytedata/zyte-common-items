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

* Documentation: https://zyte-common-items.readthedocs.io/
* Source code: https://github.com/zytedata/zyte-common-items
* Issue tracker: https://github.com/zytedata/zyte-common-items/issues

.. _`scrapy-poet`: https://scrapy-poet.readthedocs.io/en/stable/
.. _`scrapy-autoextract`: https://github.com/scrapinghub/scrapy-autoextract
.. _`python-zyte-api`: https://github.com/zytedata/python-zyte-api
.. _`Zyte Data API`: https://docs.zyte.com/zyte-api/get-started.html
.. _`Unified Schema`: https://docs.zyte.com/unified-schema.html


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
