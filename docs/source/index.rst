SQLAlchemy Diff
===============

.. pull-quote::

    Compare two database schemas using SQLAlchemy.


PyTest Example
--------------

This is how you can use the library to verify that two schemas are
the same:

.. literalinclude:: ../testing/test_example.py
    :lines: 6,8,9,13-22
    :emphasize-lines: 11


You can also make sure that two schemas are different:

.. literalinclude:: ../testing/test_example.py
    :lines: 25-33
    :emphasize-lines: 7


If your test fails, you can dump the errors to a file by just adding
the following line of code:

.. code-block:: Python

    result.dump_errors()


That will dump the errors dict to a JSON file that looks like this:

.. code-block:: JSON

    {
        'tables': {
            'left_only': ['addresses'],
            'right_only': ['roles']
        },
        'tables_data': {
            'employees': {
                'columns': {
                    'left_only': [
                        {
                            'default': None,
                            'name': 'favourite_meal',
                            'nullable': False,
                            'type': "ENUM('meat','vegan')"
                        }
                    ],
                    'right_only': [
                        {
                            'autoincrement': False,
                            'default': None,
                            'name': 'role_id',
                            'nullable': False,
                            'type': 'INTEGER(11)'
                        },
                        {
                            'autoincrement': False,
                            'default': None,
                            'name': 'number_of_pets',
                            'nullable': False,
                            'type': 'INTEGER(11)'
                        },
                    ]
                },
                'foreign_keys': { ... },
                'primary_keys': { ... },
                'indexes': { .. }
            },
            'phone_numbers': { ... }
        },
        'uris': {
            'left': "your left URI",
            'right': "your right URI",
        }
    }


Using unittest
--------------

If you prefer, you can use unittest:

.. literalinclude:: ../testing/test_unittest.py
    :lines: 2-47


Features
--------

Currently the library can detect the following differences:

- Differences in **Tables**
- Differences in **Primary Keys** for a common table
- Differences in **Foreign Keys** for a common table
- Differences in **Indexes** for a common table
- Differences in **Columns** for a common table


Installation
------------

.. code-block:: bash

    $ pip install alembic-verify


Full Example
------------

:ref:`Here <full_example>` you can find a full example on how to test
two databases which are different.
