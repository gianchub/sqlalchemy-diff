import pytest

from sqlalchemydiff.inspection import ForeignKeysInspector
from sqlalchemydiff.inspection.ignore import TableIgnoreSpec
from tests.base import BaseTest
from tests.util import assert_dicts_equal


class TestForeignKeysInspector(BaseTest):
    @pytest.fixture
    def inspector(self):
        return ForeignKeysInspector()

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector(self, db_engine_one, inspector, foreign_keys_one):
        result = inspector.inspect(db_engine_one)

        assert_dicts_equal(result, foreign_keys_one)

    @pytest.fixture
    def foreign_keys_one_with_ignores(self):
        return {
            "companies": [],
            "mobile_numbers": [],
            "skills": [
                {
                    "constrained_columns": ["employee"],
                    "name": "fk_skills_employees",
                    "options": {},
                    "referred_columns": ["id"],
                    "referred_schema": None,
                    "referred_table": "employees",
                    "comment": None,
                }
            ],
            "tenures": [
                {
                    "constrained_columns": ["employee_id"],
                    "name": "fk_tenures_employees",
                    "options": {},
                    "referred_columns": ["id"],
                    "referred_schema": None,
                    "referred_table": "employees",
                    "comment": None,
                },
            ],
        }

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector_with_ignores(self, db_engine_one, inspector, foreign_keys_one_with_ignores):
        ignore_specs = [
            TableIgnoreSpec("employees"),
            TableIgnoreSpec("roles"),
            TableIgnoreSpec("mobile_numbers", "foreign_keys", "mobile_numbers_owner_fkey"),
            TableIgnoreSpec("tenures", "foreign_keys", "fk_tenures_companies"),
        ]

        result = inspector.inspect(db_engine_one, ignore_specs=ignore_specs)
        assert_dicts_equal(result, foreign_keys_one_with_ignores)

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def testdiff(self, db_engine_one, db_engine_two, inspector):
        result_one = inspector.inspect(db_engine_one)
        result_two = inspector.inspect(db_engine_two)

        diff_result = inspector.diff(result_one, result_two)

        expected_result = {
            "companies": {"one_only": [], "two_only": [], "common": [], "diff": []},
            "employees": {
                "one_only": [],
                "two_only": [],
                "common": [
                    {
                        "name": "fk_employees_companies",
                        "constrained_columns": ["company_id"],
                        "referred_schema": None,
                        "referred_table": "companies",
                        "referred_columns": ["id"],
                        "options": {},
                        "comment": None,
                    },
                    {
                        "name": "fk_employees_roles",
                        "constrained_columns": ["role_id"],
                        "referred_schema": None,
                        "referred_table": "roles",
                        "referred_columns": ["id"],
                        "options": {},
                        "comment": None,
                    },
                ],
                "diff": [],
            },
            "employments": {
                "one_only": [],
                "two_only": [
                    {
                        "name": "fk_employments_companies",
                        "constrained_columns": ["company_id"],
                        "referred_schema": None,
                        "referred_table": "companies",
                        "referred_columns": ["id"],
                        "options": {},
                        "comment": None,
                    },
                    {
                        "name": "fk_employments_employees",
                        "constrained_columns": ["employee_id"],
                        "referred_schema": None,
                        "referred_table": "employees",
                        "referred_columns": ["id"],
                        "options": {},
                        "comment": None,
                    },
                ],
                "common": [],
                "diff": [],
            },
            "mobile_numbers": {
                "one_only": [
                    {
                        "name": "mobile_numbers_owner_fkey",
                        "constrained_columns": ["owner"],
                        "referred_schema": None,
                        "referred_table": "employees",
                        "referred_columns": ["id"],
                        "options": {},
                        "comment": None,
                    }
                ],
                "two_only": [
                    {
                        "name": "foreign_key_mobile_numbers_employees",
                        "constrained_columns": ["owner"],
                        "referred_schema": None,
                        "referred_table": "employees",
                        "referred_columns": ["id"],
                        "options": {},
                        "comment": None,
                    }
                ],
                "common": [],
                "diff": [],
            },
            "roles": {"one_only": [], "two_only": [], "common": [], "diff": []},
            "skills": {
                "one_only": [],
                "two_only": [],
                "common": [],
                "diff": [
                    {
                        "one": {
                            "name": "fk_skills_employees",
                            "constrained_columns": ["employee"],
                            "referred_schema": None,
                            "referred_table": "employees",
                            "referred_columns": ["id"],
                            "options": {},
                            "comment": None,
                        },
                        "two": {
                            "name": "fk_skills_employees",
                            "constrained_columns": ["person"],
                            "referred_schema": None,
                            "referred_table": "employees",
                            "referred_columns": ["id"],
                            "options": {},
                            "comment": None,
                        },
                    }
                ],
            },
            "tenures": {
                "one_only": [
                    {
                        "name": "fk_tenures_companies",
                        "constrained_columns": ["company_id"],
                        "referred_schema": None,
                        "referred_table": "companies",
                        "referred_columns": ["id"],
                        "options": {},
                        "comment": None,
                    },
                    {
                        "name": "fk_tenures_employees",
                        "constrained_columns": ["employee_id"],
                        "referred_schema": None,
                        "referred_table": "employees",
                        "referred_columns": ["id"],
                        "options": {},
                        "comment": None,
                    },
                ],
                "two_only": [],
                "common": [],
                "diff": [],
            },
        }

        assert_dicts_equal(diff_result, expected_result)
