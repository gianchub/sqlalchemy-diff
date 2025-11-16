from typing import cast

from sqlalchemy.engine import Engine

from .base import BaseInspector
from .compat import Inspector
from .ignore import IgnoreSpecType
from .mixins import DiffMixin


class TablesInspector(BaseInspector, DiffMixin):
    """Inspect the tables of a database."""

    key = "tables"
    db_level = True

    def inspect(self, engine: Engine, ignore_specs: list[IgnoreSpecType] | None = None) -> dict:
        ignore_clauses = self._filter_ignorers(ignore_specs)
        inspector = self._get_inspector(engine)

        def get_comment(table_name: str) -> str | None:
            try:
                return inspector.get_table_comment(table_name)["text"]
            except NotImplementedError:
                return

        return {
            table_name: self._format_table(table_name, get_comment(table_name))
            for table_name in inspector.get_table_names()
            if table_name not in ignore_clauses.tables
        }

    def _format_table(self, table_name: str, comment: str | None = None) -> dict:
        return {
            "name": table_name,
            "comment": comment or "",
        }

    def diff(self, one: dict, two: dict) -> dict:
        return self._itemsdiff(list(one.values()), list(two.values()))

    def _is_supported(self, inspector: Inspector) -> bool:
        return hasattr(inspector, "get_table_names")


class ColumnsInspector(BaseInspector, DiffMixin):
    """Inspect the columns of a database."""

    key = "columns"

    def inspect(self, engine: Engine, ignore_specs: list[IgnoreSpecType] | None = None) -> dict:
        ignore_clauses = self._filter_ignorers(ignore_specs)

        inspector = self._get_inspector(engine)
        table_names = inspector.get_table_names()

        result = {}
        for table_name in table_names:
            if table_name in ignore_clauses.tables:
                continue

            result[table_name] = [
                column_item
                for column_item in inspector.get_columns(table_name)
                if not ignore_clauses.is_clause(table_name, self.key, column_item["name"])
            ]
            self._process_types(result[table_name], engine)

        return result

    def diff(self, one: dict, two: dict) -> dict:
        return self._listdiff(one, two)

    def _process_types(self, column_dict: dict, engine: Engine) -> None:
        """Process the SQLAlchemy Column Type ``type_``.

        Calls :meth:`sqlalchemy.sql.type_api.TypeEngine.compile` on
        ``type_`` to produce a string-compiled form of it.  "string-compiled"
        meaning as it would be used for a SQL clause.
        """
        for column in column_dict:
            column["type"] = column["type"].compile(dialect=engine.dialect)

    def _is_supported(self, inspector: Inspector) -> bool:
        return hasattr(inspector, "get_columns")


class PrimaryKeysInspector(BaseInspector, DiffMixin):
    """Inspect the primary keys of a database."""

    key = "primary_keys"

    def inspect(self, engine: Engine, ignore_specs: list[IgnoreSpecType] | None = None) -> dict:
        ignore_clauses = self._filter_ignorers(ignore_specs)

        inspector = self._get_inspector(engine)
        table_names = inspector.get_table_names()
        result = {}

        for table_name in table_names:
            if table_name in ignore_clauses.tables:
                continue
            inspection_result = inspector.get_pk_constraint(table_name)

            if not ignore_clauses.is_clause(table_name, self.key, inspection_result["name"]):
                result[table_name] = inspection_result
            else:
                result[table_name] = {}

        return result

    def diff(self, one: dict, two: dict) -> dict:
        return self._dictdiff(one, two)

    def _is_supported(self, inspector: Inspector) -> bool:
        return hasattr(inspector, "get_pk_constraint")


class ForeignKeysInspector(BaseInspector, DiffMixin):
    """Inspect the foreign keys of a database."""

    key = "foreign_keys"

    def inspect(self, engine: Engine, ignore_specs: list[IgnoreSpecType] | None = None) -> dict:
        ignore_clauses = self._filter_ignorers(ignore_specs)

        inspector = self._get_inspector(engine)
        table_names = inspector.get_table_names()
        result = {}
        for table_name in table_names:
            if table_name in ignore_clauses.tables:
                continue

            result[table_name] = [
                self._get_fk_identifier(fk)
                for fk in inspector.get_foreign_keys(table_name)
                if not ignore_clauses.is_clause(table_name, self.key, fk["name"])
            ]
        return result

    def diff(self, one: dict, two: dict) -> dict:
        return self._listdiff(one, two)

    def _is_supported(self, inspector: Inspector) -> bool:
        return hasattr(inspector, "get_foreign_keys")

    def _get_fk_identifier(self, fk: dict) -> dict:
        if not fk["name"]:
            fk["name"] = f"_unnamed_fk_{fk['referred_table']}_{'_'.join(fk['constrained_columns'])}"
        return fk


class IndexesInspector(BaseInspector, DiffMixin):
    """Inspect the indexes of a database."""

    key = "indexes"

    def inspect(self, engine: Engine, ignore_specs: list[IgnoreSpecType] | None = None) -> dict:
        ignore_clauses = self._filter_ignorers(ignore_specs)
        inspector = self._get_inspector(engine)
        table_names = inspector.get_table_names()
        result = {}
        for table_name in table_names:
            if table_name in ignore_clauses.tables:
                continue

            result[table_name] = [
                index
                for index in inspector.get_indexes(table_name)
                if not ignore_clauses.is_clause(table_name, self.key, index["name"])
            ]
        return result

    def diff(self, one: dict, two: dict) -> dict:
        return self._listdiff(one, two)

    def _is_supported(self, inspector: Inspector) -> bool:
        return hasattr(inspector, "get_indexes")


class UniqueConstraintsInspector(BaseInspector, DiffMixin):
    """Inspect the unique constraints of a database."""

    key = "unique_constraints"

    def inspect(self, engine: Engine, ignore_specs: list[IgnoreSpecType] | None = None) -> dict:
        ignore_clauses = self._filter_ignorers(ignore_specs)
        inspector = self._get_inspector(engine)
        table_names = inspector.get_table_names()
        result = {}
        for table_name in table_names:
            if table_name in ignore_clauses.tables:
                continue

            result[table_name] = [
                uc
                for uc in self._format_unique_constraint(inspector, table_name)
                if not ignore_clauses.is_clause(table_name, self.key, uc["name"])
            ]
        return result

    def diff(self, one: dict, two: dict) -> dict:
        return self._listdiff(one, two)

    def _format_unique_constraint(self, inspector: Inspector, table_name: str) -> list[dict]:
        result = inspector.get_unique_constraints(table_name)
        for constraint in result:
            name = constraint.get("name")
            if not name:
                name = f"unique_{table_name}_{'_'.join(constraint.get('column_names'))}"
            constraint["name"] = name
        return cast(list[dict], result)

    def _is_supported(self, inspector: Inspector) -> bool:
        return hasattr(inspector, "get_unique_constraints")


class CheckConstraintsInspector(BaseInspector, DiffMixin):
    """Inspect the check constraints of a database."""

    key = "check_constraints"

    def inspect(self, engine: Engine, ignore_specs: list[IgnoreSpecType] | None = None) -> dict:
        ignore_clauses = self._filter_ignorers(ignore_specs)
        inspector = self._get_inspector(engine)
        table_names = inspector.get_table_names()
        result = {}
        for table_name in table_names:
            if table_name in ignore_clauses.tables:
                continue

            result[table_name] = [
                cc
                for cc in inspector.get_check_constraints(table_name)
                if not ignore_clauses.is_clause(table_name, self.key, cc["name"])
            ]
        return result

    def diff(self, one: dict, two: dict) -> dict:
        return self._listdiff(one, two)

    def _is_supported(self, inspector: Inspector) -> bool:
        return hasattr(inspector, "get_check_constraints")


class EnumsInspector(BaseInspector, DiffMixin):
    """Inspect the enums of a database."""

    key = "enums"
    db_level = True

    def inspect(
        self, engine: Engine, ignore_specs: list[IgnoreSpecType] | None = None
    ) -> list[dict]:
        inspector = self._get_inspector(engine)

        ignore_clauses = self._filter_ignorers(ignore_specs)
        enums = getattr(inspector, "get_enums", lambda: [])() or []
        return [enum for enum in enums if enum["name"] not in ignore_clauses.enums]

    def diff(self, one: dict, two: dict) -> dict:
        return self._itemsdiff(one, two)

    def _is_supported(self, inspector: Inspector) -> bool:
        return hasattr(inspector, "get_enums")
