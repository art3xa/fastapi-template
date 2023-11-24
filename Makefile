CODE_FOLDERS := src/app src/db src/config
TEST_FOLDERS := src/tests

.PHONY: install update test lint security_checks format lint-watch migrate db_seed db_start build up down run-prod up-prod down-prod cov

all: build down up

install:
	poetry install

update:
	poetry lock

run:
	poetry run uvicorn src.app.main:app --reload --port 8000

test:
	poetry run pytest

cov:
	poetry run pytest --cov

format:
	poetry run ruff $(CODE_FOLDERS) $(TEST_FOLDERS)  --fix
	poetry run isort $(CODE_FOLDERS) $(TEST_FOLDERS)
	poetry run black $(CODE_FOLDERS) $(TEST_FOLDERS)
	poetry run flake8 $(CODE_FOLDERS) $(TEST_FOLDERS)
	poetry run pylint $(CODE_FOLDERS) $(TEST_FOLDERS)

lint:
	poetry run ruff $(CODE_FOLDERS) $(TEST_FOLDERS)
	poetry run isort --check --diff $(CODE_FOLDERS) $(TEST_FOLDERS)
	poetry run black --check $(CODE_FOLDERS) $(TEST_FOLDERS)
	poetry run flake8 $(CODE_FOLDERS) $(TEST_FOLDERS)
	poetry run pylint $(CODE_FOLDERS) $(TEST_FOLDERS)
	# poetry run mypy src

lint-watch:
	poetry run ruff $(CODE_FOLDERS) $(TEST_FOLDERS) --watch

migrate:
	alembic upgrade head

db_seed:
	python -m seed

db_start: migrate db_seed

build:
	docker compose build

up:
	docker compose up tests

down:
	docker compose down tests

run-tests:
	docker compose run --rm tests poetry run pytest

run-cov:
	docker compose run --rm tests poetry run pytest --cov

up-db:
	docker compose up -d database

down-db:
	docker compose down database

run-prod: build-prod down-prod up-prod

build-prod:
	docker compose build server

up-prod:
	docker compose up server

down-prod:
	docker compose down server

security_checks:
	bandit -r $(CODE_FOLDERS)

run-autotests: build-autotests up-autotests

build-autotests:
	docker compose build autotests

up-autotests:
	docker compose up autotests

add-dev-migration:
	docker compose exec app alembic revision --autogenerate && \
	docker compose exec app alembic upgrade head && \
	echo "Migration added and applied."
