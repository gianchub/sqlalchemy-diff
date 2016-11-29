SQLAlchemy Diff
===============

.. pull-quote::

    Compare and generate a diff between two databases using SQLAlchemy's
    inspection API.


Documentation
-------------

See `<http://sqlalchemy-diff.readthedocs.org>`_.


Running tests
-------------

Tests are written with pytest. Makefile targets to invoke tests are also provided for convenience.

Test databases will be created, used during the tests and destroyed afterwards.

Example:

.. code-block:: shell

    $ # using default settings
    $ make test

    # or
    $ py.test test

    $ # overridding the database URI
    $ py.test test --test-db-url=mysql+mysqlconnector://root:password@localhost:3306/sqlalchemydiff

    # or
    $ make test ARGS="--test-db-url=mysql+mysqlconnector://root:password@localhost:3306/sqlalchemydiff"

    # providing other pytest args via Make
    $ make test ARGS="--lf -x -vv"


License
-------

Apache 2.0. See LICENSE for details.
