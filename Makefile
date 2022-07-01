export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

mypy:
	poetry run mypy *.py src/ tests/ --check-untyped-defs

pytest:
	poetry run pytest --tb=short

coverage:
	poetry run coverage run -m pytest --tb=short
	poetry run coverage report -m --omit="tests/*"

test: mypy coverage

install:
	pip install --upgrade pip
	pip install poetry
	poetry install

server:
	poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

worker:
	poetry run celery -A worker.celery worker

flower:
	poetry run celery -A worker.celery flower --port=5555

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

production: down build up

testing: down build
	docker-compose up -d
	docker-compose run --rm --no-deps --entrypoint="make test" api
