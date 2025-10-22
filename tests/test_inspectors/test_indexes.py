import pytest

from sqlalchemydiff.inspection import IndexesInspector
from sqlalchemydiff.inspection.ignore import TableIgnoreSpec
from tests.base import BaseTest
from tests.util import assert_dicts_equal


class TestIndexesInspector(BaseTest):
    @pytest.fixture
    def inspector(self):
        return IndexesInspector()

    @pytest.fixture
    def indexes_one_with_ignores(self):
        return {
            "employees": [],
            "mobile_numbers": [],
            "skills": [],
            "tenures": [],
        }

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector(self, db_engine_one, inspector, indexes_one):
        result = inspector.inspect(db_engine_one)

        assert_dicts_equal(result, indexes_one)

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector_with_ignores(self, db_engine_one, inspector, indexes_one_with_ignores):
        ignore_specs = [
            TableIgnoreSpec("roles"),
            TableIgnoreSpec("companies"),
            TableIgnoreSpec("employees", "indexes", "ix_employees_name"),
            TableIgnoreSpec("tenures", "indexes", "DOES_NOT_EXIST"),
        ]

        result = inspector.inspect(db_engine_one, ignore_specs=ignore_specs)
        assert_dicts_equal(result, indexes_one_with_ignores)

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def testdiff(self, db_engine_one, db_engine_two, inspector):
        result_one = inspector.inspect(db_engine_one)
        result_two = inspector.inspect(db_engine_two)

        diff_result = inspector.diff(result_one, result_two)

        expected_result = {
            "companies": {
                "one_only": [
                    {
                        "name": "companies_name_key",
                        "unique": True,
                        "column_names": ["name"],
                        "include_columns": [],
                        "duplicates_constraint": "companies_name_key",
                        "dialect_options": {"postgresql_include": []},
                    }
                ],
                "two_only": [],
                "common": [],
                "diff": [],
            },
            "employees": {
                "one_only": [
                    {
                        "name": "ix_employees_name",
                        "unique": True,
                        "column_names": ["name"],
                        "include_columns": [],
                        "dialect_options": {"postgresql_include": []},
                    }
                ],
                "two_only": [
                    {
                        "name": "employees_name_key",
                        "unique": True,
                        "column_names": ["name"],
                        "include_columns": [],
                        "duplicates_constraint": "employees_name_key",
                        "dialect_options": {"postgresql_include": []},
                    },
                    {
                        "name": "idx_title_department",
                        "unique": False,
                        "column_names": ["title", "department"],
                        "include_columns": [],
                        "dialect_options": {"postgresql_include": []},
                    },
                    {
                        "name": "ix_employees_ssn",
                        "unique": False,
                        "column_names": ["ssn"],
                        "include_columns": [],
                        "dialect_options": {"postgresql_include": []},
                    },
                    {
                        "name": "unique_employee_name_age",
                        "unique": True,
                        "column_names": ["name", "age"],
                        "include_columns": [],
                        "duplicates_constraint": "unique_employee_name_age",
                        "dialect_options": {"postgresql_include": []},
                    },
                ],
                "common": [],
                "diff": [],
            },
            "employments": {"one_only": [], "two_only": [], "common": [], "diff": []},
            "mobile_numbers": {
                "one_only": [],
                "two_only": [],
                "common": [],
                "diff": [],
            },
            "roles": {
                "one_only": [],
                "two_only": [
                    {
                        "name": "ix_roles_name",
                        "unique": False,
                        "column_names": ["name"],
                        "include_columns": [],
                        "dialect_options": {"postgresql_include": []},
                    }
                ],
                "common": [],
                "diff": [],
            },
            "skills": {
                "one_only": [],
                "two_only": [
                    {
                        "name": "skills_description_key",
                        "unique": True,
                        "column_names": ["description"],
                        "include_columns": [],
                        "duplicates_constraint": "skills_description_key",
                        "dialect_options": {"postgresql_include": []},
                    }
                ],
                "common": [],
                "diff": [],
            },
            "tenures": {"one_only": [], "two_only": [], "common": [], "diff": []},
        }

        assert_dicts_equal(diff_result, expected_result)
