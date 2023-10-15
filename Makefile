all: build down up

install:
	cd src && \
	poetry shell && \
	poetry install

build:
	docker compose -f docker-compose-dev.yml build

up:
	docker compose -f docker-compose-dev.yml up

down:
	docker compose -f docker-compose-dev.yml down

run:
	cd src && \
	poetry run uvicorn app.main:app --reload --port 8000

add-dev-migration:
	docker compose -f docker-compose-dev.yml exec app alembic revision --autogenerate && \
	docker compose -f docker-compose-dev.yml exec app alembic upgrade head && \
	echo "Migration added and applied."

test:
	cd src && \
	poetry run pytest

cov:
	cd src && \
	poetry run pytest --cov

lint:
	cd src && \
	poetry run ruff app && \
	poetry run black app --check

lint-watch:
	cd src
	poetry run ruff src --watch

lint-fix:
	cd src && \
	poetry run ruff app --fix && \
	poetry run black app

mypy:
	cd src && \
	poetry run mypy app
