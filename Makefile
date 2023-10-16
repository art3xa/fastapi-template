all: build down up

install:
	poetry shell && \
	poetry install

build:
	docker compose -p fastapi-template -f docker-compose-dev.yml build

up:
	docker compose -p fastapi-template -f docker-compose-dev.yml up

down:
	docker compose -p fastapi-template -f docker-compose-dev.yml down

run:
	poetry run uvicorn app.main:app --reload --port 8000

docker-test:
	docker compose -p fastapi-template -f docker-compose-dev.yml exec app poetry run pytest

docker-cov:
	docker compose -p fastapi-template -f docker-compose-dev.yml exec app poetry run pytest --cov

run-db:
	docker compose -p fastapi-template -f docker-compose-dev.yml up -d database

down-db:
	docker compose -p fastapi-template -f docker-compose-dev.yml down database

add-dev-migration:
	docker compose -p fastapi-template -f docker-compose-dev.yml exec app alembic revision --autogenerate && \
	docker compose -p fastapi-template -f docker-compose-dev.yml exec app alembic upgrade head && \
	echo "Migration added and applied."

test:
	poetry run pytest

cov:
	poetry run pytest --cov

lint:
	poetry run ruff app && \
	poetry run black app --check

lint-watch:
	poetry run ruff src --watch

lint-fix:
	poetry run ruff app --fix && \
	poetry run black app

mypy:
	poetry run mypy app
