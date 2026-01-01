.PHONY: help build up down logs restart migrate createsuperuser test clean setup

help:
	@echo "Available commands:"
	@echo "  make setup      - Setup environment (copy .env.example)"
	@echo "  make build      - Build containers"
	@echo "  make up         - Start containers"
	@echo "  make down       - Stop containers"
	@echo "  make logs       - Show logs"
	@echo "  make restart    - Restart containers"
	@echo "  make migrate    - Run migrations"
	@echo "  make createsuperuser - Create superuser"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean up containers and volumes"

setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env file created from .env.example. Please edit it!"; \
	else \
		echo ".env file already exists."; \
	fi

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose restart

migrate:
	docker-compose exec django python manage.py migrate

createsuperuser:
	docker-compose exec django python manage.py createsuperuser

test:
	docker-compose exec django python manage.py test

clean:
	docker-compose down -v
	docker system prune -f