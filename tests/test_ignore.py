import pytest

from sqlalchemydiff.inspection import register
from sqlalchemydiff.inspection.base import BaseInspector
from sqlalchemydiff.inspection.ignore import (
    EnumIgnoreSpec,
    IgnoreClauses,
    IgnoreSpecFactory,
    TableIgnoreSpec,
)


class TestFilterIgnorers:
    @pytest.fixture
    def inspector(self):
        class TestInspector(BaseInspector):
            key = "test_inspector_key"

            def inspect(self, *args, **kwargs) -> dict:
                return {}

            def diff(self, *args, **kwargs) -> dict:
                return {}

            def _is_supported(self, inspector) -> bool:
                return True

        yield TestInspector()
        register.pop("test_inspector_key")

    def test_base_inspector_filter_ignorers_empty(self, inspector):
        assert inspector._filter_ignorers([]) == IgnoreClauses(tables=[], enums=[], clauses=[])

    def test_base_inspector_filter_ignorers(self, inspector):
        ignore_specs = [
            TableIgnoreSpec("table", "test_inspector_key", "name"),
            TableIgnoreSpec("table", "BAD_INSPECTOR_KEY", "name"),
            TableIgnoreSpec("table_name2"),
            EnumIgnoreSpec("name"),
            "BAD_SPEC_TYPE",
        ]

        assert inspector._filter_ignorers(ignore_specs) == IgnoreClauses(
            tables=[
                "table_name2",
            ],
            enums=[
                "name",
            ],
            clauses=[
                TableIgnoreSpec("table", "test_inspector_key", "name"),
            ],
        )


def test_ignores_validator():
    ignores = [f"table.{key}.name" for key in register.keys()]

    ignores.extend(
        [
            "table_name1",
            "table_name2",
            "enums.name",
            "enums.another_name",
        ]
    )

    assert IgnoreSpecFactory.create_specs(register, ignores) == [
        TableIgnoreSpec("table", "tables", "name"),
        TableIgnoreSpec("table", "columns", "name"),
        TableIgnoreSpec("table", "primary_keys", "name"),
        TableIgnoreSpec("table", "foreign_keys", "name"),
        TableIgnoreSpec("table", "indexes", "name"),
        TableIgnoreSpec("table", "unique_constraints", "name"),
        TableIgnoreSpec("table", "check_constraints", "name"),
        TableIgnoreSpec("table", "enums", "name"),
        TableIgnoreSpec("table_name1"),
        TableIgnoreSpec("table_name2"),
        EnumIgnoreSpec("name"),
        EnumIgnoreSpec("another_name"),
    ]


def test_ignores_validator_valid_empty_ignore():
    assert IgnoreSpecFactory.create_specs(register) == []


def test_ignores_validator_valid_empty_ignores_list():
    assert IgnoreSpecFactory.create_specs(register, []) == []


def test_ignores_validator_invalid():
    with pytest.raises(ValueError) as e:
        IgnoreSpecFactory.create_specs(register, ["table.BAD_INSPECTOR.name"])
    assert str(e.value) == "Invalid ignore clause, no inspector found: 'table.BAD_INSPECTOR.name'"


def test_ignores_validator_invalid_format_not_an_enum():
    with pytest.raises(ValueError) as e:
        IgnoreSpecFactory.create_specs(register, ["table.name"])
    assert str(e.value) == "Invalid ignore clause format: 'table.name'"


def test_ignores_validator_invalid_format_too_many_parts():
    with pytest.raises(ValueError) as e:
        IgnoreSpecFactory.create_specs(register, ["has.too.many.parts"])
    assert str(e.value) == "Invalid ignore clause format: 'has.too.many.parts'"


def test_ignores_validator_invalid_format_empty_clause():
    with pytest.raises(ValueError) as e:
        IgnoreSpecFactory.create_specs(register, [""])
    assert str(e.value) == "Invalid ignore clause format: ''"
