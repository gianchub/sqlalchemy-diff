# -*- coding: utf-8 -*-
import json
import os
import uuid

import pytest

from sqlalchemydiff.util import CompareResult, InspectorFactory, IgnoreManager
from mock import Mock, patch


class TestCompareResult(object):

    def test___init__(self):
        info, errors = Mock(), Mock()

        result = CompareResult(info, errors)

        assert info == result.info
        assert errors == result.errors

    def test_is_match(self):
        info, errors = {}, {}
        result = CompareResult(info, errors)

        assert result.is_match

        result.errors = {1: 1}
        assert not result.is_match

    def test_dump_info(self):
        info = {'some': 'info'}
        filename = '{}.txt'.format(uuid.uuid4())
        result = CompareResult(info, {})

        result.dump_info(filename=filename)

        with open(filename, 'rU') as stream:
            assert info == json.loads(stream.read())

        os.unlink(filename)

    def test_dump_errors(self):
        errors = {'some': 'errors'}
        filename = '{}.txt'.format(uuid.uuid4())
        result = CompareResult({}, errors)

        result.dump_errors(filename=filename)

        with open(filename, 'rU') as stream:
            assert errors == json.loads(stream.read())

        os.unlink(filename)

    def test_dump_with_null_filename(self):
        errors = {'some': 'errors'}
        result = CompareResult({}, errors)

        expected_dump = json.dumps(errors, indent=4, sort_keys=True)
        assert result.dump_errors(filename=None) == expected_dump


class TestInspectorFactory(object):

    @pytest.fixture
    def create_engine_mock(self):
        with patch('sqlalchemydiff.util.create_engine') as m:
            yield m

    @pytest.fixture
    def inspect_mock(self):
        with patch('sqlalchemydiff.util.inspect') as m:
            yield m

    def test_from_uri(self, inspect_mock, create_engine_mock):
        uri = 'some-db-uri/some-db-name'
        inspector = InspectorFactory.from_uri(uri)

        create_engine_mock.assert_called_once_with(uri)
        inspect_mock.assert_called_once_with(create_engine_mock.return_value)

        assert inspect_mock.return_value == inspector


class TestIgnoreManager:

    @pytest.fixture
    def ignore_data(self):
        return [
            'table-A.pk.id',
            'table-A.fk.user_id',
            'table-A.fk.address_id',
            'table-B.pk.root_id',
            'table-C.col.telephone',
            'table-C.idx.admin_id',
            'table-D',
            'table-E',
        ]

    @pytest.mark.parametrize('ignore', [
        None,
        [],
        (),
    ])
    def test_init_empty(self, ignore):
        im = IgnoreManager(ignore)

        assert {} == im.ignore_data
        assert set() == im.ignore_tables

    def test_init(self, ignore_data):
        im = IgnoreManager(ignore_data)

        expected_ignore = {
            'table-A': {
                'pk': ['id'],
                'fk': ['user_id', 'address_id'],
            },
            'table-B': {
                'pk': ['root_id'],
            },
            'table-C': {
                'col': ['telephone'],
                'idx': ['admin_id'],
            },
        }

        expected_tables = set(['table-D', 'table-E'])

        assert expected_ignore == im.ignore_data
        assert expected_tables == im.ignore_tables

    def test_init_alternative_separator(self, ignore_data):
        ignore_data = [clause.replace('.', '#') for clause in ignore_data]
        im = IgnoreManager(ignore_data, separator='#')

        expected_ignore = {
            'table-A': {
                'pk': ['id'],
                'fk': ['user_id', 'address_id'],
            },
            'table-B': {
                'pk': ['root_id'],
            },
            'table-C': {
                'col': ['telephone'],
                'idx': ['admin_id'],
            },
        }

        expected_tables = set(['table-D', 'table-E'])

        assert expected_ignore == im.ignore_data
        assert expected_tables == im.ignore_tables

    def test_ignore_tables_property(self, ignore_data):
        im = IgnoreManager(ignore_data)

        expected_tables = set(['table-D', 'table-E'])

        assert expected_tables == im.ignore_tables

        # make sure the property returns a copy
        im.ignore_tables.add('another-table')
        assert expected_tables == im.ignore_tables

    def test_ignore_data_property(self, ignore_data):
        im = IgnoreManager(ignore_data)

        expected_ignore = {
            'table-A': {
                'pk': ['id'],
                'fk': ['user_id', 'address_id'],
            },
            'table-B': {
                'pk': ['root_id'],
            },
            'table-C': {
                'col': ['telephone'],
                'idx': ['admin_id'],
            },
        }

        assert expected_ignore == im.ignore_data

        # make sure the property returns a copy
        im.ignore_data['another-table'] = {'something': 'else'}
        assert expected_ignore == im.ignore_data

    def test_init_strip(self):
        ignore_data = ['  table-A  .  pk  .  id  ', '   table-C  ']

        im = IgnoreManager(ignore_data)

        expected_ignore = {
            'table-A': {
                'pk': ['id']
            }
        }

        expected_tables = set(['table-C'])

        assert expected_ignore == im.ignore_data
        assert expected_tables == im.ignore_tables

    def test_identifier_incorrect(self):
        ignore_data = ['table-A.unknown.some-name']

        with pytest.raises(ValueError) as err:
            IgnoreManager(ignore_data)

        assert (
            "unknown is invalid. It must be in "
            "['pk', 'fk', 'idx', 'col', 'cons', 'enum']",
        ) == err.value.args

    @pytest.mark.parametrize('clause', [
        'too.few',
        'too.many.definitely.for-sure',
    ])
    def test_incorrect_clause(self, clause):
        ignore_data = [clause]

        with pytest.raises(ValueError) as err:
            IgnoreManager(ignore_data)

        assert (
            '{} is not a well formed clause: table_name.identifier.name'
            .format(clause),
        ) == err.value.args

    @pytest.mark.parametrize('clause', [
        '.pk.b',
        'a.pk.',
    ])
    def test_incorrect_empty_clause(self, clause):
        ignore_data = [clause]

        with pytest.raises(ValueError) as err:
            IgnoreManager(ignore_data)

        assert (
            '{} is not a well formed clause: table_name.identifier.name'
            .format(clause),
        ) == err.value.args

    @pytest.mark.parametrize('clause', [
        3,
        3.14159265,
        [],
        (),
        {},
        None,
    ])
    def test_type_error_clause(self, clause):
        ignore_data = [clause]

        with pytest.raises(TypeError) as err:
            IgnoreManager(ignore_data)

        assert (
            '{} is not a string'.format(clause),
        ) == err.value.args

    def test_get_missing_table(self):
        ignore_data = []

        im = IgnoreManager(ignore_data)

        assert [] == im.get('some-table-name', 'some-identifier')

    def test_get_missing_identifier(self, ignore_data):
        im = IgnoreManager(ignore_data)

        assert [] == im.get('table-C', 'pk')

    def test_get(self, ignore_data):
        im = IgnoreManager(ignore_data)

        assert ['id'] == im.get('table-A', 'pk')
        assert ['user_id', 'address_id'] == im.get('table-A', 'fk')
