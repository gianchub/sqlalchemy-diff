import pytest

from sqlalchemydiff.inspection import EnumsInspector
from sqlalchemydiff.inspection.ignore import EnumIgnoreSpec
from tests.base import BaseTest
from tests.util import assert_dicts_equal, assert_items_equal


class TestEnumsInspector(BaseTest):
    @pytest.fixture
    def inspector(self):
        return EnumsInspector()

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector(self, db_engine_one, inspector, enums_one):
        result = inspector.inspect(db_engine_one)
        assert_items_equal(result, enums_one)

    @pytest.fixture
    def enums_one_with_ignores(self):
        return [
            {
                "name": "title",
                "schema": "public",
                "visible": True,
                "labels": ["ENGINEER", "MANAGER", "DIRECTOR", "CEO"],
            },
        ]

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector_with_ignores(self, db_engine_one, inspector, enums_one_with_ignores):
        ignore_specs = [
            EnumIgnoreSpec("role_type"),
        ]
        result = inspector.inspect(db_engine_one, ignore_specs=ignore_specs)
        assert_items_equal(result, enums_one_with_ignores)

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def testdiff(self, db_engine_one, db_engine_two, inspector):
        result_one = inspector.inspect(db_engine_one)
        result_two = inspector.inspect(db_engine_two)

        diff_result = inspector.diff(result_one, result_two)

        expected_result = {
            "one_only": [],
            "two_only": [
                {
                    "name": "company_type",
                    "schema": "public",
                    "visible": True,
                    "labels": ["Public", "Private", "Sole Trader"],
                }
            ],
            "common": [
                {
                    "name": "role_type",
                    "schema": "public",
                    "visible": True,
                    "labels": ["Permanent", "Contractor"],
                }
            ],
            "diff": [
                {
                    "one": {
                        "labels": ["ENGINEER", "MANAGER", "DIRECTOR", "CEO"],
                        "name": "title",
                        "schema": "public",
                        "visible": True,
                    },
                    "two": {
                        "labels": ["ENGINEER", "DIRECTOR", "CEO", "VP"],
                        "name": "title",
                        "schema": "public",
                        "visible": True,
                    },
                }
            ],
        }

        assert_dicts_equal(diff_result, expected_result)
