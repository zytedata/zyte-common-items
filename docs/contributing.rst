============
Contributing
============

Set up your local Python environment via:

1. ``pip install -r requirements-dev.txt``

2. ``pre-commit install``

Now every time you perform a ``git commit``, these tools will run against the
staged files:

* ``black``
* ``isort``
* ``flake8``

You can also directly invoke ``pre-commit run --all-files`` to run them without
performing a commit.
