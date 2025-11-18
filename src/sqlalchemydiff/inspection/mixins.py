from collections.abc import Iterable, Mapping


class DiffMixin:
    """Mixin for diffing two databases.

    Provides methods used by the inspectors to diff the results.
    """

    one_alias: str
    two_alias: str
    one_only_alias: str
    two_only_alias: str

    def _get_empty_result(self) -> dict:
        return {
            self.one_only_alias: [],
            self.two_only_alias: [],
            "common": [],
            "diff": [],
        }

    def _listdiff(self, one: Mapping[str, Iterable], two: Mapping[str, Iterable]) -> dict:
        """Diff two iterables of items in mapping format.

        `one` and `two` are dictionaries with table names as keys and lists of items as values.
        They will be different according to which inspector is being used, but their structure
        will always be consistent, like in the following example:

        one = {
            "companies": [],
            "employees": [
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
                    ...
                },
            ],
            "tenures": [
                {
                    "name": "fk_tenures_employees",
                    "constrained_columns": ["employee_id"],
                    "referred_schema": None,
                    "referred_table": "employees",
                    "referred_columns": ["id"],
                    "options": {},
                    "comment": None,
                },
                {
                    ...
                },
            ],
        }

        """
        result = {}

        all_tables = sorted(set(one.keys()) | set(two.keys()))

        for table_name in all_tables:
            items_in_one = one.get(table_name, [])
            items_in_two = two.get(table_name, [])

            result[table_name] = self._get_empty_result()

            # table only in db one
            if table_name in one and table_name not in two:
                result[table_name][self.one_only_alias] = items_in_one

            # table only in db two
            elif table_name in two and table_name not in one:
                result[table_name][self.two_only_alias] = items_in_two

            # table in both databases
            else:
                result[table_name] = self._itemsdiff(items_in_one, items_in_two)

        return result

    def _itemsdiff(self, items_in_one: Iterable[Mapping], items_in_two: Iterable[Mapping]) -> dict:
        """Diff iterables of items in mapping format.

        `items_in_one` and `items_in_two` are iterables of items in mapping format.
        They will be different according to which inspector is being used, but their structure
        will always be consistent, like in the following example:

        items_in_one = [
            {
                "name": "id",
                "type": "INTEGER",
                "nullable": False,
                "default": "nextval('companies_id_seq'::regclass)",
                "autoincrement": True,
                "comment": None,
            },
            {
                "name": "name",
                "type": "VARCHAR(200)",
                "nullable": False,
                "default": None,
                "autoincrement": False,
                "comment": None,
            },
        ]

        """
        result = self._get_empty_result()

        names_in_one = {item["name"]: item for item in items_in_one}
        names_in_two = {item["name"]: item for item in items_in_two}
        all_names = sorted(names_in_one | names_in_two)

        for name in all_names:
            if name in names_in_one and name not in names_in_two:
                result[self.one_only_alias].append(names_in_one[name])
            elif name in names_in_two and name not in names_in_one:
                result[self.two_only_alias].append(names_in_two[name])
            else:
                item_one = names_in_one[name]
                item_two = names_in_two[name]

                if item_one != item_two:
                    result["diff"].append(
                        {
                            self.one_alias: item_one,
                            self.two_alias: item_two,
                        }
                    )
                else:
                    result["common"].append(item_one)

        return result

    def _dictdiff(self, one: Mapping[str, Mapping], two: Mapping[str, Mapping]) -> dict:
        """Diff two iterables of items in mapping format.

        `one` and `two` are mappings with table names as keys and mappings as values.
        They will be different according to which inspector is being used, but their structure
        will always be consistent, like in the following example:

        one = {
            "companies": {
                "constrained_columns": ["id"],
                "name": "companies_pkey",
                "comment": None,
                "dialect_options": {"postgresql_include": []},
            },
            "employees": {
                "constrained_columns": ["id"],
                "name": "employees_pkey",
                "comment": None,
                "dialect_options": {"postgresql_include": []},
            },
            "roles": {
                ...
            },
            "mobile_numbers": {
                ...
            },
        }

        """
        result = {}

        all_tables = sorted(set(one.keys()) | set(two.keys()))

        for table_name in all_tables:
            item_one = one.get(table_name, {})
            item_two = two.get(table_name, {})

            result[table_name] = self._get_empty_result()

            # table only in db one
            if table_name in one and table_name not in two:
                result[table_name][self.one_only_alias] = item_one

            # table only in db two
            elif table_name in two and table_name not in one:
                result[table_name][self.two_only_alias] = item_two

            # table in both databases
            else:
                if item_one != item_two:
                    result[table_name]["diff"].append(
                        {
                            self.one_alias: item_one,
                            self.two_alias: item_two,
                        }
                    )
                else:
                    result[table_name]["common"].append(item_one)

        return result
