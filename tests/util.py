from collections.abc import Mapping

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy_utils import create_database, database_exists, drop_database

from tests import assert_items_equal


def create_db(uri):
    """Drop the database at `uri`, if it exists, and create a brand new one."""
    drop_db(uri)
    create_database(uri)


def drop_db(uri):
    """Drop the database at `uri`, if it exists."""
    if database_exists(uri):
        drop_database(uri)


def get_engine(uri: str) -> Engine:
    return create_engine(uri)


def prepare_schema_from_models(engine: Engine, sqlalchemy_base: DeclarativeMeta):
    """Creates the database schema from the `SQLAlchemy` models."""
    sqlalchemy_base.metadata.create_all(engine)


def assert_dicts_equal(dict1, dict2):
    """
    Recursively compare two dictionaries.
    For list/tuple values, check they contain the same elements regardless of order.
    """
    # Check if both are dictionaries
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        assert dict1 == dict2

    # Check if they have the same keys
    if set(dict1.keys()) != set(dict2.keys()):
        raise AssertionError(f"{dict1.keys()} != {dict2.keys()}")

    # Compare values for each key
    for key in dict1:
        val1, val2 = dict1[key], dict2[key]

        # If values are lists or tuples, compare elements regardless of order
        if isinstance(val1, (list, tuple)) and isinstance(val2, (list, tuple)):
            assert_items_equal(val1, val2)
        # If values are dictionaries, recursively compare them
        elif isinstance(val1, Mapping) and isinstance(val2, Mapping):
            assert_dicts_equal(val1, val2)
        # Otherwise, directly compare values
        elif val1 != val2:
            raise AssertionError(f"{val1} != {val2}")
