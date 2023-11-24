# FastAPI-Template

[FastAPI Template](https://github.com/art3xa/fastapi-template) with JWT Authentication

## Usage

### Preparation

- Install packages with [Poetry](https://github.com/python-poetry/poetry)
```bash
make install
```
- Create ```.env``` file with the content from ```.env.example```
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
