.PHONY: test

HTMLCOV_DIR ?= htmlcov

test: flake8 pylint pytest

pylint:
	pylint sqlalchemydiff -E

flake8:
	flake8 sqlalchemydiff test

pytest:
	coverage run --source=sqlalchemydiff --branch -m pytest test $(ARGS)
	coverage report --show-missing --fail-under=100
