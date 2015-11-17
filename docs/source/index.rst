SQLAlchemy Diff
===============

.. pull-quote::

    Compare and generate a diff between two databases using SQLAlchemy's
    inspection API


PyTest Example
--------------

Comparing two schemas is easy. You can verify they are the same like
this:

.. literalinclude:: ../../test/endtoend/test_example.py
    :lines: 6,8,9,13-22


You can also verify that they are different:

.. literalinclude:: ../../test/endtoend/test_example.py
    :lines: 25-33


You will get back a ``result`` object: ``result.is_match`` will be
``True`` when the two schemas are the same, and ``False`` when they are
different.

When two schemas don't match, you can call ``result.dump_errors()`` to
save all the differences between them to a JSON file that will look
like this:


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

    $ pip install sqlalchemy-diff
