============
Contributing
============

You can contribute to this project with code.

To prepare your development environment:

#.  Clone the `source code`_:

    .. code-block:: bash

        git clone https://github.com/zytedata/zyte-common-items.git
        cd zyte-common-items

#.  Create and activate a :ref:`Python virtual environment <tut-venv>`:

    .. code-block:: bash

        python -m venv venv
        . venv/bin/activate

#.  Install the packages needed for development:

    .. code-block:: bash

        pip install -r requirements-dev.txt

#.  Configure our `Git pre-commit hooks`_:

    .. code-block:: bash

        pre-commit install

You can search our `issue tracker`_ for pending work, and start a pull request
for any pending issue that is not actively being worked on already, no need to
ask for permission first.

If there is something else you wish to implement, please open an issue first to
open a discussion about it, before you work on a pull request. You probably do
not want to spend time on a pull request to later be told that the feature does
not fit the project plans in the first place.


.. _Git pre-commit hooks: https://pre-commit.com/
.. _issue tracker: https://github.com/zytedata/zyte-common-items/issues
.. _source code: https://github.com/zytedata/zyte-common-items
