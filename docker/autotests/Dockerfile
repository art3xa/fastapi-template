# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /opt/app

# Install Poetry
RUN pip install poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock README.md ./

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install

COPY ./src ./src

# Application entrypoint
CMD ["pytest", "--cov", "src/app/internal/homework/"]
