# Changelog

## [1.1.2]

29/10/2026

- Add Python 3.15 support and extend the CI and tox test matrices through 3.15.
- Fix SQLAlchemy 1.4 tox inheritance and preserve test environment dependencies.
- Install SQLAlchemy 1.4 in its CI jobs and document how to run the test matrix.
- Select psycopg2 explicitly in tests for compatibility with SQLAlchemy 2.1.
- Correct SQLAlchemy 1.4 constraint expectations and two type annotations.
- Refresh `uv.lock` without changing the declared dependency ranges.

## [1.1.1]

12/12/2025

- Add `dispose_engines` flag to `Comparer` constructor.
- Add `dispose` method to `Comparer` class.
- Add tests for engine disposal.
- Update README.md with new information.

## [1.1.0]

10/12/2025

- Remove dependency on sqlalchemy-utils.
- Add our own database utility functions for test purposes.
- Add comprehensive test suite for database utility functions.


## [1.0.4]

18/11/2025

- Fix `CompareResult.is_match` property.
- Fix typo in `dictdiff` method.
- Remove redundant return statement.

## [1.0.3]

15/11/2025

- Improve project description.
- Remove support for Python 3.9.
- Update type hint syntax to be compatible with Python 3.10.
- Update pytest to 9.*.

## [1.0.2]

15/11/2025

- Fix issus with sqlalchemy-utils being pinned too strictly.
- Fix tox issues.
- Remove print statements from tests.
- Fix issues with type hints.

## [1.0.0]

- Version 1.0.0.
  - This version breaks compatibility with any previous versions of the library.
