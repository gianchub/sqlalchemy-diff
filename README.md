# SQLAlchemy Diff

A tool for comparing database schemas using SQLAlchemy.

## Requirements

- Python 3.10 or higher (supports 3.10, 3.11, 3.12, 3.13, 3.14)
- SQLAlchemy >= 1.4
- sqlalchemy-utils ~= 0.41.2

## Authors

- [Fabrizio Romano](https://github.com/gianchub)
- [Mark McArdle](https://github.com/mmcardle)

# Usage

## Quick Start

```python
from sqlalchemy import create_engine
from sqlalchemydiff.comparer import Comparer

# Create engines for the two databases you want to compare
engine_one = create_engine('postgresql://user:pass@host:port/db_one')
engine_two = create_engine('postgresql://user:pass@host:port/db_two')

# Create a comparer instance
comparer = Comparer(engine_one, engine_two)

# Compare the schemas
result = comparer.compare()

# Check if schemas match
if result.is_match:
    print("Schemas are identical!")
else:
    print("Schemas differ!")
    print("Differences:", result.errors)

# Optionally save results to files
result.dump_result('comparison_result.json')
result.dump_errors('comparison_errors.json')
```

You can also create a comparer directly from database URIs:

```python
from sqlalchemydiff.comparer import Comparer

# Create comparer from URIs
comparer = Comparer.from_params(
    'postgresql://user:pass@host:port/db_one',
    'postgresql://user:pass@host:port/db_two'
)

result = comparer.compare()
```

You can use meaningful aliases for the results:

```python
result = comparer.compare(one_alias='production', two_alias='staging')
```

The built-in inspectors includes: **tables**, **columns**, **primary keys**, **foreign keys**, **indexes**, **unique constraints**, **check constraints**, and **enums**.

### To ignore specific inspectors:

For example, ignore enums and check constraints inspectors

```python
result = comparer.compare(ignore_inspectors=['enums', 'check_constraints'])
```

## Custom Inspectors

You can create your own custom inspectors to compare specific aspects of your database schemas.

All inspectors that inherit from `BaseInspector` are automatically registered and used by the comparer.

### Creating a Custom Inspector

To create a custom inspector, subclass `BaseInspector` and implement the required abstract methods. You can inheirit DiffMixin for consistent comparison logic and formatting.

Here is an example of an `Inspector` class structure.

```python
from sqlalchemy.engine import Engine
from sqlalchemydiff.inspection.base import BaseInspector
from sqlalchemydiff.inspection.mixins import DiffMixin
from typing import Optional


class MyCustomInspector(BaseInspector, DiffMixin):
    # Unique identifier for this inspector
    key = "my_custom_feature"

    # Set to True if this inspector operates at database level (like tables, enums)
    # Set to False if it operates at table level (like columns, indexes)
    db_level = False

    def inspect(self, engine: Engine, ignore_specs: list[IgnoreSpecType] | None = None) -> dict:
        """
        Inspect the database and return structured data.

        For table-level inspectors, return a dict with table names as keys:
        {
            "table1": [{"name": "item1", ...}, {"name": "item2", ...}],
            "table2": [{"name": "item3", ...}],
        }

        For db-level inspectors, return a flat dict:
        {
            "table1": {"name": "item1", ...},
            "table2": {"name": "item2", ...},
        }
        """
        ignore_clauses = self._filter_ignorers(ignore_specs)
        inspector = self._get_inspector(engine)

        # Your inspection logic here
        # Use inspector.get_* methods to retrieve database metadata

        return {...}

    def diff(self, one: dict, two: dict) -> dict:
        """
        Compare data from two databases.

        For documentation refer to the DiffMixin in `src/sqlalchemydiff/inspection/mixins.py`
        """
        return self._listdiff(one, two)

    def _is_supported(self, inspector) -> bool:
        """
        Check if this inspector is supported for the current database dialect.

        Return True if the required methods exist on the inspector.
        """
        return hasattr(inspector, 'get_something')
```

### Important Notes

- The `key` attribute must be unique, non-empty and must not start or end with whitespace
- Use the `DiffMixin` helper methods (`_listdiff`, `_dictdiff`, `_itemsdiff`) for consistent comparison logic

### Example: A Custom Sequences Inspector

This is a working example of a inspector that compares sequences.

```python
from sqlalchemy.engine import Engine
from sqlalchemydiff.inspection.base import BaseInspector
from sqlalchemydiff.inspection.mixins import DiffMixin
from typing import Optional


class SequencesInspector(BaseInspector, DiffMixin):
    key = "sequences"
    db_level = True

    def inspect(self, engine: Engine, ignore_specs: list[IgnoreSpecType] | None = None) -> dict:
        ignore_clauses = self._filter_ignorers(ignore_specs)
        inspector = self._get_inspector(engine)

        sequences = {}
        for seq in inspector.get_sequence_names():
            if seq not in ignore_clauses.tables:
                sequences[seq] = {
                    "name": seq,
                    "start": getattr(inspector.get_sequence_info(seq), 'start', None),
                    "increment": getattr(inspector.get_sequence_info(seq), 'increment', None),
                }

        return sequences

    def diff(self, one: dict, two: dict) -> dict:
        return self._itemsdiff(list(one.values()), list(two.values()))

    def _is_supported(self, inspector) -> bool:
        return hasattr(inspector, 'get_sequence_names')
```

Once defined, your custom inspector will be automatically registered and used in comparisons.
