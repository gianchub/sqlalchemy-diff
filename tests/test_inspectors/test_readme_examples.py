import pytest
from sqlalchemy.engine import Engine

from sqlalchemydiff.comparer import Comparer
from sqlalchemydiff.inspection import register
from sqlalchemydiff.inspection.base import BaseInspector
from sqlalchemydiff.inspection.mixins import DiffMixin
from tests.base import BaseTest


class TestReadmeExamples(BaseTest):
    def create_custom_inspector(self):
        """
        Create a custom inspector for sequences and register it.

        This inspector is in a factory method so that it does not auto register
        with `BaseInspectorMeta`.
        """

        class SequencesInspector(BaseInspector, DiffMixin):
            key = "sequences"
            db_level = True

            def inspect(self, engine: Engine, ignore_specs: list | None = None) -> dict:
                ignore_clauses = self._filter_ignorers(ignore_specs)
                inspector = self._get_inspector(engine)

                sequences = {}
                for seq in inspector.get_sequence_names():
                    if seq not in ignore_clauses.tables:
                        sequences[seq] = {
                            "name": seq,
                            "start": getattr(inspector.get_sequence_names(seq), "start", None),
                            "increment": getattr(
                                inspector.get_sequence_names(seq), "increment", None
                            ),
                        }

                return sequences

            def diff(self, one: dict, two: dict) -> dict:
                return self._itemsdiff(list(one.values()), list(two.values()))

            def _is_supported(self, inspector) -> bool:
                return hasattr(inspector, "get_sequence_names")

    @pytest.fixture(autouse=True, scope="class")
    def setup_method(self):
        self.create_custom_inspector()
        register_copy = register.copy()
        register.clear()
        register["sequences"] = register_copy["sequences"]
        yield
        register.update(register_copy)
        register.pop("sequences")

    @pytest.mark.usefixtures("setup_db_one", "setup_db_two")
    def test_sequences_custom_inspector(self, db_engine_one, db_engine_two):
        comparer = Comparer(db_engine_one, db_engine_two)
        result = comparer.compare()
        assert result.result == {
            "sequences": {
                "common": [
                    {
                        "increment": None,
                        "name": "employees_id_seq",
                        "start": None,
                    },
                ],
                "diff": [],
                "one_only": [
                    {
                        "increment": None,
                        "name": "companies_id_seq",
                        "start": None,
                    },
                    {
                        "increment": None,
                        "name": "mobile_numbers_id_seq",
                        "start": None,
                    },
                    {
                        "increment": None,
                        "name": "roles_id_seq",
                        "start": None,
                    },
                ],
                "two_only": [],
            },
        }
        assert result.errors == {
            "sequences": {
                "one_only": [
                    {
                        "increment": None,
                        "name": "companies_id_seq",
                        "start": None,
                    },
                    {
                        "increment": None,
                        "name": "mobile_numbers_id_seq",
                        "start": None,
                    },
                    {
                        "increment": None,
                        "name": "roles_id_seq",
                        "start": None,
                    },
                ],
            },
        }
