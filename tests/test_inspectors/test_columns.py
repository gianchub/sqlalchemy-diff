import pytest

from sqlalchemydiff.inspection import ColumnsInspector
from sqlalchemydiff.inspection.ignore import TableIgnoreSpec
from tests.base import BaseTest
from tests.util import assert_dicts_equal


class TestColumnsInspector(BaseTest):
    @pytest.fixture
    def inspector(self):
        return ColumnsInspector()

    @pytest.fixture
    def columns_one_with_ignores(self):
        return {
            "roles": [
                {
                    "name": "id",
                    "comment": None,
                    "type": "INTEGER",
                    "nullable": False,
                    "default": "nextval('roles_id_seq'::regclass)",
                    "autoincrement": True,
                },
            ],
            "skills": [
                {
                    "name": "slug",
                    "comment": None,
                    "type": "VARCHAR(50)",
                    "nullable": False,
                    "default": None,
                    "autoincrement": False,
                },
                {
                    "name": "employee",
                    "comment": None,
                    "type": "INTEGER",
                    "nullable": False,
                    "default": None,
                    "autoincrement": False,
                },
            ],
        }

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector(self, db_engine_one, inspector, columns_one):
        result = inspector.inspect(db_engine_one)
        assert_dicts_equal(result, columns_one)

    @pytest.mark.usefixtures("setup_db_one")
    def test_inspector_with_ignores(self, db_engine_one, inspector, columns_one_with_ignores):
        ignore_specs = [
            TableIgnoreSpec("employees"),
            TableIgnoreSpec("companies"),
            TableIgnoreSpec("mobile_numbers"),
            TableIgnoreSpec("tenures"),
            TableIgnoreSpec("roles", "columns", "name"),
            TableIgnoreSpec("roles", "columns", "role_type"),
            TableIgnoreSpec("skills", "columns", "description"),
        ]

        result = inspector.inspect(db_engine_one, ignore_specs=ignore_specs)
        assert_dicts_equal(result, columns_one_with_ignores)

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def testdiff(self, db_engine_one, db_engine_two, inspector):
        result_one = inspector.inspect(db_engine_one)
        result_two = inspector.inspect(db_engine_two)

        diff_result = inspector.diff(result_one, result_two)

        expected_result = {
            "companies": {
                "one_only": [],
                "two_only": [
                    {
                        "name": "company_type",
                        "type": "company_type",
                        "nullable": True,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    }
                ],
                "common": [],
                "diff": [
                    {
                        "one": {
                            "name": "id",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": "nextval('companies_id_seq'::regclass)",
                            "autoincrement": True,
                            "comment": None,
                        },
                        "two": {
                            "name": "id",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                    },
                    {
                        "one": {
                            "name": "name",
                            "type": "VARCHAR(200)",
                            "nullable": False,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                        "two": {
                            "name": "name",
                            "type": "VARCHAR(200)",
                            "nullable": True,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                    },
                ],
            },
            "employees": {
                "one_only": [],
                "two_only": [],
                "common": [
                    {
                        "name": "company_id",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                    {
                        "name": "department",
                        "type": "VARCHAR(11)",
                        "nullable": True,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                    {
                        "name": "id",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": "nextval('employees_id_seq'::regclass)",
                        "autoincrement": True,
                        "comment": None,
                    },
                    {
                        "name": "name",
                        "type": "VARCHAR(200)",
                        "nullable": True,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                    {
                        "name": "ssn",
                        "type": "VARCHAR(30)",
                        "nullable": False,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                    {
                        "name": "title",
                        "type": "title",
                        "nullable": True,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                ],
                "diff": [
                    {
                        "one": {
                            "name": "age",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                        "two": {
                            "name": "age",
                            "type": "INTEGER",
                            "nullable": True,
                            "default": "21",
                            "autoincrement": False,
                            "comment": None,
                        },
                    },
                    {
                        "one": {
                            "name": "number_of_pets",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                        "two": {
                            "name": "number_of_pets",
                            "type": "BIGINT",
                            "nullable": True,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                    },
                    {
                        "one": {
                            "name": "role_id",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                        "two": {
                            "name": "role_id",
                            "type": "VARCHAR(50)",
                            "nullable": False,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                    },
                ],
            },
            "employments": {
                "one_only": [],
                "two_only": [
                    {
                        "name": "employee_id",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                    {
                        "name": "company_id",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                    {
                        "name": "start_date",
                        "type": "TIMESTAMP WITH TIME ZONE",
                        "nullable": False,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                    {
                        "name": "end_date",
                        "type": "TIMESTAMP WITH TIME ZONE",
                        "nullable": True,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                ],
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
                            "name": "id",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": "nextval('mobile_numbers_id_seq'::regclass)",
                            "autoincrement": True,
                            "comment": None,
                        },
                        "two": {
                            "name": "id",
                            "type": "INTEGER",
                            "nullable": True,
                            "default": None,
                            "autoincrement": False,
                            "comment": "The ID of the mobile number",
                        },
                    },
                    {
                        "one": {
                            "name": "number",
                            "type": "VARCHAR(40)",
                            "nullable": False,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                        "two": {
                            "name": "number",
                            "type": "VARCHAR(50)",
                            "nullable": False,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                    },
                    {
                        "one": {
                            "name": "owner",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                        "two": {
                            "name": "owner",
                            "type": "INTEGER",
                            "nullable": True,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                    },
                ],
            },
            "roles": {
                "one_only": [],
                "two_only": [],
                "common": [
                    {
                        "name": "name",
                        "type": "VARCHAR(50)",
                        "nullable": False,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                    {
                        "name": "role_type",
                        "type": "role_type",
                        "nullable": True,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                ],
                "diff": [
                    {
                        "one": {
                            "name": "id",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": "nextval('roles_id_seq'::regclass)",
                            "autoincrement": True,
                            "comment": None,
                        },
                        "two": {
                            "name": "id",
                            "type": "VARCHAR(50)",
                            "nullable": False,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                    }
                ],
            },
            "skills": {
                "one_only": [
                    {
                        "name": "employee",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    }
                ],
                "two_only": [
                    {
                        "name": "person",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    }
                ],
                "common": [
                    {
                        "name": "slug",
                        "type": "VARCHAR(50)",
                        "nullable": False,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    }
                ],
                "diff": [
                    {
                        "one": {
                            "name": "description",
                            "type": "VARCHAR(100)",
                            "nullable": True,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                        "two": {
                            "name": "description",
                            "type": "VARCHAR(100)",
                            "nullable": False,
                            "default": None,
                            "autoincrement": False,
                            "comment": None,
                        },
                    }
                ],
            },
            "tenures": {
                "one_only": [
                    {
                        "name": "employee_id",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                    {
                        "name": "company_id",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                    {
                        "name": "start_date",
                        "type": "TIMESTAMP WITH TIME ZONE",
                        "nullable": False,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                    {
                        "name": "end_date",
                        "type": "TIMESTAMP WITH TIME ZONE",
                        "nullable": True,
                        "default": None,
                        "autoincrement": False,
                        "comment": None,
                    },
                ],
                "two_only": [],
                "common": [],
                "diff": [],
            },
        }

        assert_dicts_equal(diff_result, expected_result)
