SQLAlchemy Diff
===============

.. pull-quote::

    Compare and generate a diff between two databases using SQLAlchemy's
    inspection API.


Running tests
-------------

Makefile targets that can be used to run the tests.

Test databases will be created, used during the tests and destroyed afterwards.

Example of usage:

.. code-block:: shell

    $ # using default settings
    $ pytest test
    $ make test
    $ make coverage

    $ # or overridding the database URI
    $ pytest test --test-db-url=mysql+mysqlconnector://root:password@localhost:3306/sqlalchemydiff
    $ make test ARGS="--test-db-url=mysql+mysqlconnector://root:password@localhost:3306/sqlalchemydiff"
    $ make coverage ARGS="--lf -x -vv --test-db-url=mysql+mysqlconnector://root:password@localhost:3306/sqlalchemydiff"


License
-------

Apache 2.0. See LICENSE for details.
