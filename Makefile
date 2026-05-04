.PHONY: dev down build logs test lint clean

dev:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up -d --build

logs:
	docker compose logs -f

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check src/ tests/

clean:
	docker compose down -v
