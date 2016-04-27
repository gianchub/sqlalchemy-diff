# -*- coding: utf-8 -*-
from collections import namedtuple
from uuid import uuid4
import json

from sqlalchemy import inspect, create_engine
from sqlalchemy_utils import create_database, drop_database, database_exists


TablesInfo = namedtuple(
    'TablesInfo', ['left', 'right', 'left_only', 'right_only', 'common'])
"""Represent information about the tables in a comparison between two
databases.  It's meant for internal use. """


DiffResult = namedtuple(
    'DiffResult', ['left_only', 'right_only', 'common', 'diff'])
"""Represent information about table properties in a comparison between
tables from two databases.  It's meant for internal use. """


class InspectorFactory(object):

    """Create a :func:`sqlalchemy.inspect` instance for a given URI. """

    @classmethod
    def from_uri(cls, uri):
        engine = create_engine(uri)
        inspector = inspect(engine)
        return inspector


class CompareResult(object):

    """Represent the result of a comparison.

    It tells if the comparison was a match, and it allows the user to
    dump both the `info` and `errors` dicts to a file in JSON format,
    so that they can be inspected.
    """

    def __init__(self, info, errors):
        self.info = info
        self.errors = errors

    @property
    def is_match(self):
        """Tell if comparison was a match. """
        return not self.errors

    def dump_info(self, filename='info_dump.json'):
        """Dump `info` dict to a file. """
        return self._dump(self.info, filename)

    def dump_errors(self, filename='errors_dump.json'):
        """Dump `errors` dict to a file. """
        return self._dump(self.errors, filename)

    def _dump(self, data_to_dump, filename):
        data = self._dump_data(data_to_dump)
        if filename is not None:
            self._write_data_to_file(data, filename)
        return data

    def _dump_data(self, data):
        return json.dumps(data, indent=4, sort_keys=True)

    def _write_data_to_file(self, data, filename):
        with open(filename, 'w') as stream:
            stream.write(data)


def new_db(uri):
    """Drop the database at ``uri`` and create a brand new one. """
    destroy_database(uri)
    create_database(uri)


def destroy_database(uri):
    """Destroy the database at ``uri``, if it exists. """
    if database_exists(uri):
        drop_database(uri)


def get_temporary_uri(uri):
    """Substitutes the database name with a random one.

    For example, given this uri:
    "mysql+mysqlconnector://root:@localhost/database_name"

    a call to ``get_temporary_uri(uri)`` could return something like this:
    "mysql+mysqlconnector://root:@localhost/temp_000da...898fe"

    where the last part of the name is taken from a unique ID in hex
    format.
    """
    base, _ = uri.rsplit('/', 1)
    uri = '{}/temp_{}'.format(base, uuid4().hex)
    return uri


def prepare_schema_from_models(uri, sqlalchemy_base):
    """Creates the database schema from the ``SQLAlchemy`` models. """
    engine = create_engine(uri)
    sqlalchemy_base.metadata.create_all(engine)


class IgnoreManager:

    allowed_identifiers = ['pk', 'fk', 'idx', 'col']

    def __init__(self, ignore_data):
        self.ignore = self.parse(ignore_data)

    def parse(self, ignore_data):
        ignore = {}
        for data in ignore_data:

            self.validate_clause(data)
            table_name, identifier, name = self.fetch_data_items(data)
            self.validate_items(table_name, identifier, name)

            names = (
                ignore.setdefault(table_name, {}).setdefault(identifier, [])
            )
            names.append(name)

        return ignore

    def validate_clause(self, data):
        if len(data.split('.')) != 3:
            raise ValueError(
                '{} is not a well formed clause: table_name.identifier.name'
                .format(data)
            )

    def fetch_data_items(self, data):
        return [item.strip() for item in data.split('.')]

    def validate_items(self, table_name, identifier, name):
        if identifier not in self.allowed_identifiers:
            raise ValueError(
                '{} is invalid. It must be in {}'.format(
                    identifier, self.allowed_identifiers
                )
            )

        if not table_name or not identifier or not name:
            raise ValueError(
                '{} is not a well formed clause: table_name.identifier.name'
                .format('.'.join(
                    (table_name, identifier, name)
                    )
                )
            )

    def get(self, table_name, identifier):
        pass
