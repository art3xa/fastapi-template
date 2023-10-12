all: build down up

install:
	poetry shell && \
	poetry install

build:
	docker compose -f docker-compose-dev.yml build

up:
	docker compose -f docker-compose-dev.yml up

down:
	docker compose -f docker-compose-dev.yml down

run:
	poetry run uvicorn src.app.internal.main:app --reload --port 8000

add-dev-migration:
	docker compose -f docker-compose-dev.yml exec app alembic revision --autogenerate && \
	docker compose -f docker-compose-dev.yml exec app alembic upgrade head && \
	echo "Migration added and applied."

test:
	poetry run pytest

lint:
	poetry run ruff src
	poetry run black src --check

lint-watch:
	poetry run ruff src --watch

lint-fix:
	poetry run ruff src --fix
	poetry run black src

mypy:
	poetry run mypy src
