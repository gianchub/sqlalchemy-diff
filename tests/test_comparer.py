import json
import logging
from unittest.mock import patch

import pytest

from sqlalchemydiff.comparer import Comparer, CompareResult
from sqlalchemydiff.inspection import register
from sqlalchemydiff.inspection.base import BaseInspector
from sqlalchemydiff.inspection.exceptions import InspectorNotSupported, UnknownInspector
from tests.base import BaseTest
from tests.util import get_engine, prepare_schema_from_models

from .models.models_one import Base as BaseOne
from .models.models_two import Base as BaseTwo


class TestCompareResult(BaseTest):
    def test_compare_result(self):
        result = {
            "tables": {
                "one_only": [],
                "two_only": [],
                "common": [{"name": "common"}],
                "diff": [],
            },
            "enums": {
                "one_only": [],
                "two_only": [],
                "common": [{"name": "common"}],
                "diff": [],
            },
        }

        compare_result = CompareResult(result)
        assert compare_result.result == result
        assert compare_result.errors == {}
        assert compare_result.is_match

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def test_compare_not_match(self, db_engine_one, db_engine_two):
        comparer = Comparer(db_engine_one, db_engine_two)
        result = comparer.compare()
        assert not result.is_match

    @pytest.mark.usefixtures("setup_db_one")
    def test_compare_is_match(self, db_engine_one):
        comparer = Comparer(db_engine_one, db_engine_one)
        result = comparer.compare()
        assert result.is_match


class TestComparer(BaseTest):
    @pytest.fixture
    def tables_only_register(self):
        register_copy = register.copy()
        register.clear()
        register["tables"] = register_copy["tables"]
        yield
        register.update(register_copy)

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def test_compare(self, db_engine_one, db_engine_two, compare_result, compare_errors):
        comparer = Comparer(db_engine_one, db_engine_two)
        result = comparer.compare()
        assert result.result == compare_result
        assert result.errors == compare_errors

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def test_compare_with_ignore_inspectors(
        self, db_engine_one, db_engine_two, compare_result, compare_errors
    ):
        comparer = Comparer(db_engine_one, db_engine_two)
        result = comparer.compare(ignore_inspectors=["tables", "enums"])

        expected_result = compare_result.copy()
        expected_result.pop("tables")
        expected_result.pop("enums")

        expected_errors = compare_errors.copy()
        expected_errors.pop("tables")
        expected_errors.pop("enums")

        assert result.result == expected_result
        assert result.errors == expected_errors

    @pytest.mark.parametrize("ignore_inspectors", [["unknown"], {"unknown"}])
    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def test_compare_with_unknown_ignore_inspectors(
        self, db_engine_one, db_engine_two, ignore_inspectors
    ):
        comparer = Comparer(db_engine_one, db_engine_two)

        with pytest.raises(UnknownInspector, match="Unknown inspector: unknown"):
            comparer.compare(ignore_inspectors=ignore_inspectors)

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def test_compare_with_unknown_ignore_inspectors_multiple(self, db_engine_one, db_engine_two):
        comparer = Comparer(db_engine_one, db_engine_two)

        with pytest.raises(UnknownInspector, match="Unknown inspector: unknown, unknown2"):
            comparer.compare(ignore_inspectors=["unknown", "unknown2"])

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def test_compare_with_unknown_ignore_inspectors_multiple_and_known(
        self, db_engine_one, db_engine_two
    ):
        comparer = Comparer(db_engine_one, db_engine_two)

        with pytest.raises(UnknownInspector, match="Unknown inspector: unknown, unknown2"):
            comparer.compare(ignore_inspectors=["unknown", "unknown2", "tables"])

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two", "tables_only_register")
    def test_compare_with_aliases(
        self,
        db_engine_one,
        db_engine_two,
        compare_result_aliases,
        compare_errors_aliases,
    ):
        comparer = Comparer(db_engine_one, db_engine_two)
        result = comparer.compare(one_alias="production", two_alias="staging")
        assert result.result == compare_result_aliases
        assert result.errors == compare_errors_aliases

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def test_compare_transaction(
        self, db_engine_one, db_engine_two, compare_result, compare_errors
    ):
        with (
            patch.object(db_engine_one, "begin") as mock_begin_one,
            patch.object(db_engine_two, "begin") as mock_begin_two,
        ):
            comparer = Comparer(db_engine_one, db_engine_two)
            result = comparer.compare()
            assert result.result == compare_result
            assert result.errors == compare_errors
            mock_begin_one.assert_called_once_with()
            mock_begin_two.assert_called_once_with()

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def test_dump_result(
        self, db_engine_one, db_engine_two, compare_result, compare_errors, tmp_path
    ):
        comparer = Comparer.from_params(db_engine_one.url, db_engine_two.url)

        info_file = tmp_path / "result.json"
        error_file = tmp_path / "errors.json"

        result = comparer.compare()
        result.dump_result(info_file)
        result.dump_errors(error_file)

        with open(info_file) as f:
            assert json.load(f) == compare_result

        with open(error_file) as f:
            assert json.load(f) == compare_errors


@pytest.mark.is_sqlalchemy_1_4
class TestComparerV14(BaseTest):
    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def test_compare(self, db_engine_one, db_engine_two, compare_result_v14, compare_errors_v14):
        comparer = Comparer(db_engine_one, db_engine_two)
        result = comparer.compare()
        assert result.result == compare_result_v14
        assert result.errors == compare_errors_v14


class TestComparerSqlite(BaseTest):
    @pytest.fixture
    def sqlite_db_engine_one(self):
        return get_engine("sqlite:///:memory:")

    @pytest.fixture
    def sqlite_db_engine_two(self):
        return get_engine("sqlite:///:memory:")

    @pytest.fixture()
    def setup_db_one(self, sqlite_db_engine_one):
        prepare_schema_from_models(sqlite_db_engine_one, BaseOne)
        yield

    @pytest.fixture
    def setup_db_two(self, sqlite_db_engine_two):
        prepare_schema_from_models(sqlite_db_engine_two, BaseTwo)
        yield

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def test_compare(
        self,
        sqlite_db_engine_one,
        sqlite_db_engine_two,
        compare_result_sqlite,
        compare_errors_sqlite,
    ):
        comparer = Comparer(sqlite_db_engine_one, sqlite_db_engine_two)
        result = comparer.compare()
        assert result.result == compare_result_sqlite
        assert result.errors == compare_errors_sqlite


class TestInspectorUnsupported(BaseTest):
    @pytest.fixture
    def inspector(self):
        class TestInspector(BaseInspector):
            key = "test_unsupported_inspector"

            def inspect(self, *args, **kwargs) -> dict:
                raise InspectorNotSupported("Test inspector is not supported")

            def diff(self, *args, **kwargs) -> dict:
                return {}

            def _is_supported(self, inspector) -> bool:
                return False

        yield TestInspector()
        register.pop("test_unsupported_inspector")

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def test_compare(
        self,
        db_engine_one,
        db_engine_two,
        inspector,
        caplog,
    ):
        comparer = Comparer(db_engine_one, db_engine_two)
        comparer.compare()
        assert len(caplog.records) == 2

        assert caplog.record_tuples[0][0] == "sqlalchemydiff.comparer"
        assert caplog.record_tuples[0][1] == logging.WARNING
        assert caplog.record_tuples[0][2] == str(
            {
                "engine": db_engine_one,
                "inspector": inspector.key,
                "error": "Test inspector is not supported",
            }
        )

        assert caplog.record_tuples[1][0] == "sqlalchemydiff.comparer"
        assert caplog.record_tuples[1][1] == logging.WARNING
        assert caplog.record_tuples[1][2] == str(
            {
                "engine": db_engine_two,
                "inspector": inspector.key,
                "error": "Test inspector is not supported",
            }
        )
