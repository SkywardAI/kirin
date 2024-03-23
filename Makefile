.PHONY: env
env:
	@cp .env.example .env

.PHONY: build
build: env
	docker-compose build

.PHONY: up
up: env build
	docker-compose up -d