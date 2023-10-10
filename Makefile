
install:
	poetry shell && \
	poetry install

run:
	poetry run uvicorn src.main:app --reload --port 8000

test:
	poetry run pytest

lint:
	poetry run ruff src
	poetry run black src

lint-watch:
	poetry run ruff src --watch

lint-fix:
	poetry run ruff src --fix

mypy:
	poetry run mypy src
