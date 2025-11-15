from dataclasses import dataclass, field
from typing import NamedTuple


class TableIgnoreSpec(NamedTuple):
    table_name: str
    inspector_key: str | None = None
    object_name: str | None = None


class EnumIgnoreSpec(NamedTuple):
    name: str


IgnoreSpecType = TableIgnoreSpec | EnumIgnoreSpec


class IgnoreSpecFactory:
    """Factory for creating ignore specs.

    The format of the ignores is:

    - "table.<inspector_key>.<object_name>" (for example: "table.columns.address")
    - "<table_name>" (for example: "employees")
    - "enums.<enum_name>" (for example: "enums.status")

    """

    separator = "."

    @classmethod
    def create_specs(cls, register: dict, ignores: list[str] | None = None) -> list[IgnoreSpecType]:
        if not ignores:
            return []

        inspector_clauses = []
        valid_inspectors = register.keys()
        enums_key = "enums"

        for ignore in ignores:
            parts = [part.strip() for part in ignore.split(cls.separator) if part.strip()]

            if len(parts) not in [1, 2, 3] or (len(parts) == 2 and parts[0] != enums_key):
                raise ValueError(f"Invalid ignore clause format: '{ignore}'")

            if len(parts) == 3 and parts[1] not in valid_inspectors:
                raise ValueError(f"Invalid ignore clause, no inspector found: '{ignore}'")

            if len(parts) == 1:
                inspector_clauses.append(TableIgnoreSpec(parts[0]))
            elif len(parts) == 2:
                inspector_clauses.append(EnumIgnoreSpec(parts[1]))
            else:
                inspector_clauses.append(TableIgnoreSpec(*parts))

        return inspector_clauses


@dataclass
class IgnoreClauses:
    tables: list[str] = field(default_factory=list)
    enums: list[str] = field(default_factory=list)
    clauses: list[IgnoreSpecType] = field(default_factory=list)

    def is_clause(self, table_name: str, inspector_key: str, object_name: str | None) -> bool:
        clause = TableIgnoreSpec(table_name, inspector_key, object_name)
        return clause in self.clauses
