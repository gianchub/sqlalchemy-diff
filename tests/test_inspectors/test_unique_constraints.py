import pytest

from sqlalchemydiff.inspection import UniqueConstraintsInspector
from sqlalchemydiff.inspection.ignore import TableIgnoreSpec
from tests.base import BaseTest
from tests.util import assert_dicts_equal


class TestUniqueConstraintsInspector(BaseTest):
    @pytest.fixture
    def inspector(self):
        return UniqueConstraintsInspector()

    @pytest.fixture
    def unique_constraints_one_with_ignores(self):
        return {
            "companies": [],
            "skills": [],
            "mobile_numbers": [],
            "tenures": [],
        }

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector(self, db_engine_one, inspector, unique_constraints_one):
        result = inspector.inspect(db_engine_one)

        assert_dicts_equal(result, unique_constraints_one)

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector_with_ignores(
        self, db_engine_one, inspector, unique_constraints_one_with_ignores
    ):
        ignore_specs = [
            TableIgnoreSpec("employees"),
            TableIgnoreSpec("roles"),
            TableIgnoreSpec("companies", "unique_constraints", "companies_name_key"),
            TableIgnoreSpec("skills", "unique_constraints", "DOES_NOT_EXIST"),
        ]

        result = inspector.inspect(db_engine_one, ignore_specs=ignore_specs)
        assert_dicts_equal(result, unique_constraints_one_with_ignores)

    @pytest.fixture
    def expecteddiff(self):
        return {
            "companies": {
                "one_only": [
                    {
                        "name": "companies_name_key",
                        "column_names": ["name"],
                        "comment": None,
                        "dialect_options": {
                            "postgresql_include": [],
                            "postgresql_nulls_not_distinct": False,
                        },
                    }
                ],
                "two_only": [],
                "common": [],
                "diff": [],
            },
            "employees": {
                "one_only": [],
                "two_only": [
                    {
                        "name": "employees_name_key",
                        "column_names": ["name"],
                        "comment": None,
                        "dialect_options": {
                            "postgresql_include": [],
                            "postgresql_nulls_not_distinct": False,
                        },
                    },
                    {
                        "name": "unique_employee_name_age",
                        "column_names": ["name", "age"],
                        "comment": None,
                        "dialect_options": {
                            "postgresql_include": [],
                            "postgresql_nulls_not_distinct": False,
                        },
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
            "roles": {"one_only": [], "two_only": [], "common": [], "diff": []},
            "skills": {
                "one_only": [],
                "two_only": [
                    {
                        "name": "skills_description_key",
                        "column_names": ["description"],
                        "comment": None,
                        "dialect_options": {
                            "postgresql_include": [],
                            "postgresql_nulls_not_distinct": False,
                        },
                    }
                ],
                "common": [],
                "diff": [],
            },
            "tenures": {"one_only": [], "two_only": [], "common": [], "diff": []},
        }

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def testdiff(self, db_engine_one, db_engine_two, inspector, expecteddiff):
        result_one = inspector.inspect(db_engine_one)
        result_two = inspector.inspect(db_engine_two)

        diff_result = inspector.diff(result_one, result_two)

        assert_dicts_equal(diff_result, expecteddiff)
