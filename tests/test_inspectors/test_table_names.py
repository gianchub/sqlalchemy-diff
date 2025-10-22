import pytest

from sqlalchemydiff.inspection import TablesInspector
from sqlalchemydiff.inspection.ignore import TableIgnoreSpec
from tests.base import BaseTest
from tests.util import assert_dicts_equal


class TestTablesInspector(BaseTest):
    @pytest.fixture
    def inspector(self):
        return TablesInspector()

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector(self, db_engine_one, inspector, table_names_one):
        result = inspector.inspect(db_engine_one)
        assert_dicts_equal(result, table_names_one)

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector_with_ignore_clauses(self, db_engine_one, inspector):
        tables_to_ignore = [
            TableIgnoreSpec("employees"),
            TableIgnoreSpec("roles"),
            TableIgnoreSpec("mobile_numbers"),
            TableIgnoreSpec("companies", "enums", "whatever"),
        ]
        expected_result = {
            "companies": {"name": "companies", "comment": ""},
            "skills": {
                "name": "skills",
                "comment": "Skills are the skills of the employees",
            },
            "tenures": {"name": "tenures", "comment": ""},
        }

        result = inspector.inspect(db_engine_one, ignore_specs=tables_to_ignore)

        assert_dicts_equal(result, expected_result)

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def testdiff(self, db_engine_one, db_engine_two, inspector):
        result_one = inspector.inspect(db_engine_one)
        result_two = inspector.inspect(db_engine_two)

        diff_result = inspector.diff(result_one, result_two)

        assert_dicts_equal(
            diff_result,
            {
                "common": [
                    {
                        "name": "skills",
                        "comment": "Skills are the skills of the employees",
                    },
                    {"name": "employees", "comment": ""},
                    {"name": "roles", "comment": ""},
                    {"name": "companies", "comment": ""},
                ],
                "diff": [
                    {
                        "one": {
                            "name": "mobile_numbers",
                            "comment": "Mobile numbers are the mobile numbers of the employees",
                        },
                        "two": {
                            "name": "mobile_numbers",
                            "comment": "Mobile numbers are the phone numbers of the employees",
                        },
                    }
                ],
                "one_only": [{"name": "tenures", "comment": ""}],
                "two_only": [{"name": "employments", "comment": ""}],
            },
        )
