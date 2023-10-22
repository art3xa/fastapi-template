# Use an official Python runtime as a parent image
FROM python:3.11-slim AS builder

# Set work directory
WORKDIR /opt/build

# Install Poetry
RUN pip install poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock README.md ./

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Start final image
FROM python:3.11-slim

WORKDIR /opt/app

# Copy only the relevant files from the builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY ./src/app ./src/app
COPY ./src/db ./src/db
COPY ./src/config ./src/config

# Application entrypoint
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
