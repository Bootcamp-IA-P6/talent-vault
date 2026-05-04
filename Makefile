.PHONY: dev dev-no-gen gen-stop gen-start down build logs ps test lint clean status watch aggregate sync-sql pipeline mongo-shell psql mongo-ui prom-ui redis-shell fe-dev fe-build

# ---------- Stack lifecycle ----------

dev:          ## Start the whole stack in background (Kafka, Mongo, Postgres, app, datagen, Mongo Express)
	docker compose up -d

dev-no-gen:   ## Start the whole stack WITHOUT random_generator (no new data ingested)
	docker compose up -d --scale random_generator=0

gen-stop:     ## Stop the random_generator (everything else keeps running)
	docker compose stop random_generator

gen-start:    ## Start (or resume) the random_generator
	docker compose start random_generator

down:         ## Stop all containers (keeps data volumes)
	docker compose down

build:        ## Rebuild images and start
	docker compose up -d --build

clean:        ## Stop and DELETE all volumes (wipes Mongo + Postgres data)
	docker compose down -v

# ---------- Observability ----------

logs:         ## Tail logs from every service
	docker compose logs -f

ps:           ## Show status of all containers
	docker compose ps

status:       ## One-shot count of raw_messages, persons (Mongo) and persons (Postgres)
	@docker exec mongodb mongosh -u admin -p admin --authenticationDatabase admin --quiet --eval \
		'const db = db.getSiblingDB("talent_vault_raw"); print("[Mongo] raw_messages:", db.raw_messages.countDocuments({})); print("[Mongo] persons:     ", db.persons.countDocuments({}))'
	@docker exec postgres psql -U admin -d talent_vault -tAc "SELECT '[Postgres] persons:      ' || COUNT(*) FROM persons;" 2>/dev/null || echo "[Postgres] persons:      (table not created yet)"

watch:        ## Live-refresh the counts above every 2 seconds
	@watch -n 2 make status

# ---------- ETL steps (manual) ----------

aggregate:    ## Run the batch aggregator: raw_messages -> persons (Mongo)
	uv run python -m src.processing.transformer

sync-sql:     ## Run the SQL loader: persons (Mongo) -> persons (Postgres)
	uv run python -m src.processing.sql_loader

pipeline:     ## Aggregate + sync to SQL in one shot
	$(MAKE) aggregate
	$(MAKE) sync-sql

# ---------- Dev shells ----------

mongo-shell:  ## Open an interactive mongosh session connected to the running container
	docker exec -it mongodb mongosh -u admin -p admin --authenticationDatabase admin talent_vault_raw

psql:         ## Open an interactive psql session connected to the running container
	docker exec -it postgres psql -U admin -d talent_vault

mongo-ui:     ## Print the Mongo Express URL
	@echo "Open http://localhost:8081"

prom-ui:      ## Print the Prometheus URL
	@echo "Open http://localhost:9090  (try query: rate(talent_vault_kafka_messages_consumed_total[1m]))"

redis-shell:  ## Open an interactive redis-cli session inside the running container
	docker exec -it redis redis-cli

# ---------- Frontend (host dev server) ----------

fe-dev:       ## Run the Vite dev server on the host (HMR) against the API in Docker
	cd frontend && pnpm install && pnpm dev

fe-build:     ## Local production build of the frontend (sanity check)
	cd frontend && pnpm install && pnpm build

# ---------- QA ----------

test:         ## Run the pytest suite
	uv run pytest tests/ -v

lint:         ## Lint the codebase with ruff
	uv run ruff check src/ tests/

help:         ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
