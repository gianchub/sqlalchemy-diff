.PHONY: test

HTMLCOV_DIR ?= htmlcov

test: flake8 test_lib

flake8:
	flake8 sqlalchemydiff test

test_lib:
	coverage run --source=sqlalchemydiff -m pytest test $(ARGS)

coverage-html: test
	coverage html -d $(HTMLCOV_DIR)

coverage-report: test
	coverage report -m

coverage: coverage-html coverage-report test
