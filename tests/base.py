import os

import pytest

from tests.util import create_db, drop_db, get_engine, prepare_schema_from_models

from .models.models_one import Base as BaseOne
from .models.models_two import Base as BaseTwo


class BaseTest:
    @pytest.fixture
    def db_name_one(self):
        return f"one_{os.environ.get('PYTEST_XDIST_WORKER', '1')}"

    @pytest.fixture
    def db_uri_one(self, make_postgres_uri, db_name_one):
        return make_postgres_uri(db_name_one)

    @pytest.fixture
    def db_name_two(self):
        return f"two_{os.environ.get('PYTEST_XDIST_WORKER', '1')}"

    @pytest.fixture
    def db_uri_two(self, make_postgres_uri, db_name_two):
        return make_postgres_uri(db_name_two)

    @pytest.fixture
    def db_engine_one(self, db_uri_one):
        return get_engine(db_uri_one)

    @pytest.fixture
    def db_engine_two(self, db_uri_two):
        return get_engine(db_uri_two)

    @pytest.fixture
    def setup_db_one(self, db_uri_one, db_engine_one):
        create_db(db_uri_one)
        prepare_schema_from_models(db_engine_one, BaseOne)
        yield
        drop_db(db_uri_one)

    @pytest.fixture
    def setup_db_two(self, db_uri_two, db_engine_two):
        create_db(db_uri_two)
        prepare_schema_from_models(db_engine_two, BaseTwo)
        yield
        drop_db(db_uri_two)
