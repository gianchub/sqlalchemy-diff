# -*- coding: utf-8 -*-
import pytest

from .util import (
    get_temporary_uri,
    new_db,
    destroy_database,
)


@pytest.fixture(scope="module")
def db_uri():
    return "mysql+mysqlconnector://root:@localhost/sqlalchemydiff"


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