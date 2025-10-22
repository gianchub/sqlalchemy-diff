import pytest

from sqlalchemydiff.inspection import PrimaryKeysInspector
from sqlalchemydiff.inspection.ignore import TableIgnoreSpec
from tests.base import BaseTest
from tests.util import assert_dicts_equal


class TestPrimaryKeysInspector(BaseTest):
    @pytest.fixture
    def inspector(self):
        return PrimaryKeysInspector()

    @pytest.fixture
    def primary_keys_one_with_ignores(self):
        return {
            "roles": {
                "constrained_columns": ["id"],
                "name": "roles_pkey",
                "comment": None,
                "dialect_options": {"postgresql_include": []},
            },
            "skills": {
                "constrained_columns": ["slug"],
                "name": "skills_pkey",
                "comment": None,
                "dialect_options": {"postgresql_include": []},
            },
            "mobile_numbers": {
                "constrained_columns": ["id"],
                "name": "mobile_numbers_pkey",
                "comment": None,
                "dialect_options": {"postgresql_include": []},
            },
            "tenures": {},
        }

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector(self, db_engine_one, inspector, primary_keys_one):
        result = inspector.inspect(db_engine_one)

        assert_dicts_equal(result, primary_keys_one)

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector_with_ignores(self, db_engine_one, inspector, primary_keys_one_with_ignores):
        ignore_specs = [
            TableIgnoreSpec("companies"),
            TableIgnoreSpec("employees"),
            TableIgnoreSpec("tenures", "primary_keys", "tenures_pkey"),
        ]

        result = inspector.inspect(db_engine_one, ignore_specs=ignore_specs)
        assert_dicts_equal(result, primary_keys_one_with_ignores)

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def testdiff(self, db_engine_one, db_engine_two, inspector):
        result_one = inspector.inspect(db_engine_one)
        result_two = inspector.inspect(db_engine_two)

        diff_result = inspector.diff(result_one, result_two)

        expected_result = {
            "companies": {
                "one_only": [],
                "two_only": [],
                "common": [
                    {
                        "constrained_columns": ["id"],
                        "name": "companies_pkey",
                        "comment": None,
                        "dialect_options": {"postgresql_include": []},
                    }
                ],
                "diff": [],
            },
            "employees": {
                "one_only": [],
                "two_only": [],
                "common": [
                    {
                        "constrained_columns": ["id"],
                        "name": "employees_pkey",
                        "comment": None,
                        "dialect_options": {"postgresql_include": []},
                    }
                ],
                "diff": [],
            },
            "employments": {
                "one_only": [],
                "two_only": {
                    "constrained_columns": ["employee_id", "company_id"],
                    "name": "employments_pkey",
                    "comment": None,
                    "dialect_options": {"postgresql_include": []},
                },
                "common": [],
                "diff": [],
            },
            "mobile_numbers": {
                "one_only": [],
                "two_only": [],
                "common": [],
                "diff": [
                    {
                        "one": {
                            "constrained_columns": ["id"],
                            "name": "mobile_numbers_pkey",
                            "comment": None,
                            "dialect_options": {"postgresql_include": []},
                        },
                        "two": {
                            "constrained_columns": ["number"],
                            "name": "mobile_numbers_pkey",
                            "comment": None,
                            "dialect_options": {"postgresql_include": []},
                        },
                    }
                ],
            },
            "roles": {
                "one_only": [],
                "two_only": [],
                "common": [
                    {
                        "constrained_columns": ["id"],
                        "name": "roles_pkey",
                        "comment": None,
                        "dialect_options": {"postgresql_include": []},
                    }
                ],
                "diff": [],
            },
            "skills": {
                "one_only": [],
                "two_only": [],
                "common": [
                    {
                        "constrained_columns": ["slug"],
                        "name": "skills_pkey",
                        "comment": None,
                        "dialect_options": {"postgresql_include": []},
                    }
                ],
                "diff": [],
            },
            "tenures": {
                "one_only": {
                    "constrained_columns": ["employee_id", "company_id"],
                    "name": "tenures_pkey",
                    "comment": None,
                    "dialect_options": {"postgresql_include": []},
                },
                "two_only": [],
                "common": [],
                "diff": [],
            },
        }

        assert_dicts_equal(diff_result, expected_result)
