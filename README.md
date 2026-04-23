# Talent Vault

Real-time HR data pipeline for **HR Pro**. Consumes a continuous stream of employee fragments from Apache Kafka, persists the raw events in MongoDB, unifies each person's information across five source systems, and exposes the cleaned dataset in PostgreSQL for analytics.

## What it does

HR Pro receives data about each employee from 5 different systems as independent Kafka messages:

- **Personal** — `name`, `last_name`, `passport`, `email`, `telfnumber`, `sex`
- **Bank** — `passport`, `IBAN`, `salary`
- **Professional** — `fullname`, `company`, `job`, `company_email`, ...
- **Location** — `fullname`, `city`, `address`
- **Net** — `address`, `IPv4`

The platform joins these five fragments into a single unified person document, keyed by passport, and lands a fully normalized row in PostgreSQL for downstream analytics.

## Architecture

```
        ┌──────────────────┐
        │ random_generator │  emits JSON fragments to Kafka ("testing" topic)
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Apache Kafka     │  (topic: testing)
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ app (Python)     │  classifies each message by inspecting its keys
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────────────────────────────┐
        │ MongoDB (talent_vault_raw)               │
        │   ├─ raw_messages  (continuous)          │
        │   └─ persons       (aggregated)          │
        └────────────────┬─────────────────────────┘
                         │  batch aggregator (fuzzy join)
                         ▼
        ┌──────────────────────────────────────────┐
        │ PostgreSQL (talent_vault.persons)        │
        └──────────────────────────────────────────┘
```

### Matching strategy

- `bank` ↔ `personal` → exact join by `passport`
- `professional` and `location` ↔ `personal` → fuzzy join; a record matches when its `fullname` contains **both** the personal's `name` and `last_name` as substrings. This tolerates extra tokens such as middle names or honorifics (e.g. `"Lic. Hilda Alvarez Vergara"` matches `name="Hilda"` + `last_name="Alvarez"`).
- `net` ↔ `location` → exact join by `address`.

## Tech stack

| Area            | Tooling                                |
|-----------------|-----------------------------------------|
| Language        | Python 3.12, [uv](https://github.com/astral-sh/uv) |
| Messaging       | Apache Kafka 7.5, Zookeeper            |
| Document store  | MongoDB 7 + Mongo Express              |
| Relational DB   | PostgreSQL 16                          |
| ORM             | SQLAlchemy 2                           |
| Orchestration   | Docker + Docker Compose                |
| Testing         | pytest                                 |
| Logging         | loguru                                 |

## Prerequisites

- Docker Desktop running (`docker compose version`)
- `uv` (`uv --version`)
- A local MongoDB client (optional) — otherwise use Mongo Express at `http://localhost:8081`

## Quick start

```bash
cp .env.example .env
uv sync --extra dev
make dev
```

That brings up every service in the background. Open **http://localhost:8081** to inspect MongoDB visually.

### First-time data load

The consumer keeps writing raw messages to Mongo forever. To populate the unified `persons` collection and the Postgres table, run the ETL step manually (once there's some data):

```bash
make pipeline
```

## Commands

| Command             | What it does                                                              |
|---------------------|---------------------------------------------------------------------------|
| `make dev`          | Start the whole stack in the background                                   |
| `make down`         | Stop containers (data volumes are preserved)                              |
| `make build`        | Rebuild images and (re)start                                              |
| `make clean`        | Stop containers and **delete** Mongo and Postgres volumes                 |
| `make ps`           | List running services                                                     |
| `make logs`         | Tail the logs of every service                                            |
| `make status`       | One-shot counts of raw_messages, Mongo persons and Postgres persons       |
| `make watch`        | Live counts refreshed every 2 seconds                                     |
| `make aggregate`    | Batch: Mongo `raw_messages` → Mongo `persons`                             |
| `make sync-sql`     | Batch: Mongo `persons` → Postgres `persons`                               |
| `make pipeline`     | `aggregate` followed by `sync-sql`                                        |
| `make mongo-shell`  | Open an interactive `mongosh` session                                     |
| `make psql`         | Open an interactive `psql` session                                        |
| `make mongo-ui`     | Print the Mongo Express URL                                               |
| `make test`         | Run the pytest suite                                                      |
| `make lint`         | Lint with ruff                                                            |
| `make help`         | Print the full command list                                               |

## Viewing the data

### Live counts every 2 seconds

```bash
make watch
```

Output example:

```
[Mongo] raw_messages: 42130
[Mongo] persons:      3289
[Postgres] persons:   3289
```

`raw_messages` grows continuously. `persons` (both Mongo and Postgres) only grow after `make pipeline`.

### Mongo Express (web UI)

Open **http://localhost:8081** → database `talent_vault_raw` → collections `raw_messages` and `persons`.

### Interactive shells

```bash
make mongo-shell      # mongosh attached to talent_vault_raw
make psql             # psql attached to talent_vault
```

Useful Postgres queries:

```sql
SELECT COUNT(*) FROM persons;
SELECT fullname, company, city FROM persons WHERE city = 'Madrid' LIMIT 10;
SELECT company, COUNT(*) FROM persons GROUP BY company ORDER BY 2 DESC LIMIT 10;
```

### Tail the consumer in real time

```bash
docker compose logs -f app
```

### Structured log file (loguru)

The app also writes a rotating DEBUG-level log file to `logs/talent_vault.log` inside the `app` container (10 MB rotation, 7 days retention). To follow it:

```bash
docker exec -it app tail -f logs/talent_vault.log
```

## Running the pipeline end-to-end without Docker

If you want to develop against the services inside Docker but run the Python processes from your host (faster iteration), `.env` already points to `localhost` with the external ports:

```bash
make dev                                    # services up
uv run python -m src.consumer.kafka_consumer  # run the consumer on the host
uv run python -m src.processing.transformer   # or make aggregate
uv run python -m src.processing.sql_loader    # or make sync-sql
```

## Project structure

```
talent-vault/
├── datagen/                    # Kafka data generator (provided)
├── src/
│   ├── consumer/
│   │   └── kafka_consumer.py   # Classifier + Kafka → Mongo raw
│   ├── processing/
│   │   ├── transformer.py      # Aggregator: raw → persons (Mongo)
│   │   └── sql_loader.py       # Loader: persons (Mongo) → persons (Postgres)
│   ├── storage/
│   │   ├── mongo_client.py     # MongoDB connection + helpers
│   │   └── sql_client.py       # SQLAlchemy engine + schema
│   ├── models/
│   │   └── sql_models.py       # Person table (SQLAlchemy ORM)
│   ├── utils/
│   │   ├── config.py           # pydantic Settings (reads .env)
│   │   └── logger.py           # loguru configuration
│   └── main.py                 # Docker entrypoint (runs the consumer)
├── tests/
│   ├── test_classifier.py
│   └── test_aggregator.py
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml
└── .env.example
```

## Tests

```bash
make test
```

Currently 20 tests covering:

- **Classifier** — every payload shape routes to the correct message type, plus fallbacks.
- **Aggregator** — exact and fuzzy matchers, consumption semantics, full `build_person` join.

## Roadmap

| Level         | Feature                                           | Status |
|---------------|---------------------------------------------------|--------|
| 🟢 Essential   | Kafka consumer                                    | ✅      |
| 🟢 Essential   | Raw persistence in MongoDB                        | ✅      |
| 🟢 Essential   | Unified persons (aggregator)                      | ✅      |
| 🟢 Essential   | Persistence in PostgreSQL                         | ✅      |
| 🟡 Medium      | Structured logging                                | ✅      |
| 🟡 Medium      | Unit tests                                        | ✅      |
| 🟡 Medium      | Docker / Docker Compose                           | ✅      |
| 🟠 Advanced    | Redis as cache / buffer                           | ⬜      |
| 🟠 Advanced    | Prometheus metrics                                | ⬜      |
| 🟠 Advanced    | REST API (FastAPI)                                | ⬜      |
| 🔴 Expert      | Continuous pipeline (no manual ETL trigger)       | ⬜      |
| 🔴 Expert      | Frontend (Streamlit / Gradio)                     | ⬜      |

## Git workflow

| Branch | Owner       |
|--------|-------------|
| main   | Production  |
| dev    | Integration |
| v1     | Mar         |
| v2     | Michelle    |
| v3     | Rob         |

Each member works on their `vX` branch and opens a PR into `dev`.
