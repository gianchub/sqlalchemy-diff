.PHONY: test

test: flake8 pylint pytest

pylint:
	pylint sqlalchemydiff -E --disable=E1102

flake8:
	flake8 sqlalchemydiff test

pytest:
	coverage run --source=sqlalchemydiff --branch -m pytest test $(ARGS)
	coverage report --show-missing --fail-under=100
