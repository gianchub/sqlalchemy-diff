.PHONY: ruff-fix ruff-check ruff-format ruff-format-check lint format test install-tox-uv test-sqlalchemy14
.PHONY: ty install-reqs docker-test-db-run build publish-test publish bump-version

# Misc

MODULE_NAME=src
TEST_MODULE_NAME=tests

# Database

DB_TEST_USER?=postgres
DB_TEST_PASSWORD?=postgres
DB_TEST_PORT?=5433
DB_TEST_HOST?=localhost
POSTGRES_CONTAINER_NAME?=postgres


# Linting and formatting

ruff-fix:
	uv run ruff check $(MODULE_NAME) $(TEST_MODULE_NAME) --fix

ruff-check:
	uv run ruff check $(MODULE_NAME) $(TEST_MODULE_NAME)

ruff-format:
	uv run ruff format $(MODULE_NAME) $(TEST_MODULE_NAME)

ruff-format-check:
	uv run ruff format --check $(MODULE_NAME) $(TEST_MODULE_NAME)

lint: ruff-check ruff-format-check

format: ruff-format ruff-fix


# type checking

ty:
	uv run ty check $(MODULE_NAME) $(TEST_MODULE_NAME)

# requirements

install-reqs:
	uv pip install -U -e ."[dev,lint,test]"

install-tox-uv:
	uv tool install tox --with tox-uv


# Tests
test: ARGS?=--cov
test:
	uv run pytest tests $(ARGS) -m 'not is_sqlalchemy_1_4' \
		--db-user=$(DB_TEST_USER) \
		--db-password=$(DB_TEST_PASSWORD) \
		--db-host=$(DB_TEST_HOST) \
		--db-port=$(DB_TEST_PORT)


test-sqlalchemy14:
	uv run pytest tests --no-cov $(ARGS) -m 'is_sqlalchemy_1_4' \
		--db-user=$(DB_TEST_USER) \
		--db-password=$(DB_TEST_PASSWORD) \
		--db-host=$(DB_TEST_HOST) \
		--db-port=$(DB_TEST_PORT)

# Docker
docker-test-db-run:
	docker start $(POSTGRES_CONTAINER_NAME)-test \
		|| docker run -d --name $(POSTGRES_CONTAINER_NAME)-test -p $(DB_TEST_PORT):5432 \
		-e POSTGRES_USER=$(DB_TEST_USER) \
		-e POSTGRES_PASSWORD=$(DB_TEST_PASSWORD) \
		-e POSTGRES_INITDB_ARGS="--encoding=UTF8 --lc-collate=en_US.utf8 --lc-ctype=en_US.utf8" \
		postgres:17.4

# Build and Publish

bump-version: ARGS?=patch
bump-version:
	uv version --bump $(ARGS)

build:
	rm -rf dist/
	uv build

publish-test: build
	uv publish --index testpypi ${ARGS}

publish: build
	uv publish ${ARGS}

# local, if exists
-include Makefile.local
