# -*- coding: utf-8 -*-
import json

import pytest

from sqlalchemydiff.comparer import compare
from sqlalchemydiff.util import (
    destroy_database,
    get_temporary_uri,
    new_db,
    prepare_schema_from_models,
)
from .models_left import Base as Base_left
from .models_right import Base as Base_right

from test import assert_items_equal


@pytest.fixture(scope="module")
def uri_left(db_uri):
    return get_temporary_uri(db_uri)


@pytest.fixture(scope="module")
def uri_right(db_uri):
    return get_temporary_uri(db_uri)


@pytest.yield_fixture
def new_db_left(uri_left):
    new_db(uri_left)
    yield
    destroy_database(uri_left)


@pytest.yield_fixture
def new_db_right(uri_right):
    new_db(uri_right)
    yield
    destroy_database(uri_right)


@pytest.mark.usefixtures("new_db_left")
@pytest.mark.usefixtures("new_db_right")
def test_same_schema_is_the_same(uri_left, uri_right):
    prepare_schema_from_models(uri_left, Base_right)
    prepare_schema_from_models(uri_right, Base_right)

    result = compare(uri_left, uri_right)

    assert result.is_match


@pytest.mark.usefixtures("new_db_left")
@pytest.mark.usefixtures("new_db_right")
def test_schemas_are_different(uri_left, uri_right):
    prepare_schema_from_models(uri_left, Base_left)
    prepare_schema_from_models(uri_right, Base_right)

    result = compare(uri_left, uri_right)

    assert not result.is_match


@pytest.mark.usefixtures("new_db_left")
@pytest.mark.usefixtures("new_db_right")
def test_errors_dict_catches_all_differences(uri_left, uri_right):
    prepare_schema_from_models(uri_left, Base_left)
    prepare_schema_from_models(uri_right, Base_right)

    result = compare(uri_left, uri_right)

    expected_errors = {
        'tables': {
            'left_only': ['mobile_numbers'],
            'right_only': ['phone_numbers'],
        },
        'tables_data': {
            'companies': {
                'columns': {
                    'diff': [
                        {
                            'key': 'name',
                            'left': {
                                'default': None,
                                'name': 'name',
                                'nullable': False,
                                'type': 'VARCHAR(200)',
                            },
                            'right': {
                                'default': None,
                                'name': 'name',
                                'nullable': True,
                                'type': 'VARCHAR(200)',
                            }
                        }
                    ]
                },
                'indexes': {
                    'left_only': [
                        {
                            'column_names': ['name'],
                            'name': 'name',
                            'type': 'UNIQUE',
                            'unique': True,
                        }
                    ]
                }
            },
            'employees': {
                'columns': {
                    'diff': [
                        {
                            'key': 'polarity',
                            'left': {
                                'default': None,
                                'name': 'polarity',
                                'nullable': True,
                                'type': "ENUM('NEGATIVE','POSITIVE')"},
                            'right': {
                                'default': None,
                                'name': 'polarity',
                                'nullable': True,
                                'type': "ENUM('NEG','POS')"
                            }
                        },
                        {
                            'key': 'spin',
                            'left': {
                                'default': None,
                                'name': 'spin',
                                'nullable': True,
                                'type': 'VARCHAR(9)'
                            },
                            'right': {
                                'default': None,
                                'name': 'spin',
                                'nullable': True,
                                'type': 'VARCHAR(4)'
                            }
                        }
                    ]
                },
                'foreign_keys': {
                    'left_only': [
                        {
                            'constrained_columns': ['company_id'],
                            'name': 'fk_employees_companies',
                            'options': {},
                            'referred_columns': ['id'],
                            'referred_schema': None,
                            'referred_table': 'companies'
                        }
                    ],
                    'right_only': [
                        {
                            'constrained_columns': ['company_id'],
                            'name': 'fk_emp_comp',
                            'options': {},
                            'referred_columns': ['id'],
                            'referred_schema': None,
                            'referred_table': 'companies',
                        }
                    ]
                },
                'indexes': {
                    'left_only': [
                        {
                            'column_names': ['name'],
                            'name': 'ix_employees_name',
                            'type': 'UNIQUE',
                            'unique': True,
                        },
                        {
                            'column_names': ['company_id'],
                            'name': 'fk_employees_companies',
                            'unique': False,
                        }
                    ],
                    'right_only': [
                        {
                            'column_names': ['company_id'],
                            'name': 'fk_emp_comp',
                            'unique': False,
                        },
                        {
                            'column_names': ['name'],
                            'name': 'name',
                            'type': 'UNIQUE',
                            'unique': True,
                        }
                    ]
                }
            },
            'roles': {
                'columns': {
                    'diff': [
                        {
                            'key': 'name',
                            'left': {
                                'default': None,
                                'name': 'name',
                                'nullable': False,
                                'type': 'VARCHAR(50)',
                            },
                            'right': {
                                'default': None,
                                'name': 'name',
                                'nullable': False,
                                'type': 'VARCHAR(60)',
                            }
                        }
                    ]
                }
            },
            'skills': {
                'columns': {
                    'diff': [
                        {
                            'key': 'slug',
                            'left': {
                                'default': None,
                                'name': 'slug',
                                'nullable': False,
                                'type': 'VARCHAR(50)',
                            },
                            'right': {
                                'default': None,
                                'name': 'slug',
                                'nullable': True,
                                'type': 'VARCHAR(50)',
                            }
                        }
                    ],
                    'right_only': [
                        {
                            'autoincrement': True,
                            'default': None,
                            'name': 'id',
                            'nullable': False,
                            'type': 'INTEGER(11)',
                        }
                    ]
                },
                'primary_keys': {
                    'left_only': ['slug'],
                    'right_only': ['id'],
                }
            }
        },
        'enums': {
        },
        'uris': {
            'left': uri_left,
            'right': uri_right,
        }
    }

    assert not result.is_match

    compare_error_dicts(expected_errors, result.errors)


def compare_error_dicts(err1, err2):
    """Smart comparer of error dicts.

    We cannot directly compare a nested dict structure that has lists
    as values on some level. The order of the same list in the two dicts
    could be different, which would lead to a failure in the comparison,
    but it would be wrong as for us the order doesn't matter and we need
    a comparison that only checks that the same items are in the lists.
    In order to do this, we use the walk_dict function to perform a
    smart comparison only on the lists.

    This function compares the ``tables`` and ``uris`` items, then it does
    an order-insensitive comparison of all lists, and finally it compares
    that the sorted JSON dump of both dicts is the same.
    """
    assert err1['tables'] == err2['tables']
    assert err1['uris'] == err2['uris']

    paths = [
        ['tables_data', 'companies', 'columns', 'diff'],
        ['tables_data', 'companies', 'indexes', 'left_only'],
        ['tables_data', 'employees', 'foreign_keys', 'left_only'],
        ['tables_data', 'employees', 'foreign_keys', 'right_only'],
        ['tables_data', 'employees', 'indexes', 'left_only'],
        ['tables_data', 'employees', 'indexes', 'right_only'],
        ['tables_data', 'roles', 'columns', 'diff'],
        ['tables_data', 'skills', 'columns', 'diff'],
        ['tables_data', 'skills', 'columns', 'right_only'],
        ['tables_data', 'skills', 'primary_keys', 'left_only'],
        ['tables_data', 'skills', 'primary_keys', 'right_only'],
    ]

    for path in paths:
        assert_items_equal(walk_dict(err1, path), walk_dict(err2, path))

    assert sorted(json.dumps(err1)) == sorted(json.dumps(err2))


def walk_dict(d, path):
    """Walks a dict given a path of keys.

    For example, if we have a dict like this::

        d = {
            'a': {
                'B': {
                    1: ['hello', 'world'],
                    2: ['hello', 'again'],
                }
            }
        }

    Then ``walk_dict(d, ['a', 'B', 1])`` would return
    ``['hello', 'world']``.
    """
    if not path:
        return d
    return walk_dict(d[path[0]], path[1:])


@pytest.mark.usefixtures("new_db_left")
@pytest.mark.usefixtures("new_db_right")
def test_ignores(uri_left, uri_right):
    # functionally the same of `test_errors_dict_catches_all_differences`
    # but all errors are silenced with ignores
    prepare_schema_from_models(uri_left, Base_left)
    prepare_schema_from_models(uri_right, Base_right)

    ignores = [
        'mobile_numbers',
        'phone_numbers',
        '*.enum.polarity',
        'companies.col.name',
        'companies.idx.name',
        'employees.col.polarity',
        'employees.col.spin',
        'employees.fk.fk_employees_companies',
        'employees.fk.fk_emp_comp',
        'employees.idx.ix_employees_name',
        'employees.idx.fk_employees_companies',
        'employees.idx.name',
        'employees.idx.fk_emp_comp',
        'roles.col.name',
        'skills.col.slug',
        'skills.col.id',
        'skills.pk.slug',
        'skills.pk.id',
    ]

    result = compare(uri_left, uri_right, ignores)

    assert result.is_match


@pytest.mark.usefixtures("new_db_left")
@pytest.mark.usefixtures("new_db_right")
def test_ignores_alternative_sep(uri_left, uri_right):
    # functionally the same of `test_errors_dict_catches_all_differences`
    # but all errors are silenced with ignores
    prepare_schema_from_models(uri_left, Base_left)
    prepare_schema_from_models(uri_right, Base_right)

    ignores = [
        'mobile_numbers',
        'phone_numbers',
        '*#enum#polarity',
        'companies#col#name',
        'companies#idx#name',
        'employees#col#polarity',
        'employees#col#spin',
        'employees#fk#fk_employees_companies',
        'employees#fk#fk_emp_comp',
        'employees#idx#ix_employees_name',
        'employees#idx#fk_employees_companies',
        'employees#idx#name',
        'employees#idx#fk_emp_comp',
        'roles#col#name',
        'skills#col#slug',
        'skills#col#id',
        'skills#pk#slug',
        'skills#pk#id',
    ]

    result = compare(uri_left, uri_right, ignores=ignores, ignores_sep='#')

    assert result.is_match


@pytest.mark.usefixtures("new_db_left")
@pytest.mark.usefixtures("new_db_right")
@pytest.mark.parametrize('missing_ignore', [
    'mobile_numbers',
    'phone_numbers',
    '*.enum.polarity',
    'companies.col.name',
    'companies.idx.name',
    'employees.fk.fk_employees_companies',
    'employees.fk.fk_emp_comp',
    'employees.idx.ix_employees_name',
    'employees.idx.fk_employees_companies',
    'employees.idx.name',
    'employees.idx.fk_emp_comp',
    'roles.col.name',
    'skills.col.slug',
    'skills.col.id',
    'skills.pk.slug',
    'skills.pk.id',
])
def test_ignores_all_needed(uri_left, uri_right, missing_ignore):
    # proves each ignore clause is needed
    prepare_schema_from_models(uri_left, Base_left)
    prepare_schema_from_models(uri_right, Base_right)

    ignores = [
        'mobile_numbers',
        'phone_numbers',
        '*.enum.polarity',
        'companies.col.name',
        'companies.idx.name',
        'employees.fk.fk_employees_companies',
        'employees.fk.fk_emp_comp',
        'employees.idx.ix_employees_name',
        'employees.idx.fk_employees_companies',
        'employees.idx.name',
        'employees.idx.fk_emp_comp',
        'roles.col.name',
        'skills.col.slug',
        'skills.col.id',
        'skills.pk.slug',
        'skills.pk.id',
    ]

    result = compare(
        uri_left,
        uri_right,
        ignores=list(set(ignores) - set([missing_ignore]))
    )

    assert not result.is_match
