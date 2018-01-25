# -*- coding: utf-8 -*-
import pytest

from mock import Mock, patch, call

from sqlalchemydiff.comparer import (
    _compile_errors,
    _diff_dicts,
    _discard_ignores,
    _discard_ignores_by_name,
    _get_columns,
    _get_columns_info,
    _get_common_tables,
    _get_foreign_keys,
    _get_foreign_keys_info,
    _get_indexes,
    _get_indexes_info,
    _get_info_dict,
    _get_inspectors,
    _get_primary_keys,
    _get_primary_keys_info,
    _get_table_data,
    _get_tables,
    _get_tables_data,
    _get_tables_diff,
    _get_tables_info,
    _make_result,
    _process_type,
    _process_types,
    compare,
    CompareResult,
    InspectorFactory,
    TablesInfo,
)
from test import assert_items_equal


@pytest.yield_fixture
def mock_inspector_factory():
    with patch.object(InspectorFactory, 'from_uri') as from_uri:
        from_uri.side_effect = [
            Mock(name="Left Inspector From Factory"),
            Mock(name="Right Inspector From Factory")
        ]
        yield


@pytest.mark.usefixtures("mock_inspector_factory")
class TestCompareCallsChain(object):
    """This test class makes sure the `compare` function inside process
    works as expected.
    """
    @pytest.yield_fixture
    def _get_inspectors_mock(self):
        with patch('sqlalchemydiff.comparer._get_inspectors') as m:
            m.return_value = [
                Mock(name="Left Inspector"),
                Mock(name="Right Inspector"),
            ]
            yield m

    @pytest.yield_fixture
    def _get_tables_data_mock(self):
        with patch('sqlalchemydiff.comparer._get_tables_data') as m:
            yield m

    @pytest.yield_fixture
    def _compile_errors_mock(self):
        with patch('sqlalchemydiff.comparer._compile_errors') as m:

            def info_side_effect(info):
                """Using this side effect is enough to verify that we
                pass the final version of `info` to the `calculate_errors`
                function, and that the function actually does something,
                which in the mocked version is adding the '_err' key/val.
                """
                errors = info.copy()
                errors['_err'] = True
                return errors

            m.side_effect = info_side_effect
            yield m

    @pytest.yield_fixture
    def _get_tables_info_mock(self):
        with patch('sqlalchemydiff.comparer._get_tables_info') as m:
            m.return_value = TablesInfo(
                left=Mock(name="Tables Left"),
                right=Mock(name="Tables Right"),
                left_only=Mock(name="Tables Only Left"),
                right_only=Mock(name="Tables Only Right"),
                common=['common_table_A', 'common_table_B'],
            )
            yield m

    @pytest.yield_fixture
    def _get_enums_data_mock(self):
        with patch('sqlalchemydiff.comparer._get_enums_data') as m:
            m.return_value = []
            yield m

    def test_compare_calls_chain(
            self, _get_tables_info_mock, _get_tables_data_mock,
            _get_enums_data_mock, _compile_errors_mock):
        """By inspecting `info` and `errors` at the end, we automatically
        check that the whole process works as expected.  What this test
        leaves out is the verifications about inspectors.
        """
        _get_tables_data_mock.return_value = {
            'common_table_A': {
                'data': 'some-data-A',
            },
            'common_table_B': {
                'data': 'some-data-B',
            },
        }

        tables_info = _get_tables_info_mock.return_value

        result = compare(
            "left_uri", "right_uri", ignores=['ignore_me'])

        expected_info = {
            'uris': {
                'left': "left_uri",
                'right': "right_uri",
            },
            'tables': {
                'left': tables_info.left,
                'left_only': tables_info.left_only,
                'right': tables_info.right,
                'right_only': tables_info.right_only,
                'common': tables_info.common,
            },
            'tables_data': {
                'common_table_A': {
                    'data': 'some-data-A',
                },
                'common_table_B': {
                    'data': 'some-data-B',
                },
            },
            'enums': {
                'left_only': [],
                'right_only': [],
                'common': [],
                'diff': [],
            },
        }

        expected_errors = expected_info.copy()
        expected_errors['_err'] = True

        assert expected_info == result.info
        assert expected_errors == result.errors

    def test__get_tables_info_called_with_correct_inspectors(
            self, _get_inspectors_mock, _get_tables_info_mock,
            _get_tables_data_mock, _get_enums_data_mock,
            _compile_errors_mock):
        left_inspector, right_inspector = _get_inspectors_mock.return_value

        compare("left_uri", "right_uri", ignores=['ignore_me'])

        _get_inspectors_mock.assert_called_once_with("left_uri", "right_uri")
        _get_tables_info_mock.assert_called_once_with(
            left_inspector, right_inspector, set(['ignore_me']))


@pytest.mark.usefixtures("mock_inspector_factory")
class TestCompareInternals(object):

    # FIXTURES

    @pytest.yield_fixture
    def _get_table_data_mock(self):
        with patch('sqlalchemydiff.comparer._get_table_data') as m:
            yield m

    @pytest.yield_fixture
    def _diff_dicts_mock(self):
        with patch('sqlalchemydiff.comparer._diff_dicts') as m:
            yield m

    @pytest.yield_fixture
    def _get_foreign_keys_mock(self):
        with patch('sqlalchemydiff.comparer._get_foreign_keys') as m:
            yield m

    @pytest.yield_fixture
    def _get_primary_keys_mock(self):
        with patch('sqlalchemydiff.comparer._get_primary_keys') as m:
            yield m

    @pytest.yield_fixture
    def _get_indexes_mock(self):
        with patch('sqlalchemydiff.comparer._get_indexes') as m:
            yield m

    @pytest.yield_fixture
    def _get_columns_mock(self):
        with patch('sqlalchemydiff.comparer._get_columns') as m:
            yield m

    @pytest.yield_fixture
    def _process_types_mock(self):
        with patch('sqlalchemydiff.comparer._process_types') as m:
            yield m

    @pytest.yield_fixture
    def _process_type_mock(self):
        with patch('sqlalchemydiff.comparer._process_type') as m:
            yield m

    @pytest.yield_fixture
    def _get_foreign_keys_info_mock(self):
        with patch('sqlalchemydiff.comparer._get_foreign_keys_info') as m:
            yield m

    @pytest.yield_fixture
    def _get_primary_keys_info_mock(self):
        with patch('sqlalchemydiff.comparer._get_primary_keys_info') as m:
            yield m

    @pytest.yield_fixture
    def _get_indexes_info_mock(self):
        with patch('sqlalchemydiff.comparer._get_indexes_info') as m:
            yield m

    @pytest.yield_fixture
    def _get_columns_info_mock(self):
        with patch('sqlalchemydiff.comparer._get_columns_info') as m:
            yield m

    @pytest.yield_fixture
    def _get_constraints_info_mock(self):
        with patch('sqlalchemydiff.comparer._get_constraints_info') as m:
            yield m

    # TESTS

    def test__get_inspectors(self):
        left_inspector_mock, right_inspector_mock = Mock(), Mock()
        InspectorFactory.from_uri.side_effect = [
            left_inspector_mock, right_inspector_mock]
        left_inspector, right_inspector = _get_inspectors(
            "left_uri", "right_uri")

        assert (
            [call("left_uri"), call("right_uri")] ==
            InspectorFactory.from_uri.call_args_list
        )

        assert left_inspector_mock == left_inspector
        assert right_inspector_mock == right_inspector

    def test__get_tables(self):
        left_inspector, right_inspector = Mock(), Mock()
        left_inspector.get_table_names.return_value = ['B', 'ignore_me', 'A']
        right_inspector.get_table_names.return_value = ['C', 'D', 'ignore_me']

        tables_left, tables_right = _get_tables(
            left_inspector, right_inspector, set(['ignore_me'])
        )

        assert ['A', 'B'] == tables_left
        assert ['C', 'D'] == tables_right

    def test__get_tables_diff(self):
        tables_left = ['B', 'A', 'Z', 'C']
        tables_right = ['D', 'Z', 'C', 'F']

        tables_left_only, tables_right_only = _get_tables_diff(
            tables_left, tables_right)

        assert ['A', 'B'] == tables_left_only
        assert ['D', 'F'] == tables_right_only

    def test__get_common_tables(self):
        tables_left = ['B', 'A', 'Z', 'C']
        tables_right = ['D', 'Z', 'C', 'F']

        tables_common = _get_common_tables(tables_left, tables_right)

        assert ['C', 'Z'] == tables_common

    def test__get_tables_info(self):
        left_inspector, right_inspector = Mock(), Mock()
        left_inspector.get_table_names.return_value = [
            'B', 'ignore_me', 'A', 'C']
        right_inspector.get_table_names.return_value = [
            'D', 'C', 'ignore_me', 'Z']

        tables_info = _get_tables_info(
            left_inspector, right_inspector, set(['ignore_me']))

        assert ['A', 'B', 'C'] == tables_info.left
        assert ['C', 'D', 'Z'] == tables_info.right
        assert ['A', 'B'] == tables_info.left_only
        assert ['D', 'Z'] == tables_info.right_only
        assert ['C'] == tables_info.common

    def test__get_info_dict(self):
        tables_info = TablesInfo(
            left=['A', 'B', 'C'], right=['C', 'D', 'Z'],
            left_only=['A', 'B'], right_only=['D', 'Z'], common=['C'])

        info = _get_info_dict('left_uri', 'right_uri', tables_info)

        expected_info = {
            'uris': {
                'left': 'left_uri',
                'right': 'right_uri',
            },
            'tables': {
                'left': ['A', 'B', 'C'],
                'left_only': ['A', 'B'],
                'right': ['C', 'D', 'Z'],
                'right_only': ['D', 'Z'],
                'common': ['C'],
            },
            'tables_data': {},
            'enums': {},
        }

        assert expected_info == info

    def test__get_tables_data(self, _get_table_data_mock):
        _get_table_data_mock.side_effect = [
            {'table_data': 'data_A'},
            {'table_data': 'data_B'},
        ]
        left_inspector, right_inspector, ignore_manager = (
            Mock(), Mock(), Mock()
        )
        tables_common = ['common_table_A', 'common_table_B']

        tables_data = _get_tables_data(
            tables_common, left_inspector, right_inspector, ignore_manager)

        expected_tables_data = {
            'common_table_A': {'table_data': 'data_A'},
            'common_table_B': {'table_data': 'data_B'},
        }

        assert expected_tables_data == tables_data
        assert [
            call(
                left_inspector, right_inspector, 'common_table_A',
                ignore_manager
            ),
            call(
                left_inspector, right_inspector, 'common_table_B',
                ignore_manager
            ),
        ] == _get_table_data_mock.call_args_list

    def test__make_result(self):
        info = {'info': 'dict'}
        errors = {'errors': 'dict'}

        result = _make_result(info, errors)

        assert isinstance(result, CompareResult)
        assert info == result.info
        assert errors == result.errors

    def test__diff_dicts(self):
        left = {
            'a': 'value-a',
            'b': 'value-b-left',
            'c': 'value-common',
        }

        right = {
            'b': 'value-b-right',
            'c': 'value-common',
            'd': 'value-d',
        }

        expected_result = {
            'left_only': ['value-a'],
            'right_only': ['value-d'],
            'common': ['value-common'],
            'diff': [
                {'key': 'b',
                 'left': 'value-b-left',
                 'right': 'value-b-right'}
            ],
        }

        result = _diff_dicts(left, right)

        assert expected_result == result

    def test__get_foreign_keys_info(
            self, _diff_dicts_mock, _get_foreign_keys_mock):
        _get_foreign_keys_mock.side_effect = [
            [{'name': 'fk_left_1'}, {'name': 'fk_left_2'}],
            [{'name': 'fk_right_1'}]
        ]
        left_inspector, right_inspector = Mock(), Mock()

        result = _get_foreign_keys_info(
            left_inspector, right_inspector, 'table_A', [])

        _diff_dicts_mock.assert_called_once_with(
            {
                'fk_left_1': {'name': 'fk_left_1'},
                'fk_left_2': {'name': 'fk_left_2'}
            },
            {
                'fk_right_1': {'name': 'fk_right_1'}
            }
        )

        assert _diff_dicts_mock.return_value == result

    def test__get_foreign_keys_info_ignores(
            self, _diff_dicts_mock, _get_foreign_keys_mock):
        _get_foreign_keys_mock.side_effect = [
            [{'name': 'fk_left_1'}, {'name': 'fk_left_2'}],
            [{'name': 'fk_right_1'}, {'name': 'fk_right_2'}]
        ]
        left_inspector, right_inspector = Mock(), Mock()
        ignores = ['fk_left_1', 'fk_right_2']

        result = _get_foreign_keys_info(
            left_inspector, right_inspector, 'table_A', ignores)

        _diff_dicts_mock.assert_called_once_with(
            {
                'fk_left_2': {'name': 'fk_left_2'}
            },
            {
                'fk_right_1': {'name': 'fk_right_1'}
            }
        )

        assert _diff_dicts_mock.return_value == result

    def test__get_foreign_keys(self):
        inspector = Mock()

        result = _get_foreign_keys(inspector, 'table_A')

        inspector.get_foreign_keys.assert_called_once_with('table_A')
        assert inspector.get_foreign_keys.return_value == result

    def test__get_primary_keys_info(
            self, _diff_dicts_mock, _get_primary_keys_mock):
        _get_primary_keys_mock.side_effect = [
            {'constrained_columns': ['pk_left_1', 'pk_left_2']},
            {'constrained_columns': ['pk_right_1']}
        ]
        left_inspector, right_inspector = Mock(), Mock()

        result = _get_primary_keys_info(
            left_inspector, right_inspector, 'table_A', [])

        _diff_dicts_mock.assert_called_once_with(
            {'pk_left_1': 'pk_left_1', 'pk_left_2': 'pk_left_2'},
            {'pk_right_1': 'pk_right_1'}
        )

        assert _diff_dicts_mock.return_value == result

    def test__get_primary_keys_info_ignores(
            self, _diff_dicts_mock, _get_primary_keys_mock):
        _get_primary_keys_mock.side_effect = [
            {'constrained_columns': ['pk_left_1', 'pk_left_2']},
            {'constrained_columns': ['pk_right_1', 'pk_right_2']},
        ]
        left_inspector, right_inspector = Mock(), Mock()
        ignores = ['pk_left_1', 'pk_right_2']

        result = _get_primary_keys_info(
            left_inspector, right_inspector, 'table_A', ignores)

        _diff_dicts_mock.assert_called_once_with(
            {'pk_left_2': 'pk_left_2'},
            {'pk_right_1': 'pk_right_1'}
        )

        assert _diff_dicts_mock.return_value == result

    def test__get_primary_keys_info_with_pk_constraint_name(
            self, _diff_dicts_mock, _get_primary_keys_mock):
        _get_primary_keys_mock.side_effect = [
            {'name': 'left', 'constrained_columns': ['pk_left_1']},
            {'name': 'right', 'constrained_columns': ['pk_right_1']}
        ]
        left_inspector, right_inspector = Mock(), Mock()

        result = _get_primary_keys_info(
            left_inspector, right_inspector, 'table_A', [])

        _diff_dicts_mock.assert_called_once_with(
            {
                'left': {'name': 'left',
                         'constrained_columns': ['pk_left_1']}
            },
            {
                'right': {'name': 'right',
                          'constrained_columns': ['pk_right_1']}
            }
        )
        assert _diff_dicts_mock.return_value == result

    def test__get_primary_keys_info_ignores_with_pk_constraint_name(
            self, _diff_dicts_mock, _get_primary_keys_mock):
        _get_primary_keys_mock.side_effect = [
            {'name': 'left_1', 'constrained_columns': ['pk_left_1']},
            {'name': 'right_1', 'constrained_columns': ['pk_right_1']},
        ]
        left_inspector, right_inspector = Mock(), Mock()
        ignores = ['left_1', 'left_2', 'right_2']

        result = _get_primary_keys_info(
            left_inspector, right_inspector, 'table_A', ignores)

        _diff_dicts_mock.assert_called_once_with(
            dict(),
            {
                'right_1': {'name': 'right_1',
                            'constrained_columns': ['pk_right_1']},
            }
        )

        assert _diff_dicts_mock.return_value == result

    def test__get_primary_keys(self):
        inspector = Mock()

        result = _get_primary_keys(inspector, 'table_A')

        inspector.get_pk_constraint.assert_called_once_with('table_A')
        assert inspector.get_pk_constraint.return_value == result

    def test__get_indexes_info(
            self, _diff_dicts_mock, _get_indexes_mock):
        _get_indexes_mock.side_effect = [
            [{'name': 'index_left_1'}, {'name': 'index_left_2'}],
            [{'name': 'index_right_1'}]
        ]
        left_inspector, right_inspector = Mock(), Mock()

        result = _get_indexes_info(
            left_inspector, right_inspector, 'table_A', [])

        _diff_dicts_mock.assert_called_once_with(
            {
                'index_left_1': {'name': 'index_left_1'},
                'index_left_2': {'name': 'index_left_2'}
            },
            {
                'index_right_1': {'name': 'index_right_1'}
            }
        )

        assert _diff_dicts_mock.return_value == result

    def test__get_indexes_info_ignores(
            self, _diff_dicts_mock, _get_indexes_mock):
        _get_indexes_mock.side_effect = [
            [{'name': 'index_left_1'}, {'name': 'index_left_2'}],
            [{'name': 'index_right_1'}, {'name': 'index_right_2'}]
        ]
        left_inspector, right_inspector = Mock(), Mock()
        ignores = ['index_left_1', 'index_right_2']

        result = _get_indexes_info(
            left_inspector, right_inspector, 'table_A', ignores)

        _diff_dicts_mock.assert_called_once_with(
            {
                'index_left_2': {'name': 'index_left_2'}
            },
            {
                'index_right_1': {'name': 'index_right_1'}
            }
        )

        assert _diff_dicts_mock.return_value == result

    def test__get_indexes(self):
        inspector = Mock()

        result = _get_indexes(inspector, 'table_A')

        inspector.get_indexes.assert_called_once_with('table_A')
        assert inspector.get_indexes.return_value == result

    def test__get_columns_info(
            self, _diff_dicts_mock, _get_columns_mock, _process_types_mock):
        _get_columns_mock.side_effect = [
            [{'name': 'columns_left_1'}, {'name': 'columns_left_2'}],
            [{'name': 'columns_right_1'}]
        ]

        def process_types_side_effect(columns):
            columns['_processed'] = True
        _process_types_mock.side_effect = process_types_side_effect

        left_inspector, right_inspector = Mock(), Mock()

        result = _get_columns_info(
            left_inspector, right_inspector, 'table_A', [])

        _diff_dicts_mock.assert_called_once_with(
            {
                '_processed': True,
                'columns_left_1': {'name': 'columns_left_1'},
                'columns_left_2': {'name': 'columns_left_2'}
            },
            {
                '_processed': True,
                'columns_right_1': {'name': 'columns_right_1'}
            }
        )

        assert _diff_dicts_mock.return_value == result

    def test__get_columns_info_ignores(
            self, _diff_dicts_mock, _get_columns_mock, _process_types_mock):
        _get_columns_mock.side_effect = [
            [{'name': 'columns_left_1'}, {'name': 'columns_left_2'}],
            [{'name': 'columns_right_1'}, {'name': 'columns_right_2'}]
        ]

        def process_types_side_effect(columns):
            columns['_processed'] = True
        _process_types_mock.side_effect = process_types_side_effect

        left_inspector, right_inspector = Mock(), Mock()
        ignores = ['columns_left_1', 'columns_right_2']

        result = _get_columns_info(
            left_inspector, right_inspector, 'table_A', ignores)

        _diff_dicts_mock.assert_called_once_with(
            {
                '_processed': True,
                'columns_left_2': {'name': 'columns_left_2'}
            },
            {
                '_processed': True,
                'columns_right_1': {'name': 'columns_right_1'}
            }
        )

        assert _diff_dicts_mock.return_value == result

    def test__get_columns(self):
        inspector = Mock()

        result = _get_columns(inspector, 'table_A')

        inspector.get_columns.assert_called_once_with('table_A')
        assert inspector.get_columns.return_value == result

    def test__process_types(self, _process_type_mock):
        column_dict = {
            'columns_left_1': {'name': 'columns_left_1', 'type': 'type1'},
            'columns_left_2': {'name': 'columns_left_2', 'type': 'type2'}
        }

        _process_types(column_dict)

        assert_items_equal(
            [call('type1'), call('type2')],
            _process_type_mock.call_args_list)

    def test_process_type(self):
        type_ = Mock()
        result = _process_type(type_)

        type_.compile.assert_called_once_with()
        assert type_.compile.return_value == result

    def test__get_table_data(
            self, _get_foreign_keys_info_mock, _get_primary_keys_info_mock,
            _get_indexes_info_mock, _get_columns_info_mock,
            _get_constraints_info_mock):
        left_inspector, right_inspector = Mock(), Mock()

        _get_foreign_keys_info_mock.return_value = {
            'left_only': 1, 'right_only': 2, 'common': 3, 'diff': 4
        }
        _get_primary_keys_info_mock.return_value = {
            'left_only': 5, 'right_only': 6, 'common': 7, 'diff': 8
        }
        _get_indexes_info_mock.return_value = {
            'left_only': 9, 'right_only': 10, 'common': 11, 'diff': 12
        }
        _get_columns_info_mock.return_value = {
            'left_only': 13, 'right_only': 14, 'common': 15, 'diff': 16
        }
        _get_constraints_info_mock.return_value = {
            'left_only': 17, 'right_only': 18, 'common': 19, 'diff': 20
        }

        result = _get_table_data(
            left_inspector, right_inspector, 'table_A', Mock()
        )

        expected_result = {
            'foreign_keys': {
                'left_only': 1,
                'right_only': 2,
                'common': 3,
                'diff': 4,
            },
            'primary_keys': {
                'left_only': 5,
                'right_only': 6,
                'common': 7,
                'diff': 8,
            },
            'indexes': {
                'left_only': 9,
                'right_only': 10,
                'common': 11,
                'diff': 12,
            },
            'columns': {
                'left_only': 13,
                'right_only': 14,
                'common': 15,
                'diff': 16,
            },
            'constraints': {
                'left_only': 17,
                'right_only': 18,
                'common': 19,
                'diff': 20,
            },
        }

        assert expected_result == result

    def test__compile_errors_with_errors(self):
        info = {
            'uris': {
                'left': 'left_uri',
                'right': 'right_uri',
            },
            'tables': {
                'left': 'tables_left',
                'left_only': 'tables_left_only',
                'right': 'tables_right',
                'right_only': 'tables_right_only',
                'common': 'tables_common',
            },
            'tables_data': {

                'table_name_1': {
                    'foreign_keys': {
                        'left_only': 1,
                        'right_only': 2,
                        'common': 3,
                        'diff': 4,
                    },
                    'primary_keys': {
                        'left_only': 5,
                        'right_only': 6,
                        'common': 7,
                        'diff': 8,
                    },
                    'indexes': {
                        'left_only': 9,
                        'right_only': 10,
                        'common': 11,
                        'diff': 12,
                    },
                    'columns': {
                        'left_only': 13,
                        'right_only': 14,
                        'common': 15,
                        'diff': 16,
                    },
                    'constraints': {
                        'left_only': 17,
                        'right_only': 18,
                        'common': 19,
                        'diff': 20,
                    }
                },

                'table_name_2': {
                    'foreign_keys': {
                        'left_only': 1,
                        'right_only': 2,
                        'common': 3,
                        'diff': 4,
                    },
                    'primary_keys': {
                        'left_only': 5,
                        'right_only': 6,
                        'common': 7,
                        'diff': 8,
                    },
                    'indexes': {
                        'left_only': 9,
                        'right_only': 10,
                        'common': 11,
                        'diff': 12,
                    },
                    'columns': {
                        'left_only': 13,
                        'right_only': 14,
                        'common': 15,
                        'diff': 16,
                    },
                    'constraints': {
                        'left_only': 17,
                        'right_only': 18,
                        'common': 19,
                        'diff': 20,
                    }
                }
            },
            'enums': {
                'left_only': 21,
                'right_only': 22,
                'common': 23,
                'diff': 24,
            }
        }

        expected_errors = {
            'uris': {
                'left': 'left_uri',
                'right': 'right_uri',
            },
            'tables': {
                'left_only': 'tables_left_only',
                'right_only': 'tables_right_only',
            },
            'tables_data': {
                'table_name_1': {
                    'foreign_keys': {
                        'left_only': 1,
                        'right_only': 2,
                        'diff': 4,
                    },
                    'primary_keys': {
                        'left_only': 5,
                        'right_only': 6,
                        'diff': 8,
                    },
                    'indexes': {
                        'left_only': 9,
                        'right_only': 10,
                        'diff': 12,
                    },
                    'columns': {
                        'left_only': 13,
                        'right_only': 14,
                        'diff': 16,
                    },
                    'constraints': {
                        'left_only': 17,
                        'right_only': 18,
                        'diff': 20,
                    }
                },

                'table_name_2': {
                    'foreign_keys': {
                        'left_only': 1,
                        'right_only': 2,
                        'diff': 4,
                    },
                    'primary_keys': {
                        'left_only': 5,
                        'right_only': 6,
                        'diff': 8,
                    },
                    'indexes': {
                        'left_only': 9,
                        'right_only': 10,
                        'diff': 12,
                    },
                    'columns': {
                        'left_only': 13,
                        'right_only': 14,
                        'diff': 16,
                    },
                    'constraints': {
                        'left_only': 17,
                        'right_only': 18,
                        'diff': 20,
                    }
                }
            },
            'enums': {
                'left_only': 21,
                'right_only': 22,
                'diff': 24,
            }
        }

        errors = _compile_errors(info)

        assert expected_errors == errors

    def test__compile_errors_without_errors(self):
        info = {
            'uris': {
                'left': 'left_uri',
                'right': 'right_uri',
            },
            'tables': {
                'left': 'tables_left',
                'left_only': [],
                'right': 'tables_right',
                'right_only': [],
                'common': 'tables_common',
            },
            'tables_data': {
                'table_name_1': {
                    'foreign_keys': {
                        'left_only': [],
                        'right_only': [],
                        'common': 1,
                        'diff': [],
                    },
                    'primary_keys': {
                        'left_only': [],
                        'right_only': [],
                        'common': 2,
                        'diff': [],
                    },
                    'indexes': {
                        'left_only': [],
                        'right_only': [],
                        'common': 3,
                        'diff': [],
                    },
                    'columns': {
                        'left_only': [],
                        'right_only': [],
                        'common': 4,
                        'diff': [],
                    },
                    'constraints': {
                        'left_only': [],
                        'right_only': [],
                        'common': 5,
                        'diff': [],
                    },
                }
            },
            'enums': {
                'left_only': [],
                'right_only': [],
                'common': 6,
                'diff': [],
            }
        }

        expected_errors = {}
        errors = _compile_errors(info)

        assert expected_errors == errors

    @pytest.mark.parametrize('ignores,expected', [
        ([], [{'name': 'A'}, {'name': 'B'}, {'name': 'C'}]),
        (['A', 'C'], [{'name': 'B'}]),
    ])
    def test__discard_ignores_by_name(self, ignores, expected):
        items = [{'name': 'A'}, {'name': 'B'}, {'name': 'C'}]

        assert expected == _discard_ignores_by_name(items, ignores)

    @pytest.mark.parametrize('ignores,expected', [
        ([], ['A', 'B', 'C']),
        (['A', 'C'], ['B']),
    ])
    def test__discard_ignores(self, ignores, expected):
        items = ['A', 'B', 'C']

        assert expected == _discard_ignores(items, ignores)
