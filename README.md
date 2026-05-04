<div align="center">

<img src="frontend/src/assets/logo.png" alt="Talent Vault" width="200" />

# Talent Vault

**Real-time HR data pipeline for HR Pro**

Consumes a continuous stream of employee fragments from Apache Kafka, persists the raw events in MongoDB, unifies each person's information across five source systems, and exposes the cleaned dataset in PostgreSQL for analytics.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-7.5-231F20?logo=apachekafka&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-7-47A248?logo=mongodb&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-06B6D4?logo=tailwindcss&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

</div>

---

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

### Real-time path via Redis

Each fragment is also buffered in Redis with a 1-hour TTL. When a `personal` arrives, the consumer immediately tries to find its four siblings in Redis. If all five fragments are present:

- The fully assembled person is **upserted directly into PostgreSQL**, skipping Mongo `persons` and the periodic aggregator.
- The five buffered fragments are removed from Redis.

If any sibling is missing, nothing is consumed and the periodic Mongo aggregator (60-second window) eventually picks it up. Mongo `raw_messages` always retains the original fragment, so the batch path remains the safety net even if Redis is unavailable.

Redis key layout (namespace `tv:`):

| Pattern                          | Holds                                  | Why                       |
|----------------------------------|----------------------------------------|---------------------------|
| `tv:personal:{passport}`         | JSON of the personal payload           | exact lookup by passport  |
| `tv:bank:{passport}`             | JSON of the bank payload               | exact lookup by passport  |
| `tv:net:{address}`               | JSON of the net payload                | exact lookup by address   |
| `tv:professional:rec:{uuid}`     | JSON of one professional record        | individual storage        |
| `tv:professional:tok:{token}`    | SET of uuids — one entry per `fullname` token | fuzzy lookup index |
| `tv:location:rec:{uuid}`         | JSON of one location record            | individual storage        |
| `tv:location:tok:{token}`        | SET of uuids — one entry per `fullname` token | fuzzy lookup index |

The token-set strategy mirrors the in-memory `index_by_fullname_tokens` used by the batch transformer, so the same fuzzy-match constraint applies (a record matches when its `fullname` contains both `name` and `last_name`).

The `talent_vault_realtime_persons_assembled_total` Prometheus counter tracks how many persons skipped the batch path entirely.

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
| Cache / buffer  | Redis 7                                |
| Relational DB   | PostgreSQL 16                          |
| ORM             | SQLAlchemy 2                           |
| API             | FastAPI + Uvicorn                      |
| Frontend        | React 18 + Vite + Tailwind (served by nginx) |
| Monitoring      | Prometheus + prometheus-client         |
| Orchestration   | Docker + Docker Compose                |
| Testing         | pytest                                 |
| Logging         | loguru                                 |

## Prerequisites

- Docker Desktop running (`docker compose version`)
- `uv` (`uv --version`)
- A local MongoDB client (optional) — otherwise use Mongo Express at `http://localhost:8081`

## Quick start

### macOS / Linux

```bash
cp .env.example .env
uv sync --extra dev
make dev
```

That brings up every service in the background. Open **http://localhost:8501** for the frontend or **http://localhost:8081** to inspect MongoDB visually.

### Windows (PowerShell o CMD, sin instalar nada extra)

Windows no trae `make`, pero todos los targets son alias de `docker compose`. Con Docker Desktop instalado, los comandos equivalentes son:

```powershell
copy .env.example .env
docker compose up -d
```

Eso es todo: levanta el stack completo. Si quieres replicar `uv sync` para correr Python en local, instala uv siguiendo las instrucciones de https://docs.astral.sh/uv/, pero **no es necesario** para usar el sistema — todo corre dentro de Docker.

#### Paso a paso desde cero (Windows)

Pensado para alguien que clona el repo por primera vez en una máquina con Windows limpio.

**1. Instalar Docker Desktop** (única dependencia). Descarga de [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/), instala y abre la app. Espera a que el icono de la barra esté en verde. Verifica:

```powershell
docker --version
docker compose version
```

**2. Clonar el repositorio.** En PowerShell o Windows Terminal:

```powershell
cd $HOME\Documents
git clone https://github.com/iRuperth/talent-vault.git
cd talent-vault
```

> Si no tienes Git, descárgalo de [git-scm.com](https://git-scm.com/) o baja el zip desde GitHub y descomprímelo.

**3. Crear el archivo `.env`:**

```powershell
copy .env.example .env
```

**4. Levantar el stack.** La primera vez tarda 5-10 minutos descargando imágenes (~2 GB):

```powershell
docker compose up -d
```

**5. Verificar que todo está arriba:**

```powershell
docker compose ps
```

Tienen que aparecer los 11 servicios con `STATUS = Up`. Si alguno está `Exited`, mira sus logs:

```powershell
docker compose logs <nombre-servicio> --tail 50
```

**6. Abrir las URLs:**

| URL | Qué es |
|---|---|
| http://localhost:8501 | Frontend (CRM de Talent Vault) |
| http://localhost:8081 | Mongo Express (UI de MongoDB) |
| http://localhost:9090 | Prometheus (métricas) |
| http://localhost:8000/docs | API REST con Swagger |

El sistema ya está procesando datos en cuanto los servicios están `Up`.

**7. Parar y arrancar el generador (para inspeccionar con calma):**

```powershell
docker compose stop random_generator
docker compose start random_generator
```

**8. Apagar todo al terminar:**

```powershell
docker compose down       # preserva volúmenes (datos)
docker compose down -v    # borra volúmenes (empieza de cero la próxima vez)
```

#### Errores típicos en Windows

| Síntoma | Causa | Fix |
|---|---|---|
| `error during connect` al lanzar `docker compose` | Docker Desktop no está corriendo | Abre Docker Desktop y espera al icono verde |
| `port is already allocated` | Otro proceso usa el 5433, 8501, 8000... | `docker compose down`, identifica con `netstat -ano \| findstr :5433`, mata el proceso o cambia el puerto en `docker-compose.yml` |
| Las imágenes tardan eternamente en descargar | Internet lento o límite de Docker Hub | Paciencia. Desde una conexión rápida son ~2 GB |
| `docker compose ps` no muestra todos los servicios | Alguno crasheó al arrancar | `docker compose logs` para ver el error y reintentar `docker compose up -d` |

#### Resumen en 3 comandos (Windows)

Lo mínimo absoluto para arrancar:

```powershell
copy .env.example .env
docker compose up -d
start http://localhost:8501
```

#### Tabla de equivalencias `make` → `docker compose`

| Mac / Linux (`make`) | Windows (`docker compose`) | Qué hace |
|---|---|---|
| `make dev` | `docker compose up -d` | Levanta todo el stack (incluido el generador) |
| `make dev-no-gen` | `docker compose up -d --scale random_generator=0` | Levanta todo **sin** el generador |
| `make gen-start` | `docker compose start random_generator` | Arranca el generador (si ya existe) |
| `make gen-stop` | `docker compose stop random_generator` | Para el generador |
| `make down` | `docker compose down` | Para todo (preserva volúmenes) |
| `make build` | `docker compose up -d --build` | Reconstruye imágenes y arranca |
| `make clean` | `docker compose down -v` | Para todo y **borra** volúmenes |
| `make ps` | `docker compose ps` | Lista servicios corriendo |
| `make logs` | `docker compose logs -f` | Sigue logs de todos los servicios |
| `make mongo-shell` | `docker compose exec mongodb mongosh -u root -p example talent_vault_raw` | Abre shell de Mongo |
| `make psql` | `docker compose exec postgres psql -U postgres talent_vault` | Abre shell de Postgres |
| `make redis-shell` | `docker compose exec redis redis-cli` | Abre shell de Redis |
| `make test` | `docker compose run --rm app pytest` | Lanza la suite de tests |
| `make pipeline` | `docker compose exec app python -m src.processing.transformer` <br> `docker compose exec app python -m src.processing.sql_loader` | ETL completo de Mongo raw → Postgres |
| `make status` | `docker compose exec mongodb mongosh -u root -p example --quiet --eval "..."` | Foto puntual de los 3 contadores |
| `make watch` | (no hay equivalente directo — usa `make status` en bucle) | Contadores cada 2 s |

> **Tip:** en PowerShell puedes usar `--scale` igual que en bash. No hace falta `make`, `bash`, ni WSL.

### Controlling the data generator

The `random_generator` service produces fake employee fragments to Kafka **as fast as it can** ([datagen/kafka_push.py](datagen/kafka_push.py)) — there is no throttling. On a developer laptop it easily piles up tens of millions of raw messages in a few hours, which makes the UI hard to read (counts move every second) and the aggregator fall behind.

To make the system easy to inspect, you can start the stack without the generator and turn it on/off on demand:

```bash
make dev-no-gen
```

`docker compose up -d --scale random_generator=0` — boots Kafka, Zookeeper, MongoDB, PostgreSQL, the consumer (`app`), the API, the frontend and Mongo Express, but leaves the generator container off.

```bash
make gen-start
```

`docker compose start random_generator` — spins the generator back up. It will reconnect to Kafka and resume publishing fragments to the `testing` topic.

```bash
make gen-stop
```

`docker compose stop random_generator` — stops the generator only. Kafka keeps whatever is already in the topic; the consumer keeps draining it; the periodic pipeline keeps aggregating.

```bash
make dev
```

Equivalent to `docker compose up -d` — starts **everything**, generator included. Use this when you want a full live demo.

#### What is still running when the generator is stopped

Stopping the generator does **not** pause the rest of the pipeline. With `make dev-no-gen` (or after `make gen-stop`):

- **Kafka / Zookeeper** stay up and keep whatever messages are already buffered.
- **`app` (consumer)** keeps reading any pending Kafka messages and writing them to `raw_messages` in MongoDB. Once the topic is drained, `raw_messages` stops growing.
- **`app` (continuous pipeline)** keeps ticking every 10 seconds over a 60-second window ([src/main.py](src/main.py)). After ~60s without new raw messages it has nothing left to aggregate, so `persons` stops growing too.
- **MongoDB / PostgreSQL** keep all data; volumes are persistent.
- **API (`:8000`) and frontend (`:8501`)** keep serving the data already in PostgreSQL.

This is the right state for reading the UI calmly, running queries from `make psql`, or recording a demo without numbers flickering.

#### Catching up the historical backlog

The continuous loop only processes the last 60 seconds of raw messages. If you stopped the generator after a long run and want to drain everything that is still sitting unprocessed in MongoDB, run the full batch ETL:

```bash
make gen-stop          # make sure new fragments are not arriving
make pipeline          # full batch: aggregate ALL raw_messages -> Mongo persons -> Postgres
make status            # confirm the three counts are aligned
```

`make pipeline` runs `aggregate_batch()` ([src/processing/transformer.py](src/processing/transformer.py)) without a time window, so it processes the entire history. Depending on backlog size this can take from a few seconds to several minutes.

#### Typical workflows

**Quiet inspection** — open `http://localhost:8501` and explore.

```bash
make dev-no-gen
```

**Live demo** — watch counts grow.

```bash
make dev
make watch
```

**Calm down a noisy stack** — drain the backlog and verify counts are aligned.

```bash
make gen-stop
make pipeline
make status
```

**Resume ingestion** — no need to restart anything else.

```bash
make gen-start
```

### First-time data load

The consumer keeps writing raw messages to Mongo forever. To populate the unified `persons` collection and the Postgres table, run the ETL step manually (once there's some data):

```bash
make pipeline
```

## Commands

### Stack lifecycle

```bash
make dev
```
Start the whole stack in the background.

```bash
make dev-no-gen
```
Start the whole stack **without** `random_generator` (no new data).

```bash
make gen-stop
```
Stop the `random_generator` (everything else keeps running).

```bash
make gen-start
```
Start (or resume) the `random_generator`.

```bash
make down
```
Stop containers (data volumes are preserved).

```bash
make build
```
Rebuild images and (re)start.

```bash
make clean
```
Stop containers and **delete** Mongo and Postgres volumes.

```bash
make ps
```
List running services.

```bash
make logs
```
Tail the logs of every service.

### Inspection

```bash
make status
```
One-shot counts of `raw_messages`, Mongo `persons` and Postgres `persons`.

```bash
make watch
```
Live counts refreshed every 2 seconds.

### ETL

```bash
make aggregate
```
Batch: Mongo `raw_messages` → Mongo `persons`.

```bash
make sync-sql
```
Batch: Mongo `persons` → Postgres `persons`.

```bash
make pipeline
```
`aggregate` followed by `sync-sql`.

### Shells & UIs

```bash
make mongo-shell
```
Open an interactive `mongosh` session.

```bash
make psql
```
Open an interactive `psql` session.

```bash
make redis-shell
```
Open an interactive `redis-cli` session.

```bash
make mongo-ui
```
Print the Mongo Express URL.

```bash
make prom-ui
```
Print the Prometheus URL with a sample query.

### QA

```bash
make test
```
Run the pytest suite.

```bash
make lint
```
Lint with ruff.

```bash
make help
```
Print the full command list.

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

### Prometheus metrics

All Python processes expose Prometheus metrics. Open **http://localhost:9090** to query them.

| Endpoint scraped                | Source                | What it covers                                  |
|---------------------------------|-----------------------|-------------------------------------------------|
| `http://api:8000/metrics`       | FastAPI (`api`)       | API request count + latency, plus all pipeline metrics that ran in the same Python process |
| `http://app:9100/metrics`       | Pipeline (`app`)      | Kafka consumer counts, aggregator runs, Mongo→Postgres sync runs, pipeline tick duration |

Useful Prometheus queries:

```promql
# Throughput per second of consumed Kafka messages, by type
sum by (type) (rate(talent_vault_kafka_messages_consumed_total[1m]))

# How many persons the windowed aggregator inserted in the last minute
increase(talent_vault_aggregate_persons_inserted_total[1m])

# 95th percentile API latency by endpoint
histogram_quantile(
  0.95,
  sum by (path, le) (rate(talent_vault_api_request_duration_seconds_bucket[5m]))
)

# Time spent on a single pipeline tick (aggregate window + optional sync)
histogram_quantile(0.9, rate(talent_vault_pipeline_tick_duration_seconds_bucket[5m]))
```

Scrape config lives in [monitoring/prometheus.yml](monitoring/prometheus.yml). All metric definitions are centralized in [src/monitoring/metrics.py](src/monitoring/metrics.py).

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
│   ├── api/                    # FastAPI service
│   │   ├── main.py             # ASGI app
│   │   ├── routes.py           # /persons, /persons/{passport}, /stats
│   │   └── dependencies.py     # SQLAlchemy session
│   ├── utils/
│   │   ├── config.py           # pydantic Settings (reads .env)
│   │   └── logger.py           # loguru configuration
│   └── main.py                 # Docker entrypoint (consumer + ETL loop)
├── frontend/                   # React 18 + Vite SPA (CRM look)
│   ├── Dockerfile              # multi-stage node build → nginx
│   ├── nginx.conf              # SPA fallback + /api proxy → api:8000
│   ├── package.json, vite.config.ts, tailwind.config.ts
│   └── src/
│       ├── pages/              # Splash, Pitch, Dashboard, Personas, Detail
│       ├── pitch/              # Carousel + slide contract (slides/index.ts)
│       ├── components/         # ui, layout, kpi, charts, persons, search
│       ├── lib/                # api client, types, queryClient, format
│       ├── hooks/              # usePersons, usePerson, useStats
│       └── state/pitchStore.ts # Zustand (en memoria, no persist)
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
| 🟠 Advanced    | REST API (FastAPI)                                | ✅      |
| 🟠 Advanced    | Prometheus metrics                                | ✅      |
| 🟠 Advanced    | Redis as cache / buffer                           | ✅      |
| 🔴 Expert      | Continuous pipeline (no manual ETL trigger)       | ✅      |
| 🔴 Expert      | Frontend CRM (React + Vite, splash + pitch)       | ✅      |

## Git workflow

| Branch | Owner       |
|--------|-------------|
| main   | Production  |
| dev    | Integration |
| v1     | Mar         |
| v2     | Michelle    |
| v3     | Rob         |

Each member works on their `vX` branch and opens a PR into `dev`.

## Contributors

<table>
  <tr>
    <td align="center" width="220">
      <a href="https://www.linkedin.com/in/mar-izquierdo-vaquer/">
        <img src="frontend/src/assets/contact/mar.png" width="110" alt="Mar Izquierdo Vaquer" /><br />
        <sub><b>Mar Izquierdo Vaquer</b></sub><br />
        <sub>in/mar-izquierdo-vaquer</sub>
      </a>
    </td>
    <td align="center" width="220">
      <a href="https://www.linkedin.com/in/ruperthlosada/">
        <img src="frontend/src/assets/contact/rob.png" height="165" alt="Roberto Molero" /><br />
        <sub><b>Roberto Molero</b></sub><br />
        <sub>in/ruperthlosada</sub>
      </a>
    </td>
    <td align="center" width="220">
      <a href="https://www.linkedin.com/in/michellegelves/">
        <img src="frontend/src/assets/contact/michelle.png" width="110" alt="Michelle Gelves" /><br />
        <sub><b>Michelle Gelves</b></sub><br />
        <sub>in/michellegelves</sub>
      </a>
    </td>
  </tr>
</table>
