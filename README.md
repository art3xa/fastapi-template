# FastAPI-Template

[![Deploy application](https://github.com/art3xa/fastapi-template/actions/workflows/deploy.yml/badge.svg)](https://github.com/art3xa/fastapi-template/actions/workflows/deploy.yml)
[![Static Checks](https://github.com/art3xa/fastapi-template/actions/workflows/ci.yml/badge.svg)](https://github.com/art3xa/fastapi-template/actions/workflows/ci.yml)
[![](https://tokei.rs/b1/github/art3xa/fastapi-template)](https://github.com/art3xa/fastapi-template)
[![Hits-of-Code](https://hitsofcode.com/github/art3xa/fastapi-template?branch=main)](https://hitsofcode.com/github/art3xa/fastapi-template/view?branch=main)
[![Maintainability](https://api.codeclimate.com/v1/badges/4b56ef8c3d1f1beeea22/maintainability)](https://codeclimate.com/github/art3xa/fastapi-template/maintainability)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fart3xa%2Ffastapi-template&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

[FastAPI Template](https://github.com/art3xa/fastapi-template) with JWT Authentication

## Technologies used
- Python
- Poetry
- FastAPI
- SQLAlchemy v2
- Alembic
- Asyncpg
- PostgreSQL
- Pydantic v2
- Pytest
- Docker
- Docker Compose

## Swagger

![][swagger]

### You can check and open [openapi.json] in [swagger editor](https://editor.swagger.io/) or [redoc](https://redocly.github.io/redoc/)

## Usage

### Preparation

- Install packages with [Poetry](https://github.com/python-poetry/poetry)
```bash
make install
```
- Create ```.env``` file with the content from [.env.example]
```bash
cp .env.example .env
```
- Configure environment variables
### Run in [Docker](https://docs.docker.com/compose/)

- Build and run the docker container
```bash
make
```

### Run local
- Change `DATABASE_HOST` from `database` to `localhost` in ```.env``` file
- Startup PostgreSQL
```bash
make up-db
```
- Run migrations
```bash
make migrate
```
- Run ```make run``` to start app
```bash
make run
```

### Other Makefile commands
- Run tests
```bash
make test
```
- Run tests coverage
```bash
make cov
```
- Run linters
```bash
make lint
```
- Run formatters
```bash
make format
```

---

[.env.example]: .env.example ".env.example"

[swagger]: docs/images/swagger.png "swagger"

[openapi.json]: docs/openapi.json "openapi.json"
