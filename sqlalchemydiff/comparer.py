# -*- coding: utf-8 -*-
from copy import deepcopy

from .util import (
    TablesInfo, DiffResult, InspectorFactory, CompareResult, IgnoreManager
)


def compare(left_uri, right_uri, ignores=None, ignores_sep=None):
    """Compare two databases, given two URIs.

    Compare two databases, ignoring whatever is specified in `ignores`.

    The ``info`` dict has this structure::

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
                'common': ['table_name_1', 'table_name_2'],
            },
            'tables_data': {

                'table_name_1': {
                    'foreign_keys': {
                        'left_only': [...],
                        'right_only': [...],
                        'common': [...],
                        'diff': [...],
                    },
                    'primary_keys': {
                        'left_only': [...],
                        'right_only': [...],
                        'common': [...],
                        'diff': [...],
                    },
                    'indexes': {
                        'left_only': [...],
                        'right_only': [...],
                        'common': [...],
                        'diff': [...],
                    },
                    'columns': {
                        'left_only': [...],
                        'right_only': [...],
                        'common': [...],
                        'diff': [...],
                    }
                },

                'table_name_2': { ... },
            }
        }

    The ``errors`` dict will follow the same structure of the ``info``
    dict, but it will only have the data that is showing a discrepancy
    between the two databases.

    :param string left_uri: The URI for the first (left) database.
    :param string right_uri: The URI for the second (right) database.
    :param iterable ignores:
        A list of strings in the format:
          * `table-name`
          * `table-name.identifier.name`

        If a table name is specified, the whole table is excluded from
        comparison.  If a complete clause is specified, then only the
        specified element is excluded from comparison.  `identifier` is one
        of (`col`, `pk`, `fk`, `idx`) and name is the name of the element
        to be excluded from the comparison.
    :param string ignores_sep:
        Separator to be used to spilt the `ignores` clauses.
    :return:
        A :class:`~.util.CompareResult` object with ``info`` and
        ``errors`` dicts populated with the comparison result.
    """
    ignore_manager = IgnoreManager(ignores, separator=ignores_sep)

    left_inspector, right_inspector = _get_inspectors(left_uri, right_uri)

    tables_info = _get_tables_info(
        left_inspector, right_inspector, ignore_manager.ignore_tables)

    info = _get_info_dict(left_uri, right_uri, tables_info)

    info['tables_data'] = _get_tables_data(
        tables_info.common, left_inspector, right_inspector, ignore_manager
    )

    info['enums'] = _get_enums_info(
        left_inspector,
        right_inspector,
        ignore_manager.get('*', 'enum'),
    )

    errors = _compile_errors(info)
    result = _make_result(info, errors)

    return result


def _get_inspectors(left_uri, right_uri):
    left_inspector = InspectorFactory.from_uri(left_uri)
    right_inspector = InspectorFactory.from_uri(right_uri)
    return left_inspector, right_inspector


def _get_tables_info(left_inspector, right_inspector, ignore_tables):
    """Get information about the differences at the table level. """
    tables_left, tables_right = _get_tables(
        left_inspector, right_inspector, ignore_tables)

    tables_left_only, tables_right_only = _get_tables_diff(
        tables_left, tables_right)

    tables_common = _get_common_tables(tables_left, tables_right)

    return TablesInfo(
        left=tables_left, right=tables_right, left_only=tables_left_only,
        right_only=tables_right_only, common=tables_common)


def _get_tables(left_inspector, right_inspector, ignore_tables):
    """Get table names for both databases. ``ignore_tables`` are removed. """
    tables_left = _get_tables_names(left_inspector, ignore_tables)
    tables_right = _get_tables_names(right_inspector, ignore_tables)
    return tables_left, tables_right


def _get_tables_names(inspector, ignore_tables):
    return sorted(set(inspector.get_table_names()) - ignore_tables)


def _get_tables_diff(tables_left, tables_right):
    return (
        _diff_table_lists(tables_left, tables_right),
        _diff_table_lists(tables_right, tables_left)
    )


def _diff_table_lists(tables_left, tables_right):
    return sorted(set(tables_left) - set(tables_right))


def _get_common_tables(tables_left, tables_right):
    return sorted(set(tables_left) & set(tables_right))


def _get_info_dict(left_uri, right_uri, tables_info):
    """Create an empty stub for the `info` dict. """
    info = {
        'uris': {
            'left': left_uri,
            'right': right_uri,
        },
        'tables': {
            'left': tables_info.left,
            'left_only': tables_info.left_only,
            'right': tables_info.right,
            'right_only': tables_info.right_only,
            'common': tables_info.common,
        },
        'tables_data': {},
        'enums': {},
    }

    return info


def _get_tables_data(
    tables_common, left_inspector, right_inspector, ignore_manager
):
    tables_data = {}

    for table_name in tables_common:
        table_data = _get_table_data(
            left_inspector, right_inspector, table_name, ignore_manager
        )
        tables_data[table_name] = table_data

    return tables_data


def _get_table_data(
    left_inspector, right_inspector, table_name, ignore_manager
):
    table_data = {}

    # foreign keys
    table_data['foreign_keys'] = _get_foreign_keys_info(
        left_inspector,
        right_inspector,
        table_name,
        ignore_manager.get(table_name, 'fk')
    )

    table_data['primary_keys'] = _get_primary_keys_info(
        left_inspector,
        right_inspector,
        table_name,
        ignore_manager.get(table_name, 'pk')
    )

    table_data['indexes'] = _get_indexes_info(
        left_inspector,
        right_inspector,
        table_name,
        ignore_manager.get(table_name, 'idx')
    )

    table_data['columns'] = _get_columns_info(
        left_inspector,
        right_inspector,
        table_name,
        ignore_manager.get(table_name, 'col')
    )

    table_data['constraints'] = _get_constraints_info(
        left_inspector,
        right_inspector,
        table_name,
        ignore_manager.get(table_name, 'cons')
    )

    return table_data


def _diff_dicts(left, right):
    """Makes the diff of two dictionaries, based on keys and values.

    :return:
        A 4-tuple with elements::

            * A list of elements only in left
            * A list of elements only in right
            * A list of common elements
            * A list of diff elements
              {'key':..., 'left':..., 'right':...}
    """
    left_only_key = set(left) - set(right)
    right_only_key = set(right) - set(left)

    left_only = [left[key] for key in left_only_key]
    right_only = [right[key] for key in right_only_key]

    # common and diff
    common_keys = set(left) & set(right)
    common = []
    diff = []

    for key in common_keys:
        if left[key] == right[key]:
            common.append(left[key])
        else:
            diff.append({
                'key': key,
                'left': left[key],
                'right': right[key],
            })

    return DiffResult(
        left_only=left_only, right_only=right_only, common=common, diff=diff
    )._asdict()


def _get_foreign_keys_info(
    left_inspector, right_inspector, table_name, ignores
):
    left_fk_list = _get_foreign_keys(left_inspector, table_name)
    right_fk_list = _get_foreign_keys(right_inspector, table_name)

    left_fk_list = _discard_ignores_by_name(left_fk_list, ignores)
    right_fk_list = _discard_ignores_by_name(right_fk_list, ignores)

    # process into dict
    left_fk = dict((elem['name'], elem) for elem in left_fk_list)
    right_fk = dict((elem['name'], elem) for elem in right_fk_list)

    return _diff_dicts(left_fk, right_fk)


def _get_foreign_keys(inspector, table_name):
    return inspector.get_foreign_keys(table_name)


def _get_primary_keys_info(
    left_inspector, right_inspector, table_name, ignores
):
    left_pk_constraint = _get_primary_keys(left_inspector, table_name)
    right_pk_constraint = _get_primary_keys(right_inspector, table_name)

    pk_constraint_has_name = ('name' in left_pk_constraint and
                              left_pk_constraint['name'] is not None)

    if pk_constraint_has_name:
        left_pk = ({left_pk_constraint['name']: left_pk_constraint}
                   if _discard_ignores_by_name([left_pk_constraint], ignores)
                   else {})
        right_pk = ({right_pk_constraint['name']: right_pk_constraint}
                    if _discard_ignores_by_name([right_pk_constraint], ignores)
                    else {})
    else:
        left_pk_list = left_pk_constraint['constrained_columns']
        right_pk_list = right_pk_constraint['constrained_columns']

        left_pk_list = _discard_ignores(left_pk_list, ignores)
        right_pk_list = _discard_ignores(right_pk_list, ignores)

        # process into dict
        left_pk = dict((elem, elem) for elem in left_pk_list)
        right_pk = dict((elem, elem) for elem in right_pk_list)

    return _diff_dicts(left_pk, right_pk)


def _get_primary_keys(inspector, table_name):
    return inspector.get_pk_constraint(table_name)


def _get_indexes_info(left_inspector, right_inspector, table_name, ignores):
    left_index_list = _get_indexes(left_inspector, table_name)
    right_index_list = _get_indexes(right_inspector, table_name)

    left_index_list = _discard_ignores_by_name(left_index_list, ignores)
    right_index_list = _discard_ignores_by_name(right_index_list, ignores)

    # process into dict
    left_index = dict((elem['name'], elem) for elem in left_index_list)
    right_index = dict((elem['name'], elem) for elem in right_index_list)

    return _diff_dicts(left_index, right_index)


def _get_indexes(inspector, table_name):
    return inspector.get_indexes(table_name)


def _get_columns_info(left_inspector, right_inspector, table_name, ignores):
    left_columns_list = _get_columns(left_inspector, table_name)
    right_columns_list = _get_columns(right_inspector, table_name)

    left_columns_list = _discard_ignores_by_name(left_columns_list, ignores)
    right_columns_list = _discard_ignores_by_name(right_columns_list, ignores)

    # process into dict
    left_columns = dict((elem['name'], elem) for elem in left_columns_list)
    right_columns = dict((elem['name'], elem) for elem in right_columns_list)

    # process `type` fields
    _process_types(left_columns)
    _process_types(right_columns)

    return _diff_dicts(left_columns, right_columns)


def _get_columns(inspector, table_name):
    return inspector.get_columns(table_name)


def _get_constraints_info(left_inspector, right_inspector,
                          table_name, ignores):
    left_constraints_list = _get_constraints_data(left_inspector, table_name)
    right_constraints_list = _get_constraints_data(right_inspector, table_name)

    left_constraints_list = _discard_ignores_by_name(left_constraints_list,
                                                     ignores)
    right_constraints_list = _discard_ignores_by_name(right_constraints_list,
                                                      ignores)

    # process into dict
    left_constraints = dict((elem['name'], elem)
                            for elem in left_constraints_list)
    right_constraints = dict((elem['name'], elem)
                             for elem in right_constraints_list)

    return _diff_dicts(left_constraints, right_constraints)


def _get_constraints_data(inspector, table_name):
    try:
        return inspector.get_check_constraints(table_name)
    except (AttributeError, NotImplementedError):  # pragma: no cover
        # sqlalchemy < 1.1.0
        # or a dialect that doesn't implement get_check_constraints
        return []


def _get_enums_info(left_inspector, right_inspector, ignores):
    left_enums_list = _get_enums_data(left_inspector)
    right_enums_list = _get_enums_data(right_inspector)

    left_enums_list = _discard_ignores_by_name(left_enums_list, ignores)
    right_enums_list = _discard_ignores_by_name(right_enums_list, ignores)

    # process into dict
    left_enums = dict((elem['name'], elem) for elem in left_enums_list)
    right_enums = dict((elem['name'], elem) for elem in right_enums_list)

    return _diff_dicts(left_enums, right_enums)


def _get_enums_data(inspector):
    try:
        # as of 1.2.0, PostgreSQL dialect only; see PGInspector
        return inspector.get_enums()
    except AttributeError:
        return []


def _discard_ignores_by_name(items, ignores):
    return [item for item in items if item['name'] not in ignores]


def _discard_ignores(items, ignores):
    return [item for item in items if item not in ignores]


def _process_types(column_dict):
    for column in column_dict:
        column_dict[column]['type'] = _process_type(
            column_dict[column]['type'])


def _process_type(type_):
    """Process the SQLAlchemy Column Type ``type_``.

    Calls :meth:`sqlalchemy.sql.type_api.TypeEngine.compile` on
    ``type_`` to produce a string-compiled form of it.  "string-compiled"
    meaning as it would be used for a SQL clause.
    """
    return type_.compile()


def _compile_errors(info):
    """Create ``errors`` dict from ``info`` dict. """
    errors_template = {
        'tables': {},
        'tables_data': {},
        'enums': {},
    }
    errors = deepcopy(errors_template)

    # first check if tables aren't a match
    if info['tables']['left_only']:
        errors['tables']['left_only'] = info['tables']['left_only']

    if info['tables']['right_only']:
        errors['tables']['right_only'] = info['tables']['right_only']

    # then check if there is a discrepancy in the data for each table
    keys = ['foreign_keys', 'primary_keys', 'indexes', 'columns',
            'constraints']
    subkeys = ['left_only', 'right_only', 'diff']

    for table_name in info['tables_data']:
        for key in keys:
            for subkey in subkeys:
                if info['tables_data'][table_name][key][subkey]:
                    table_d = errors['tables_data'].setdefault(table_name, {})
                    table_d.setdefault(key, {})[subkey] = info[
                        'tables_data'][table_name][key][subkey]

    for subkey in subkeys:
        if info['enums'][subkey]:
            errors['enums'][subkey] = info['enums'][subkey]

    if errors != errors_template:
        errors['uris'] = info['uris']
        return errors
    return {}


def _make_result(info, errors):
    """Create a :class:`~.util.CompareResult` object. """
    return CompareResult(info, errors)
