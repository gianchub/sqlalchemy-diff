import abc
import inspect as stdlib_inspect

from sqlalchemy import inspect
from sqlalchemy.engine import Engine

from .compat import Inspector
from .exceptions import InspectorNotSupported
from .ignore import EnumIgnoreSpec, IgnoreClauses, IgnoreSpecType, TableIgnoreSpec


class BaseInspectorMeta(abc.ABCMeta):
    """Metaclass for all inspectors.

    This class registers all concrete classes derived from BaseInspector into the register
    dictionary. This way, if the user of this library wants to add an inspector, they can
    simply write their own inspector class (as a subclass of BaseInspector), and it will
    be automatically picked up by the comparer.
    """

    register = {}

    def __new__(mcs, name: str, bases: tuple, attrs: dict) -> type:
        cls = super().__new__(mcs, name, bases, attrs)

        if stdlib_inspect.isabstract(cls):
            return cls

        if not cls.key.strip():
            raise ValueError("Key must be set")

        if cls.key.strip() != cls.key:
            raise ValueError("Key must not start or end with whitespace")

        mcs.register[cls.key] = (name, cls)
        return cls


# Register of all inspectors
register = BaseInspectorMeta.register


class BaseInspector(abc.ABC, metaclass=BaseInspectorMeta):
    """Base class for all inspectors.

    To create your own inspector, you need to subclass this class and implement its
    abstract methods.
    """

    key: str = ""
    db_level = False

    def __init__(self, one_alias: str = "one", two_alias: str = "two"):
        self.one_alias = one_alias
        self.two_alias = two_alias
        self.one_only_alias = f"{one_alias}_only"
        self.two_only_alias = f"{two_alias}_only"

    @abc.abstractmethod
    def inspect(
        self, engine: Engine, ignore_specs: list[IgnoreSpecType] | None = None
    ) -> dict: ...  # pragma: no cover

    @abc.abstractmethod
    def diff(self, one: dict, two: dict) -> dict: ...  # pragma: no cover

    @abc.abstractmethod
    def _is_supported(self, inspector: Inspector) -> bool: ...  # pragma: no cover

    def _filter_ignorers(self, specs: list[IgnoreSpecType] | None) -> IgnoreClauses:
        tables, enums, clauses = [], [], []

        for spec in specs or []:
            if isinstance(spec, TableIgnoreSpec):
                if spec.inspector_key is None and spec.object_name is None:
                    tables.append(spec.table_name)
                elif spec.inspector_key == self.key:
                    clauses.append(spec)
            elif isinstance(spec, EnumIgnoreSpec):
                enums.append(spec.name)

        return IgnoreClauses(tables, enums, clauses)

    def _get_inspector(self, engine: Engine) -> Inspector:
        inspector = inspect(engine)
        if not self._is_supported(inspector):
            raise InspectorNotSupported(f"{self.key} are not supported on this database")
        return inspector
