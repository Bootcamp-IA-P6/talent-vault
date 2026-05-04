# Talent Vault

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Kafka](https://img.shields.io/badge/Apache_Kafka-7.5-black?logo=apachekafka)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green?logo=mongodb)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-red?logo=redis)
![FastAPI](https://img.shields.io/badge/FastAPI-0.1.0-teal?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)
![Prometheus](https://img.shields.io/badge/Prometheus-monitoring-orange?logo=prometheus)

A real-time data engineering platform that consumes HR data from Apache Kafka, stores raw messages in MongoDB, processes and unifies employee records, and persists them into PostgreSQL for analysis.

---

## Architecture

```
┌─────────────────┐     ┌───────────────┐     ┌─────────────┐
│  random_generator│────▶│  Apache Kafka │────▶│   Consumer  │
│  (Faker data)   │     │  topic:probando│     │  (Python)   │
└─────────────────┘     └───────────────┘     └──────┬──────┘
                                                      │
                                              ┌───────▼──────┐
                                              │    Redis      │
                                              │  (batch cache)│
                                              └───────┬──────┘
                                                      │ flush every 50 msgs
                                              ┌───────▼──────┐
                                              │   MongoDB     │
                                              │  5 collections│
                                              └───────┬──────┘
                                                      │
                                              ┌───────▼──────┐
                                              │  Transformer  │
                                              │ (auto every   │
                                              │  5 minutes)   │
                                              └───────┬──────┘
                                                      │
                                              ┌───────▼──────┐
                                              │  PostgreSQL   │
                                              │  persons table│
                                              └───────┬──────┘
                                                      │
                                              ┌───────▼──────┐
                                              │  FastAPI      │
                                              │  REST API     │
                                              └───────┬──────┘
                                                      │
                                              ┌───────▼──────┐
                                              │  Prometheus   │
                                              │  /metrics     │
                                              └──────────────┘
```

Each Kafka message contains one of five document types — `personal_data`, `location`, `professional_data`, `bank_data`, or `net_data` — which are first cached in Redis, then flushed to MongoDB in batches, and finally unified into a single `persons` record in PostgreSQL by the transformer. The transformer runs automatically every 5 minutes via a scheduler.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Ingestion | Apache Kafka + kafka-python-ng |
| Cache | Redis 7 |
| Raw storage | MongoDB 7 |
| Processed storage | PostgreSQL 16 |
| API | FastAPI + uvicorn |
| Frontend | React |
| Monitoring | Prometheus |
| Scheduling | schedule |
| Package manager | uv |
| Containerization | Docker + Docker Compose |

---

## Prerequisites

```bash
docker --version        # Docker 24+
docker compose version  # Compose v2+
uv --version            # uv 0.4+
```

---

## Setup

Clone the repository including the data source submodule:

```bash
git clone --recurse-submodules git@github.com:Bootcamp-IA-P6/talent-vault.git
cd talent-vault
```

Create the shared Docker network:

```bash
docker network create talent-network
```

Copy and fill in the environment variables:

```bash
cp .env.example .env
```

Install Python dependencies:

```bash
uv sync
```

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker address | `localhost:29092` |
| `KAFKA_TOPIC` | Topic to consume | `probando` |
| `KAFKA_GROUP_ID` | Consumer group ID | `data-engineering-consumer` |
| `KAFKA_AUTO_OFFSET_RESET` | Offset reset policy | `earliest` |
| `MONGO_HOST` | MongoDB host | `localhost` |
| `MONGO_PORT` | MongoDB port | `27017` |
| `MONGO_USER` | MongoDB username | — |
| `MONGO_PASSWORD` | MongoDB password | — |
| `MONGO_DB` | MongoDB database name | `datagen` |
| `POSTGRES_HOST` | PostgreSQL host | `localhost` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_USER` | PostgreSQL username | — |
| `POSTGRES_PASSWORD` | PostgreSQL password | — |
| `POSTGRES_DB` | PostgreSQL database name | — |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `REDIS_BATCH_SIZE` | Messages per type before flushing to MongoDB | `50` |
| `TRANSFORMER_INTERVAL_MINUTES` | How often the transformer runs automatically | `5` |
| `LOG_LEVEL` | Logging level | `INFO` |

---

## Run

Start the data source (Kafka + generator):

```bash
cd external/data-source
docker compose up -d
cd ../..
```

Start the main stack:

```bash
docker compose up -d
```

Stop all services:

```bash
docker compose down
```

Rebuild containers:

```bash
docker compose build
```

View logs:

```bash
docker logs talent-vault-app -f
```

Run the Kafka consumer manually:

```bash
python -m src.consumer.kafka_consumer
```

Run the transformer manually:

```bash
python -m src.processing.transformer
```

---

## API Endpoints

Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/metrics` | Prometheus metrics scraping endpoint |
| GET | `/persons/` | Paginated list of persons (`?limit=20&offset=0`) |
| GET | `/persons/search` | Search by name, city, company or job |
| GET | `/persons/stats` | Aggregated statistics |
| GET | `/persons/{passport}` | Full profile by passport number |

Interactive docs available at `http://localhost:8000/docs`.

---

## Monitoring

Prometheus scrapes metrics from the app every 15 seconds.

| URL | Description |
|---|---|
| `http://localhost:9090` | Prometheus UI |
| `http://localhost:9090/targets` | Scraping targets status |
| `http://localhost:8000/metrics` | Raw metrics endpoint |

Useful PromQL queries:

```promql
# Messages consumed per type
rate(kafka_messages_consumed_total[5m])

# Redis cache size per type
redis_cache_size

# Batches flushed to MongoDB
redis_batch_flushed_total

# Persons processed by transformer
transformer_persons_processed_total

# App memory usage
process_resident_memory_bytes
```

---

## Run Tests

```bash
uv run pytest tests/ -v
```

---

## Project Structure

```
talent-vault/
├── src/
│   ├── consumer/       # Kafka consumer with Redis batching
│   ├── storage/        # MongoDB, PostgreSQL and Redis clients
│   ├── processing/     # Data transformer (MongoDB → PostgreSQL)
│   ├── models/         # Data models
│   ├── api/            # FastAPI REST API
│   ├── monitoring/     # Prometheus metrics definitions
│   └── utils/          # Logger and config
├── tests/              # Unit tests
├── frontend/           # React frontend
├── monitoring/         # Prometheus & Grafana config
├── docs/               # Documentation
├── external/           # Kafka data source submodule
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── .env.example
```

---

## Git Workflow

| Branch | Purpose |
|---|---|
| `main` | Production — stable releases only |
| `dev` | Integration — all PRs merge here first |
| `v1` | Mar's feature branch |
| `v2` | Michelle's feature branch |
| `v3` | Rob's feature branch |

Each team member works on their `vX` branch and opens a Pull Request to `dev`. Once reviewed and tested, `dev` is merged into `main`.

---

## Team

Developed at Factoria F5 Madrid — IA Bootcamp P6.