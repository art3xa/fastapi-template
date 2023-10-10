
install:
	poetry shell && \
	poetry install

run:
	poetry run uvicorn main:app --reload --app-dir src --port 8000

test:
	poetry run pytest src

lint:
	poetry run ruff src
	poetry run autoflake src -r --in-place --remove-all-unused-imports --remove-duplicate-keys
	poetry run black src
	poetry run isort src
	poetry run flake8 src
	poetry run mypy src
