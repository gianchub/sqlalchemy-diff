import pytest

from sqlalchemydiff.inspection.base import BaseInspector
from sqlalchemydiff.inspection.mixins import DiffMixin
from tests.base import BaseTest


class TestBadInspector(BaseTest):
    def test_bad_inspector_key_empty(self):
        with pytest.raises(ValueError) as exc_info:

            class BadInspector(BaseInspector, DiffMixin):
                def inspect(self, *args, **kwargs) -> list[dict]:
                    return []

                def diff(self, one: dict, two: dict) -> dict:
                    return {}

                def _is_supported(self, inspector) -> bool:
                    return True

        assert exc_info.value.args[0] == "Key must be set"

    @pytest.mark.parametrize("inspector_key", ["  key", "key  ", "  key  "])
    def test_bad_inspector_key_whitespace(self, inspector_key):
        with pytest.raises(ValueError) as exc_info:

            class BadInspector(BaseInspector, DiffMixin):
                key = inspector_key

                def inspect(self, *args, **kwargs) -> list[dict]:
                    return []

                def diff(self, one: dict, two: dict) -> dict:
                    return {}

                def _is_supported(self, inspector) -> bool:
                    return True

        assert exc_info.value.args[0] == "Key must not start or end with whitespace"
