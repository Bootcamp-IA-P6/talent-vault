# Talent Vault

A real-time data engineering platform that consumes HR data from Apache Kafka, stores raw messages in MongoDB, processes and unifies employee records, and persists them into PostgreSQL for analysis.

## Tech Stack

- **Python 3.12** with **uv**
- **Apache Kafka** (consumer)
- **MongoDB** (raw data storage)
- **PostgreSQL** (processed data)
- **Redis** (cache layer)
- **FastAPI** (REST API)
- **React** (frontend)
- **Docker & Docker Compose**
- **Prometheus** (monitoring)

## Prerequisites

```bash
docker --version
```

```bash
docker compose version
```

```bash
uv --version
```

## Setup

Clone the repository:

```bash
git clone git@github.com:your-org/talent-vault.git
```

```bash
cd talent-vault
```

Copy the environment variables:

```bash
cp .env.example .env
```

Install Python dependencies:

```bash
uv sync
```

## Run

Start all services with Docker:

```bash
make dev
```

Stop all services:

```bash
make down
```

Rebuild containers:

```bash
make build
```

View logs:

```bash
make logs
```

## Run Tests

```bash
make test
```

## Project Structure

```
talent-vault/
├── src/
│   ├── consumer/       # Kafka consumer
│   ├── storage/        # MongoDB, PostgreSQL, Redis clients
│   ├── processing/     # Data transformation and grouping
│   ├── models/         # Data models (Mongo + SQL)
│   ├── api/            # FastAPI REST API
│   ├── monitoring/     # Prometheus metrics
│   └── utils/          # Logger, config
├── tests/              # Unit tests
├── frontend/           # React frontend
├── monitoring/         # Prometheus & Grafana config
├── docs/               # Documentation
├── docker-compose.yml
├── Dockerfile
├── Makefile
└── pyproject.toml
```

## Git Workflow

| Branch | Owner    |
|--------|----------|
| main   | Production |
| dev    | Integration |
| v1     | Mar      |
| v2     | Michelle |
| v3     | Rob      |

Each member works on their `vX` branch and opens a PR to `dev`.
