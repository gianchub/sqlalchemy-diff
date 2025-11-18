import json
import logging
from collections.abc import Iterable
from copy import deepcopy
from typing import Any

from sqlalchemy.engine import Engine

from .connection import DBConnectionFactory
from .inspection import IgnoreSpecFactory, register
from .inspection.base import BaseInspector
from .inspection.exceptions import InspectorNotSupported, UnknownInspector
from .inspection.ignore import IgnoreSpecType


logger = logging.getLogger(__name__)


class CompareResult:
    """
    Analyse the result of comparing two database schemas.

    If you wish to use meaningful aliases for the result, you can pass them to the constructor.

    :attribute result: The comparison result.
    :attribute errors: The errors of the comparison.
    """

    def __init__(self, result: dict, one_alias: str = "one", two_alias: str = "two"):
        self.result = result
        self._one_only_alias = f"{one_alias}_only"
        self._two_only_alias = f"{two_alias}_only"
        self.errors = self._compile_errors()

    def _prune_keys(self, data: dict) -> None:
        data.pop("common", None)
        for key in [self._one_only_alias, self._two_only_alias, "diff"]:
            if not data.get(key):
                data.pop(key)

    def _compile_errors(self) -> dict:
        errors = deepcopy(self.result)
        for inspector_key in self.result:
            inspector_cls = register[inspector_key][1]
            if inspector_cls.db_level:
                self._prune_keys(errors[inspector_key])
                if not errors[inspector_key]:
                    errors.pop(inspector_key)
            else:
                for table_name in self.result[inspector_key]:
                    self._prune_keys(errors[inspector_key][table_name])
                    if not errors[inspector_key][table_name]:
                        errors[inspector_key].pop(table_name)

        return errors

    @property
    def is_match(self):
        """Tell if comparison was a match."""
        return not any(self.errors.values())

    def dump_result(self, filename):
        """Dump `result` dict to a file."""
        return self._dump(self.result, filename)

    def dump_errors(self, filename):
        """Dump `errors` dict to a file."""
        return self._dump(self.errors, filename)

    def _dump(self, data_to_dump, filename):
        data = self._dump_data(data_to_dump)
        self._write_data_to_file(data, filename)

    def _dump_data(self, data):
        return json.dumps(data, indent=4, sort_keys=True)

    def _write_data_to_file(self, data, filename):
        with open(filename, "w") as stream:
            stream.write(data)


class Comparer:
    """
    Compare two database schemas.

    You can pass two engines to the constructor, or use the `from_params` classmethod to create
    an engine from a URI and parameters.

    Simply call the `compare` method to get the result.

    You can customise how certain aspects of the comparison are performed by setting your own
    classes for the `ignore_spec_factory` and `compare_result_class` attributes.
    """

    ignore_spec_factory_class = IgnoreSpecFactory
    compare_result_class = CompareResult

    def __init__(self, db_one_engine: Engine, db_two_engine: Engine):
        self.db_one_engine = db_one_engine
        self.db_two_engine = db_two_engine

    @classmethod
    def from_params(
        cls,
        db_one_uri: str,
        db_two_uri: str,
        db_one_params: dict[str, Any] | None = None,
        db_two_params: dict[str, Any] | None = None,
    ):
        db_one_params = db_one_params or {}
        db_two_params = db_two_params or {}
        db_one_engine = DBConnectionFactory.create_engine(db_one_uri, **db_one_params)
        db_two_engine = DBConnectionFactory.create_engine(db_two_uri, **db_two_params)

        return cls(db_one_engine, db_two_engine)

    def compare(
        self,
        one_alias: str = "one",
        two_alias: str = "two",
        ignores: list[str] | None = None,
        ignore_inspectors: Iterable[str] | None = None,
    ):
        ignore_specs = self.ignore_spec_factory_class().create_specs(register, ignores)

        filtered_inspectors = self._filter_inspectors(set(ignore_inspectors or set()))

        result = {}
        with self.db_one_engine.begin(), self.db_two_engine.begin():
            for key, inspector_class in filtered_inspectors:
                inspector = inspector_class(one_alias=one_alias, two_alias=two_alias)

                db_one_info = self._get_db_info(ignore_specs, inspector, self.db_one_engine)
                db_two_info = self._get_db_info(ignore_specs, inspector, self.db_two_engine)

                if db_one_info is not None and db_two_info is not None:
                    result[key] = inspector.diff(db_one_info, db_two_info)

        return self.compare_result_class(result, one_alias=one_alias, two_alias=two_alias)

    def _filter_inspectors(
        self, ignore_inspectors: set[str] | None
    ) -> list[tuple[str, type[BaseInspector]]]:
        if not ignore_inspectors:
            ignore_inspectors = set()

        if not ignore_inspectors < register.keys():
            unknown_inspectors = set(ignore_inspectors) - register.keys()
            raise UnknownInspector(f"Unknown inspector: {', '.join(sorted(unknown_inspectors))}")

        return [(key, cls) for key, (_, cls) in register.items() if key not in ignore_inspectors]

    def _get_db_info(
        self, ignore_specs: list[IgnoreSpecType], inspector: BaseInspector, engine: Engine
    ) -> dict | None:
        try:
            return inspector.inspect(engine, ignore_specs)
        except InspectorNotSupported as e:
            logger.warning({"engine": engine, "inspector": inspector.key, "error": e.message})
