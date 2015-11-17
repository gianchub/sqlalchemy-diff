# -*- coding: utf-8 -*-
import json
import unittest

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
from test.endtoend.test_example import compare_error_dicts


class TestSchemasAreDifferent(unittest.TestCase):

    def setUp(self):
        uri = "mysql+mysqlconnector://root:@localhost/sqlalchemydiff"
        self.uri_left = get_temporary_uri(uri)
        self.uri_right = get_temporary_uri(uri)

        new_db(self.uri_left)
        new_db(self.uri_right)

    def tearDown(self):
        destroy_database(self.uri_left)
        destroy_database(self.uri_right)

    def test_same_schema_is_the_same(self):
        prepare_schema_from_models(self.uri_left, Base_right)
        prepare_schema_from_models(self.uri_right, Base_right)

        result = compare(self.uri_left, self.uri_right)

        assert result.is_match

    def test_schemas_are_different(self):
        prepare_schema_from_models(self.uri_left, Base_left)
        prepare_schema_from_models(self.uri_right, Base_right)

        result = compare(self.uri_left, self.uri_right)

        assert not result.is_match

    def test_errors_dict_catches_all_differences(self):
        prepare_schema_from_models(self.uri_left, Base_left)
        prepare_schema_from_models(self.uri_right, Base_right)

        result = compare(self.uri_left, self.uri_right)

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
            'uris': {
                'left': self.uri_left,
                'right': self.uri_right,
            }
        }

        assert not result.is_match

        compare_error_dicts(expected_errors, result.errors)
