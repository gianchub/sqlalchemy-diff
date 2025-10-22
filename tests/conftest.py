import pytest


def pytest_addoption(parser):
    """Add command line options for the database connection."""
    parser.addoption("--db-user", action="store", default=None, help="Database user")
    parser.addoption("--db-password", action="store", default=None, help="Database password")
    parser.addoption("--db-host", action="store", default=None, help="Database host")
    parser.addoption("--db-port", action="store", default=None, help="Database port")


@pytest.fixture
def config(pytestconfig):
    return {
        "postgres": {
            "user": pytestconfig.getoption("--db-user"),
            "password": pytestconfig.getoption("--db-password"),
            "host": pytestconfig.getoption("--db-host"),
            "port": pytestconfig.getoption("--db-port"),
        },
    }


@pytest.fixture
def make_postgres_uri(config):
    def _make_uri(db_name):
        postgres_cfg = config["postgres"]
        return (
            f"postgresql://{postgres_cfg['user']}:{postgres_cfg['password']}@"
            f"{postgres_cfg['host']}:{postgres_cfg['port']}/{db_name}"
        )

    return _make_uri


@pytest.fixture
def table_names_one():
    return {
        "employees": {"name": "employees", "comment": ""},
        "companies": {"name": "companies", "comment": ""},
        "roles": {"name": "roles", "comment": ""},
        "skills": {
            "name": "skills",
            "comment": "Skills are the skills of the employees",
        },
        "mobile_numbers": {
            "name": "mobile_numbers",
            "comment": "Mobile numbers are the mobile numbers of the employees",
        },
        "tenures": {"name": "tenures", "comment": ""},
    }


@pytest.fixture
def columns_one():
    return {
        "employees": [
            {
                "name": "id",
                "comment": None,
                "type": "INTEGER",
                "nullable": False,
                "default": "nextval('employees_id_seq'::regclass)",
                "autoincrement": True,
            },
            {
                "name": "name",
                "comment": None,
                "type": "VARCHAR(200)",
                "nullable": True,
                "default": None,
                "autoincrement": False,
            },
            {
                "name": "age",
                "comment": None,
                "type": "INTEGER",
                "nullable": False,
                "default": None,
                "autoincrement": False,
            },
            {
                "name": "ssn",
                "comment": None,
                "type": "VARCHAR(30)",
                "nullable": False,
                "default": None,
                "autoincrement": False,
            },
            {
                "name": "number_of_pets",
                "comment": None,
                "type": "INTEGER",
                "nullable": False,
                "default": None,
                "autoincrement": False,
            },
            {
                "name": "title",
                "comment": None,
                "type": "title",
                "nullable": True,
                "default": None,
                "autoincrement": False,
            },
            {
                "name": "department",
                "comment": None,
                "type": "VARCHAR(11)",
                "nullable": True,
                "default": None,
                "autoincrement": False,
            },
            {
                "name": "company_id",
                "comment": None,
                "type": "INTEGER",
                "nullable": False,
                "default": None,
                "autoincrement": False,
            },
            {
                "name": "role_id",
                "comment": None,
                "type": "INTEGER",
                "nullable": False,
                "default": None,
                "autoincrement": False,
            },
        ],
        "companies": [
            {
                "name": "id",
                "comment": None,
                "type": "INTEGER",
                "nullable": False,
                "default": "nextval('companies_id_seq'::regclass)",
                "autoincrement": True,
            },
            {
                "name": "name",
                "comment": None,
                "type": "VARCHAR(200)",
                "nullable": False,
                "default": None,
                "autoincrement": False,
            },
        ],
        "roles": [
            {
                "name": "id",
                "comment": None,
                "type": "INTEGER",
                "nullable": False,
                "default": "nextval('roles_id_seq'::regclass)",
                "autoincrement": True,
            },
            {
                "name": "name",
                "comment": None,
                "type": "VARCHAR(50)",
                "nullable": False,
                "default": None,
                "autoincrement": False,
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
                "name": "description",
                "comment": None,
                "type": "VARCHAR(100)",
                "nullable": True,
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
        "mobile_numbers": [
            {
                "name": "id",
                "comment": None,
                "type": "INTEGER",
                "nullable": False,
                "default": "nextval('mobile_numbers_id_seq'::regclass)",
                "autoincrement": True,
            },
            {
                "name": "number",
                "comment": None,
                "type": "VARCHAR(40)",
                "nullable": False,
                "default": None,
                "autoincrement": False,
            },
            {
                "name": "owner",
                "comment": None,
                "type": "INTEGER",
                "nullable": False,
                "default": None,
                "autoincrement": False,
            },
        ],
        "tenures": [
            {
                "name": "employee_id",
                "comment": None,
                "type": "INTEGER",
                "nullable": False,
                "default": None,
                "autoincrement": False,
            },
            {
                "name": "company_id",
                "comment": None,
                "type": "INTEGER",
                "nullable": False,
                "default": None,
                "autoincrement": False,
            },
            {
                "name": "start_date",
                "comment": None,
                "type": "TIMESTAMP WITH TIME ZONE",
                "nullable": False,
                "default": None,
                "autoincrement": False,
            },
            {
                "name": "end_date",
                "comment": None,
                "type": "TIMESTAMP WITH TIME ZONE",
                "nullable": True,
                "default": None,
                "autoincrement": False,
            },
        ],
    }


@pytest.fixture
def primary_keys_one():
    return {
        "employees": {
            "constrained_columns": ["id"],
            "name": "employees_pkey",
            "comment": None,
            "dialect_options": {"postgresql_include": []},
        },
        "companies": {
            "constrained_columns": ["id"],
            "name": "companies_pkey",
            "comment": None,
            "dialect_options": {"postgresql_include": []},
        },
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
        "tenures": {
            "constrained_columns": ["employee_id", "company_id"],
            "name": "tenures_pkey",
            "comment": None,
            "dialect_options": {"postgresql_include": []},
        },
    }


@pytest.fixture
def foreign_keys_one():
    return {
        "companies": [],
        "employees": [
            {
                "constrained_columns": ["company_id"],
                "name": "fk_employees_companies",
                "options": {},
                "referred_columns": ["id"],
                "referred_schema": None,
                "referred_table": "companies",
                "comment": None,
            },
            {
                "constrained_columns": ["role_id"],
                "name": "fk_employees_roles",
                "options": {},
                "referred_columns": ["id"],
                "referred_schema": None,
                "referred_table": "roles",
                "comment": None,
            },
        ],
        "mobile_numbers": [
            {
                "constrained_columns": ["owner"],
                "name": "mobile_numbers_owner_fkey",
                "options": {},
                "referred_columns": ["id"],
                "referred_schema": None,
                "referred_table": "employees",
                "comment": None,
            }
        ],
        "roles": [],
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
                "constrained_columns": ["company_id"],
                "name": "fk_tenures_companies",
                "options": {},
                "referred_columns": ["id"],
                "referred_schema": None,
                "referred_table": "companies",
                "comment": None,
            },
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


@pytest.fixture
def indexes_one():
    return {
        "companies": [
            {
                "column_names": ["name"],
                "dialect_options": {"postgresql_include": []},
                "duplicates_constraint": "companies_name_key",
                "include_columns": [],
                "name": "companies_name_key",
                "unique": True,
            }
        ],
        "employees": [
            {
                "column_names": ["name"],
                "dialect_options": {"postgresql_include": []},
                "include_columns": [],
                "name": "ix_employees_name",
                "unique": True,
            }
        ],
        "mobile_numbers": [],
        "roles": [],
        "skills": [],
        "tenures": [],
    }


@pytest.fixture
def unique_constraints_one():
    return {
        "companies": [
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
        "employees": [],
        "roles": [],
        "skills": [],
        "mobile_numbers": [],
        "tenures": [],
    }


@pytest.fixture
def check_constraints_one():
    return {
        "companies": [],
        "employees": [
            {
                "name": "check_age",
                "sqltext": "age > 0 AND age <= 100",
                "comment": None,
            }
        ],
        "roles": [{"name": "check_name", "sqltext": "length(name::text) > 5", "comment": None}],
        "skills": [],
        "mobile_numbers": [],
        "tenures": [],
    }


@pytest.fixture
def enums_one():
    return [
        {
            "name": "title",
            "schema": "public",
            "visible": True,
            "labels": ["ENGINEER", "MANAGER", "DIRECTOR", "CEO"],
        },
        {
            "name": "role_type",
            "schema": "public",
            "visible": True,
            "labels": ["Permanent", "Contractor"],
        },
    ]


@pytest.fixture
def compare_result_tables_factory():
    def compare_result_tables(one_alias="one", two_alias="two"):
        return {
            f"{one_alias}_only": [{"name": "tenures", "comment": ""}],
            f"{two_alias}_only": [{"name": "employments", "comment": ""}],
            "common": [
                {"name": "companies", "comment": ""},
                {"name": "employees", "comment": ""},
                {"name": "roles", "comment": ""},
                {"name": "skills", "comment": "Skills are the skills of the employees"},
            ],
            "diff": [
                {
                    f"{one_alias}": {
                        "name": "mobile_numbers",
                        "comment": "Mobile numbers are the mobile numbers of the employees",
                    },
                    f"{two_alias}": {
                        "name": "mobile_numbers",
                        "comment": "Mobile numbers are the phone numbers of the employees",
                    },
                }
            ],
        }

    return compare_result_tables


@pytest.fixture
def compare_result_columns():
    return {
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


@pytest.fixture
def compare_result_primary_keys():
    return {
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


@pytest.fixture
def compare_result_foreign_keys():
    return {
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


@pytest.fixture
def compare_result_indexes():
    return {
        "companies": {
            "one_only": [
                {
                    "name": "companies_name_key",
                    "unique": True,
                    "column_names": ["name"],
                    "duplicates_constraint": "companies_name_key",
                    "include_columns": [],
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
                    "duplicates_constraint": "employees_name_key",
                    "include_columns": [],
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
                    "duplicates_constraint": "unique_employee_name_age",
                    "include_columns": [],
                    "dialect_options": {"postgresql_include": []},
                },
            ],
            "common": [],
            "diff": [],
        },
        "employments": {"one_only": [], "two_only": [], "common": [], "diff": []},
        "mobile_numbers": {"one_only": [], "two_only": [], "common": [], "diff": []},
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
                    "duplicates_constraint": "skills_description_key",
                    "include_columns": [],
                    "dialect_options": {"postgresql_include": []},
                }
            ],
            "common": [],
            "diff": [],
        },
        "tenures": {"one_only": [], "two_only": [], "common": [], "diff": []},
    }


@pytest.fixture
def compare_result_enums():
    return {
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
                    "name": "title",
                    "schema": "public",
                    "visible": True,
                    "labels": ["ENGINEER", "MANAGER", "DIRECTOR", "CEO"],
                },
                "two": {
                    "name": "title",
                    "schema": "public",
                    "visible": True,
                    "labels": ["ENGINEER", "DIRECTOR", "CEO", "VP"],
                },
            }
        ],
    }


@pytest.fixture
def compare_result_unique_constraints():
    return {
        "companies": {
            "one_only": [
                {
                    "column_names": ["name"],
                    "name": "companies_name_key",
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
                    "column_names": ["name"],
                    "name": "employees_name_key",
                    "comment": None,
                    "dialect_options": {
                        "postgresql_include": [],
                        "postgresql_nulls_not_distinct": False,
                    },
                },
                {
                    "column_names": ["name", "age"],
                    "name": "unique_employee_name_age",
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
        "mobile_numbers": {"one_only": [], "two_only": [], "common": [], "diff": []},
        "roles": {"one_only": [], "two_only": [], "common": [], "diff": []},
        "skills": {
            "one_only": [],
            "two_only": [
                {
                    "column_names": ["description"],
                    "name": "skills_description_key",
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


@pytest.fixture
def compare_result_check_constraints():
    return {
        "companies": {"one_only": [], "two_only": [], "common": [], "diff": []},
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
        "mobile_numbers": {"one_only": [], "two_only": [], "common": [], "diff": []},
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
        "skills": {"one_only": [], "two_only": [], "common": [], "diff": []},
        "tenures": {"one_only": [], "two_only": [], "common": [], "diff": []},
    }


@pytest.fixture
def compare_result_v14(
    compare_result_tables_factory,
    compare_result_columns,
    compare_result_primary_keys,
    compare_result_foreign_keys,
    compare_result_enums,
    compare_result_indexes,
    compare_result_unique_constraints,
    compare_result_check_constraints,
):
    return {
        "tables": compare_result_tables_factory(),
        "columns": compare_result_columns,
        "primary_keys": compare_result_primary_keys,
        "foreign_keys": compare_result_foreign_keys,
        "indexes": compare_result_indexes,
        "unique_constraints": compare_result_unique_constraints,
        "check_constraints": compare_result_check_constraints,
        "enums": compare_result_enums,
    }


@pytest.fixture
def compare_result(
    compare_result_tables_factory,
    compare_result_columns,
    compare_result_primary_keys,
    compare_result_foreign_keys,
    compare_result_enums,
    compare_result_indexes,
    compare_result_unique_constraints,
    compare_result_check_constraints,
):
    return {
        "tables": compare_result_tables_factory(),
        "columns": compare_result_columns,
        "primary_keys": compare_result_primary_keys,
        "foreign_keys": compare_result_foreign_keys,
        "indexes": compare_result_indexes,
        "unique_constraints": compare_result_unique_constraints,
        "check_constraints": compare_result_check_constraints,
        "enums": compare_result_enums,
    }


@pytest.fixture
def compare_result_aliases(compare_result_tables_factory):
    return {"tables": compare_result_tables_factory("production", "staging")}


@pytest.fixture
def compare_errors_tables_factory():
    def compare_errors_tables(one_alias="one", two_alias="two"):
        return {
            f"{one_alias}_only": [{"name": "tenures", "comment": ""}],
            f"{two_alias}_only": [{"name": "employments", "comment": ""}],
            "diff": [
                {
                    f"{one_alias}": {
                        "name": "mobile_numbers",
                        "comment": "Mobile numbers are the mobile numbers of the employees",
                    },
                    f"{two_alias}": {
                        "name": "mobile_numbers",
                        "comment": "Mobile numbers are the phone numbers of the employees",
                    },
                }
            ],
        }

    return compare_errors_tables


@pytest.fixture
def compare_errors_columns():
    return {
        "companies": {
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
            ]
        },
        "employments": {
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
            ]
        },
        "mobile_numbers": {
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
            ]
        },
        "roles": {
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
            ]
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
            ]
        },
    }


@pytest.fixture
def compare_errors_primary_keys():
    return {
        "employments": {
            "two_only": {
                "constrained_columns": ["employee_id", "company_id"],
                "name": "employments_pkey",
                "comment": None,
                "dialect_options": {"postgresql_include": []},
            }
        },
        "mobile_numbers": {
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
            ]
        },
        "tenures": {
            "one_only": {
                "constrained_columns": ["employee_id", "company_id"],
                "name": "tenures_pkey",
                "comment": None,
                "dialect_options": {"postgresql_include": []},
            }
        },
    }


@pytest.fixture
def compare_errors_foreign_keys():
    return {
        "employments": {
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
            ]
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
        },
        "skills": {
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
            ]
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
            ]
        },
    }


@pytest.fixture
def compare_errors_indexes():
    return {
        "companies": {
            "one_only": [
                {
                    "name": "companies_name_key",
                    "unique": True,
                    "column_names": ["name"],
                    "duplicates_constraint": "companies_name_key",
                    "include_columns": [],
                    "dialect_options": {"postgresql_include": []},
                }
            ]
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
                    "duplicates_constraint": "employees_name_key",
                    "include_columns": [],
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
                    "duplicates_constraint": "unique_employee_name_age",
                    "include_columns": [],
                    "dialect_options": {"postgresql_include": []},
                },
            ],
        },
        "roles": {
            "two_only": [
                {
                    "name": "ix_roles_name",
                    "unique": False,
                    "column_names": ["name"],
                    "include_columns": [],
                    "dialect_options": {"postgresql_include": []},
                }
            ]
        },
        "skills": {
            "two_only": [
                {
                    "name": "skills_description_key",
                    "unique": True,
                    "column_names": ["description"],
                    "duplicates_constraint": "skills_description_key",
                    "include_columns": [],
                    "dialect_options": {"postgresql_include": []},
                }
            ]
        },
    }


@pytest.fixture
def compare_errors_unique_constraints():
    return {
        "companies": {
            "one_only": [
                {
                    "column_names": ["name"],
                    "name": "companies_name_key",
                    "comment": None,
                    "dialect_options": {
                        "postgresql_include": [],
                        "postgresql_nulls_not_distinct": False,
                    },
                }
            ]
        },
        "employees": {
            "two_only": [
                {
                    "column_names": ["name"],
                    "name": "employees_name_key",
                    "comment": None,
                    "dialect_options": {
                        "postgresql_include": [],
                        "postgresql_nulls_not_distinct": False,
                    },
                },
                {
                    "column_names": ["name", "age"],
                    "name": "unique_employee_name_age",
                    "comment": None,
                    "dialect_options": {
                        "postgresql_include": [],
                        "postgresql_nulls_not_distinct": False,
                    },
                },
            ]
        },
        "skills": {
            "two_only": [
                {
                    "column_names": ["description"],
                    "name": "skills_description_key",
                    "comment": None,
                    "dialect_options": {
                        "postgresql_include": [],
                        "postgresql_nulls_not_distinct": False,
                    },
                }
            ]
        },
    }


@pytest.fixture
def compare_errors_check_constraints():
    return {
        "employees": {
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
            ]
        },
        "employments": {
            "two_only": [
                {
                    "name": "check_end_date_after_start_date",
                    "sqltext": "end_date > start_date",
                    "comment": None,
                }
            ]
        },
    }


@pytest.fixture
def compare_errors_enums():
    return {
        "two_only": [
            {
                "name": "company_type",
                "schema": "public",
                "visible": True,
                "labels": ["Public", "Private", "Sole Trader"],
            }
        ],
        "diff": [
            {
                "one": {
                    "name": "title",
                    "schema": "public",
                    "visible": True,
                    "labels": ["ENGINEER", "MANAGER", "DIRECTOR", "CEO"],
                },
                "two": {
                    "name": "title",
                    "schema": "public",
                    "visible": True,
                    "labels": ["ENGINEER", "DIRECTOR", "CEO", "VP"],
                },
            }
        ],
    }


@pytest.fixture
def compare_errors_v14(
    compare_errors_tables_factory,
    compare_errors_columns,
    compare_errors_primary_keys,
    compare_errors_foreign_keys,
    compare_errors_indexes,
    compare_errors_unique_constraints,
    compare_errors_check_constraints,
    compare_errors_enums,
):
    return {
        "tables": compare_errors_tables_factory(),
        "columns": compare_errors_columns,
        "primary_keys": compare_errors_primary_keys,
        "foreign_keys": compare_errors_foreign_keys,
        "indexes": compare_errors_indexes,
        "unique_constraints": compare_errors_unique_constraints,
        "check_constraints": compare_errors_check_constraints,
        "enums": compare_errors_enums,
    }


@pytest.fixture
def compare_errors(
    compare_errors_tables_factory,
    compare_errors_columns,
    compare_errors_primary_keys,
    compare_errors_foreign_keys,
    compare_errors_indexes,
    compare_errors_unique_constraints,
    compare_errors_check_constraints,
    compare_errors_enums,
):
    return {
        "tables": compare_errors_tables_factory(),
        "columns": compare_errors_columns,
        "primary_keys": compare_errors_primary_keys,
        "foreign_keys": compare_errors_foreign_keys,
        "indexes": compare_errors_indexes,
        "unique_constraints": compare_errors_unique_constraints,
        "check_constraints": compare_errors_check_constraints,
        "enums": compare_errors_enums,
    }


@pytest.fixture
def compare_errors_aliases(compare_errors_tables_factory):
    return {
        "tables": compare_errors_tables_factory("production", "staging"),
    }


@pytest.fixture
def compare_result_sqlite():
    return {
        "tables": {
            "one_only": [{"name": "tenures", "comment": ""}],
            "two_only": [{"name": "employments", "comment": ""}],
            "common": [
                {"name": "companies", "comment": ""},
                {"name": "employees", "comment": ""},
                {"name": "mobile_numbers", "comment": ""},
                {"name": "roles", "comment": ""},
                {"name": "skills", "comment": ""},
            ],
            "diff": [],
        },
        "columns": {
            "companies": {
                "one_only": [],
                "two_only": [
                    {
                        "name": "company_type",
                        "type": "VARCHAR(11)",
                        "nullable": True,
                        "default": None,
                        "primary_key": 0,
                    }
                ],
                "common": [
                    {
                        "name": "id",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "primary_key": 1,
                    }
                ],
                "diff": [
                    {
                        "one": {
                            "name": "name",
                            "type": "VARCHAR(200)",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
                        },
                        "two": {
                            "name": "name",
                            "type": "VARCHAR(200)",
                            "nullable": True,
                            "default": None,
                            "primary_key": 0,
                        },
                    }
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
                        "primary_key": 0,
                    },
                    {
                        "name": "department",
                        "type": "VARCHAR(11)",
                        "nullable": True,
                        "default": None,
                        "primary_key": 0,
                    },
                    {
                        "name": "id",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "primary_key": 1,
                    },
                    {
                        "name": "name",
                        "type": "VARCHAR(200)",
                        "nullable": True,
                        "default": None,
                        "primary_key": 0,
                    },
                    {
                        "name": "ssn",
                        "type": "VARCHAR(30)",
                        "nullable": False,
                        "default": None,
                        "primary_key": 0,
                    },
                    {
                        "name": "title",
                        "type": "VARCHAR(8)",
                        "nullable": True,
                        "default": None,
                        "primary_key": 0,
                    },
                ],
                "diff": [
                    {
                        "one": {
                            "name": "age",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
                        },
                        "two": {
                            "name": "age",
                            "type": "INTEGER",
                            "nullable": True,
                            "default": "CAST(21 as int)",
                            "primary_key": 0,
                        },
                    },
                    {
                        "one": {
                            "name": "number_of_pets",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
                        },
                        "two": {
                            "name": "number_of_pets",
                            "type": "BIGINT",
                            "nullable": True,
                            "default": None,
                            "primary_key": 0,
                        },
                    },
                    {
                        "one": {
                            "name": "role_id",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
                        },
                        "two": {
                            "name": "role_id",
                            "type": "VARCHAR(50)",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
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
                        "primary_key": 1,
                    },
                    {
                        "name": "company_id",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "primary_key": 2,
                    },
                    {
                        "name": "start_date",
                        "type": "DATETIME",
                        "nullable": False,
                        "default": None,
                        "primary_key": 0,
                    },
                    {
                        "name": "end_date",
                        "type": "DATETIME",
                        "nullable": True,
                        "default": None,
                        "primary_key": 0,
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
                            "default": None,
                            "primary_key": 1,
                        },
                        "two": {
                            "name": "id",
                            "type": "INTEGER",
                            "nullable": True,
                            "default": None,
                            "primary_key": 0,
                        },
                    },
                    {
                        "one": {
                            "name": "number",
                            "type": "VARCHAR(40)",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
                        },
                        "two": {
                            "name": "number",
                            "type": "VARCHAR(50)",
                            "nullable": False,
                            "default": None,
                            "primary_key": 1,
                        },
                    },
                    {
                        "one": {
                            "name": "owner",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
                        },
                        "two": {
                            "name": "owner",
                            "type": "INTEGER",
                            "nullable": True,
                            "default": None,
                            "primary_key": 0,
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
                        "primary_key": 0,
                    },
                    {
                        "name": "role_type",
                        "type": "VARCHAR(10)",
                        "nullable": True,
                        "default": None,
                        "primary_key": 0,
                    },
                ],
                "diff": [
                    {
                        "one": {
                            "name": "id",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "primary_key": 1,
                        },
                        "two": {
                            "name": "id",
                            "type": "VARCHAR(50)",
                            "nullable": False,
                            "default": None,
                            "primary_key": 1,
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
                        "primary_key": 0,
                    }
                ],
                "two_only": [
                    {
                        "name": "person",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "primary_key": 0,
                    }
                ],
                "common": [
                    {
                        "name": "slug",
                        "type": "VARCHAR(50)",
                        "nullable": False,
                        "default": None,
                        "primary_key": 1,
                    }
                ],
                "diff": [
                    {
                        "one": {
                            "name": "description",
                            "type": "VARCHAR(100)",
                            "nullable": True,
                            "default": None,
                            "primary_key": 0,
                        },
                        "two": {
                            "name": "description",
                            "type": "VARCHAR(100)",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
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
                        "primary_key": 1,
                    },
                    {
                        "name": "company_id",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "primary_key": 2,
                    },
                    {
                        "name": "start_date",
                        "type": "DATETIME",
                        "nullable": False,
                        "default": None,
                        "primary_key": 0,
                    },
                    {
                        "name": "end_date",
                        "type": "DATETIME",
                        "nullable": True,
                        "default": None,
                        "primary_key": 0,
                    },
                ],
                "two_only": [],
                "common": [],
                "diff": [],
            },
        },
        "primary_keys": {
            "companies": {
                "one_only": [],
                "two_only": [],
                "common": [{"constrained_columns": ["id"], "name": None}],
                "diff": [],
            },
            "employees": {
                "one_only": [],
                "two_only": [],
                "common": [{"constrained_columns": ["id"], "name": None}],
                "diff": [],
            },
            "employments": {
                "one_only": [],
                "two_only": {
                    "constrained_columns": ["employee_id", "company_id"],
                    "name": None,
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
                        "one": {"constrained_columns": ["id"], "name": None},
                        "two": {"constrained_columns": ["number"], "name": None},
                    }
                ],
            },
            "roles": {
                "one_only": [],
                "two_only": [],
                "common": [{"constrained_columns": ["id"], "name": None}],
                "diff": [],
            },
            "skills": {
                "one_only": [],
                "two_only": [],
                "common": [{"constrained_columns": ["slug"], "name": None}],
                "diff": [],
            },
            "tenures": {
                "one_only": {
                    "constrained_columns": ["employee_id", "company_id"],
                    "name": None,
                },
                "two_only": [],
                "common": [],
                "diff": [],
            },
        },
        "foreign_keys": {
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
                    },
                    {
                        "name": "fk_employees_roles",
                        "constrained_columns": ["role_id"],
                        "referred_schema": None,
                        "referred_table": "roles",
                        "referred_columns": ["id"],
                        "options": {},
                    },
                ],
                "diff": [],
            },
            "employments": {
                "one_only": [],
                "two_only": [
                    {
                        "name": "fk_employments_employees",
                        "constrained_columns": ["employee_id"],
                        "referred_schema": None,
                        "referred_table": "employees",
                        "referred_columns": ["id"],
                        "options": {},
                    },
                    {
                        "name": "fk_employments_companies",
                        "constrained_columns": ["company_id"],
                        "referred_schema": None,
                        "referred_table": "companies",
                        "referred_columns": ["id"],
                        "options": {},
                    },
                ],
                "common": [],
                "diff": [],
            },
            "mobile_numbers": {
                "one_only": [
                    {
                        "name": "_unnamed_fk_employees_owner",
                        "constrained_columns": ["owner"],
                        "referred_schema": None,
                        "referred_table": "employees",
                        "referred_columns": ["id"],
                        "options": {},
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
                        },
                        "two": {
                            "name": "fk_skills_employees",
                            "constrained_columns": ["person"],
                            "referred_schema": None,
                            "referred_table": "employees",
                            "referred_columns": ["id"],
                            "options": {},
                        },
                    }
                ],
            },
            "tenures": {
                "one_only": [
                    {
                        "name": "fk_tenures_employees",
                        "constrained_columns": ["employee_id"],
                        "referred_schema": None,
                        "referred_table": "employees",
                        "referred_columns": ["id"],
                        "options": {},
                    },
                    {
                        "name": "fk_tenures_companies",
                        "constrained_columns": ["company_id"],
                        "referred_schema": None,
                        "referred_table": "companies",
                        "referred_columns": ["id"],
                        "options": {},
                    },
                ],
                "two_only": [],
                "common": [],
                "diff": [],
            },
        },
        "indexes": {
            "companies": {"one_only": [], "two_only": [], "common": [], "diff": []},
            "employees": {
                "one_only": [
                    {
                        "name": "ix_employees_name",
                        "column_names": ["name"],
                        "unique": 1,
                        "dialect_options": {},
                    }
                ],
                "two_only": [
                    {
                        "name": "idx_title_department",
                        "column_names": ["title", "department"],
                        "unique": 0,
                        "dialect_options": {},
                    },
                    {
                        "name": "ix_employees_ssn",
                        "column_names": ["ssn"],
                        "unique": 0,
                        "dialect_options": {},
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
                        "column_names": ["name"],
                        "unique": 0,
                        "dialect_options": {},
                    }
                ],
                "common": [],
                "diff": [],
            },
            "skills": {"one_only": [], "two_only": [], "common": [], "diff": []},
            "tenures": {"one_only": [], "two_only": [], "common": [], "diff": []},
        },
        "unique_constraints": {
            "companies": {
                "one_only": [{"name": "unique_companies_name", "column_names": ["name"]}],
                "two_only": [],
                "common": [],
                "diff": [],
            },
            "employees": {
                "one_only": [],
                "two_only": [
                    {
                        "name": "unique_employee_name_age",
                        "column_names": ["name", "age"],
                    },
                    {"name": "unique_employees_name", "column_names": ["name"]},
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
                        "name": "unique_skills_description",
                        "column_names": ["description"],
                    }
                ],
                "common": [],
                "diff": [],
            },
            "tenures": {"one_only": [], "two_only": [], "common": [], "diff": []},
        },
        "check_constraints": {
            "companies": {"one_only": [], "two_only": [], "common": [], "diff": []},
            "employees": {
                "one_only": [],
                "two_only": [],
                "common": [],
                "diff": [
                    {
                        "one": {
                            "sqltext": "age > 0 AND age <= 100",
                            "name": "check_age",
                        },
                        "two": {
                            "sqltext": "age > 0 AND age <= 90",
                            "name": "check_age",
                        },
                    }
                ],
            },
            "employments": {
                "one_only": [],
                "two_only": [
                    {
                        "sqltext": "end_date > start_date",
                        "name": "check_end_date_after_start_date",
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
                "common": [{"sqltext": "LENGTH(name) > 5", "name": "check_name"}],
                "diff": [],
            },
            "skills": {"one_only": [], "two_only": [], "common": [], "diff": []},
            "tenures": {"one_only": [], "two_only": [], "common": [], "diff": []},
        },
    }


@pytest.fixture
def compare_errors_sqlite():
    return {
        "tables": {
            "one_only": [{"name": "tenures", "comment": ""}],
            "two_only": [{"name": "employments", "comment": ""}],
        },
        "columns": {
            "companies": {
                "two_only": [
                    {
                        "name": "company_type",
                        "type": "VARCHAR(11)",
                        "nullable": True,
                        "default": None,
                        "primary_key": 0,
                    }
                ],
                "diff": [
                    {
                        "one": {
                            "name": "name",
                            "type": "VARCHAR(200)",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
                        },
                        "two": {
                            "name": "name",
                            "type": "VARCHAR(200)",
                            "nullable": True,
                            "default": None,
                            "primary_key": 0,
                        },
                    }
                ],
            },
            "employees": {
                "diff": [
                    {
                        "one": {
                            "name": "age",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
                        },
                        "two": {
                            "name": "age",
                            "type": "INTEGER",
                            "nullable": True,
                            "default": "CAST(21 as int)",
                            "primary_key": 0,
                        },
                    },
                    {
                        "one": {
                            "name": "number_of_pets",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
                        },
                        "two": {
                            "name": "number_of_pets",
                            "type": "BIGINT",
                            "nullable": True,
                            "default": None,
                            "primary_key": 0,
                        },
                    },
                    {
                        "one": {
                            "name": "role_id",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
                        },
                        "two": {
                            "name": "role_id",
                            "type": "VARCHAR(50)",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
                        },
                    },
                ]
            },
            "employments": {
                "two_only": [
                    {
                        "name": "employee_id",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "primary_key": 1,
                    },
                    {
                        "name": "company_id",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "primary_key": 2,
                    },
                    {
                        "name": "start_date",
                        "type": "DATETIME",
                        "nullable": False,
                        "default": None,
                        "primary_key": 0,
                    },
                    {
                        "name": "end_date",
                        "type": "DATETIME",
                        "nullable": True,
                        "default": None,
                        "primary_key": 0,
                    },
                ]
            },
            "mobile_numbers": {
                "diff": [
                    {
                        "one": {
                            "name": "id",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "primary_key": 1,
                        },
                        "two": {
                            "name": "id",
                            "type": "INTEGER",
                            "nullable": True,
                            "default": None,
                            "primary_key": 0,
                        },
                    },
                    {
                        "one": {
                            "name": "number",
                            "type": "VARCHAR(40)",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
                        },
                        "two": {
                            "name": "number",
                            "type": "VARCHAR(50)",
                            "nullable": False,
                            "default": None,
                            "primary_key": 1,
                        },
                    },
                    {
                        "one": {
                            "name": "owner",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
                        },
                        "two": {
                            "name": "owner",
                            "type": "INTEGER",
                            "nullable": True,
                            "default": None,
                            "primary_key": 0,
                        },
                    },
                ]
            },
            "roles": {
                "diff": [
                    {
                        "one": {
                            "name": "id",
                            "type": "INTEGER",
                            "nullable": False,
                            "default": None,
                            "primary_key": 1,
                        },
                        "two": {
                            "name": "id",
                            "type": "VARCHAR(50)",
                            "nullable": False,
                            "default": None,
                            "primary_key": 1,
                        },
                    }
                ]
            },
            "skills": {
                "one_only": [
                    {
                        "name": "employee",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "primary_key": 0,
                    }
                ],
                "two_only": [
                    {
                        "name": "person",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "primary_key": 0,
                    }
                ],
                "diff": [
                    {
                        "one": {
                            "name": "description",
                            "type": "VARCHAR(100)",
                            "nullable": True,
                            "default": None,
                            "primary_key": 0,
                        },
                        "two": {
                            "name": "description",
                            "type": "VARCHAR(100)",
                            "nullable": False,
                            "default": None,
                            "primary_key": 0,
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
                        "primary_key": 1,
                    },
                    {
                        "name": "company_id",
                        "type": "INTEGER",
                        "nullable": False,
                        "default": None,
                        "primary_key": 2,
                    },
                    {
                        "name": "start_date",
                        "type": "DATETIME",
                        "nullable": False,
                        "default": None,
                        "primary_key": 0,
                    },
                    {
                        "name": "end_date",
                        "type": "DATETIME",
                        "nullable": True,
                        "default": None,
                        "primary_key": 0,
                    },
                ]
            },
        },
        "primary_keys": {
            "employments": {
                "two_only": {
                    "constrained_columns": ["employee_id", "company_id"],
                    "name": None,
                }
            },
            "mobile_numbers": {
                "diff": [
                    {
                        "one": {"constrained_columns": ["id"], "name": None},
                        "two": {"constrained_columns": ["number"], "name": None},
                    }
                ]
            },
            "tenures": {
                "one_only": {
                    "constrained_columns": ["employee_id", "company_id"],
                    "name": None,
                }
            },
        },
        "foreign_keys": {
            "employments": {
                "two_only": [
                    {
                        "name": "fk_employments_employees",
                        "constrained_columns": ["employee_id"],
                        "referred_schema": None,
                        "referred_table": "employees",
                        "referred_columns": ["id"],
                        "options": {},
                    },
                    {
                        "name": "fk_employments_companies",
                        "constrained_columns": ["company_id"],
                        "referred_schema": None,
                        "referred_table": "companies",
                        "referred_columns": ["id"],
                        "options": {},
                    },
                ]
            },
            "mobile_numbers": {
                "one_only": [
                    {
                        "name": "_unnamed_fk_employees_owner",
                        "constrained_columns": ["owner"],
                        "referred_schema": None,
                        "referred_table": "employees",
                        "referred_columns": ["id"],
                        "options": {},
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
                    }
                ],
            },
            "skills": {
                "diff": [
                    {
                        "one": {
                            "name": "fk_skills_employees",
                            "constrained_columns": ["employee"],
                            "referred_schema": None,
                            "referred_table": "employees",
                            "referred_columns": ["id"],
                            "options": {},
                        },
                        "two": {
                            "name": "fk_skills_employees",
                            "constrained_columns": ["person"],
                            "referred_schema": None,
                            "referred_table": "employees",
                            "referred_columns": ["id"],
                            "options": {},
                        },
                    }
                ]
            },
            "tenures": {
                "one_only": [
                    {
                        "name": "fk_tenures_employees",
                        "constrained_columns": ["employee_id"],
                        "referred_schema": None,
                        "referred_table": "employees",
                        "referred_columns": ["id"],
                        "options": {},
                    },
                    {
                        "name": "fk_tenures_companies",
                        "constrained_columns": ["company_id"],
                        "referred_schema": None,
                        "referred_table": "companies",
                        "referred_columns": ["id"],
                        "options": {},
                    },
                ]
            },
        },
        "indexes": {
            "employees": {
                "one_only": [
                    {
                        "name": "ix_employees_name",
                        "column_names": ["name"],
                        "unique": 1,
                        "dialect_options": {},
                    }
                ],
                "two_only": [
                    {
                        "name": "idx_title_department",
                        "column_names": ["title", "department"],
                        "unique": 0,
                        "dialect_options": {},
                    },
                    {
                        "name": "ix_employees_ssn",
                        "column_names": ["ssn"],
                        "unique": 0,
                        "dialect_options": {},
                    },
                ],
            },
            "roles": {
                "two_only": [
                    {
                        "name": "ix_roles_name",
                        "column_names": ["name"],
                        "unique": 0,
                        "dialect_options": {},
                    }
                ]
            },
        },
        "unique_constraints": {
            "companies": {
                "one_only": [{"name": "unique_companies_name", "column_names": ["name"]}]
            },
            "employees": {
                "two_only": [
                    {
                        "name": "unique_employee_name_age",
                        "column_names": ["name", "age"],
                    },
                    {"name": "unique_employees_name", "column_names": ["name"]},
                ]
            },
            "skills": {
                "two_only": [
                    {
                        "name": "unique_skills_description",
                        "column_names": ["description"],
                    }
                ]
            },
        },
        "check_constraints": {
            "employees": {
                "diff": [
                    {
                        "one": {
                            "sqltext": "age > 0 AND age <= 100",
                            "name": "check_age",
                        },
                        "two": {
                            "sqltext": "age > 0 AND age <= 90",
                            "name": "check_age",
                        },
                    }
                ]
            },
            "employments": {
                "two_only": [
                    {
                        "sqltext": "end_date > start_date",
                        "name": "check_end_date_after_start_date",
                    }
                ]
            },
        },
    }
