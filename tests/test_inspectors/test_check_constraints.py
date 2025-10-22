import pytest

from sqlalchemydiff.inspection import CheckConstraintsInspector
from sqlalchemydiff.inspection.ignore import TableIgnoreSpec
from tests.base import BaseTest
from tests.util import assert_dicts_equal


class TestCheckConstraintsInspector(BaseTest):
    @pytest.fixture
    def inspector(self):
        return CheckConstraintsInspector()

    @pytest.fixture
    def check_constraints_one_with_ignores(self):
        return {
            "employees": [
                {
                    "name": "check_age",
                    "sqltext": "age > 0 AND age <= 100",
                    "comment": None,
                }
            ],
            "roles": [],
            "skills": [],
            "mobile_numbers": [],
            "tenures": [],
        }

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector(self, db_engine_one, inspector, check_constraints_one):
        result = inspector.inspect(db_engine_one)

        assert_dicts_equal(result, check_constraints_one)

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector_with_ignores(
        self, db_engine_one, inspector, check_constraints_one_with_ignores
    ):
        ignore_specs = [
            TableIgnoreSpec("companies"),
            TableIgnoreSpec("employees", "check_constraints", "DOES_NOT_EXIST"),
            TableIgnoreSpec("roles", "check_constraints", "check_name"),
        ]

        result = inspector.inspect(db_engine_one, ignore_specs=ignore_specs)
        assert_dicts_equal(result, check_constraints_one_with_ignores)

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def testdiff(self, db_engine_one, db_engine_two, inspector):
        result_one = inspector.inspect(db_engine_one)
        result_two = inspector.inspect(db_engine_two)

        diff_result = inspector.diff(result_one, result_two)

        expected_result = {
            "companies": {
                "one_only": [],
                "two_only": [],
                "common": [],
                "diff": [],
            },
            "employees": {
                "one_only": [],
                "two_only": [],
                "common": [],
                "diff": [
                    {
                        "one": {
                            "name": "check_age",
                            "sqltext": "age > 0 AND age <= 100",
                            "comment": None,
                        },
                        "two": {
                            "name": "check_age",
                            "sqltext": "age > 0 AND age <= 90",
                            "comment": None,
                        },
                    }
                ],
            },
            "employments": {
                "one_only": [],
                "two_only": [
                    {
                        "name": "check_end_date_after_start_date",
                        "sqltext": "end_date > start_date",
                        "comment": None,
                    }
                ],
                "common": [],
                "diff": [],
            },
            "mobile_numbers": {
                "one_only": [],
                "two_only": [],
                "common": [],
                "diff": [],
            },
            "roles": {
                "one_only": [],
                "two_only": [],
                "common": [
                    {
                        "name": "check_name",
                        "sqltext": "length(name::text) > 5",
                        "comment": None,
                    }
                ],
                "diff": [],
            },
            "skills": {
                "one_only": [],
                "two_only": [],
                "common": [],
                "diff": [],
            },
            "tenures": {"one_only": [], "two_only": [], "common": [], "diff": []},
        }

        assert_dicts_equal(diff_result, expected_result)
