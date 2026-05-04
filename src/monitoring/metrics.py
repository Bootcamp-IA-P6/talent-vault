"""Prometheus metrics for the Talent Vault pipeline.

All metric objects are module-level singletons so they accumulate across the
lifetime of the process. They are scraped from two HTTP endpoints:

- The API container exposes them at GET /metrics (FastAPI route).
- The app container (consumer + ETL loop) exposes them on a dedicated HTTP
  server started from src/main.py via start_metrics_server().
"""

from prometheus_client import Counter, Gauge, Histogram, start_http_server

# ---- Kafka consumer ----

kafka_messages_consumed = Counter(
    "talent_vault_kafka_messages_consumed_total",
    "Kafka messages consumed by the app, labelled by classified type.",
    ["type"],
)

# ---- Aggregator (Mongo raw -> Mongo persons) ----

aggregate_runs = Counter(
    "talent_vault_aggregate_runs_total",
    "Number of aggregator passes.",
    ["mode"],  # batch | window
)

aggregate_duration_seconds = Histogram(
    "talent_vault_aggregate_duration_seconds",
    "Time spent in a single aggregator pass.",
    ["mode"],
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10, 30, 60, 120, 300),
)

aggregate_persons_inserted = Counter(
    "talent_vault_aggregate_persons_inserted_total",
    "Persons inserted into the MongoDB persons collection.",
)

aggregate_persons_skipped = Counter(
    "talent_vault_aggregate_persons_skipped_total",
    "Personals skipped during aggregation (e.g. missing passport).",
)

aggregate_duplicates = Counter(
    "talent_vault_aggregate_duplicates_total",
    "Personals dropped because the unified person already existed in Mongo.",
)

# ---- SQL loader (Mongo persons -> Postgres) ----

sql_sync_runs = Counter(
    "talent_vault_sql_sync_runs_total",
    "Number of Mongo->Postgres sync runs.",
)

sql_sync_duration_seconds = Histogram(
    "talent_vault_sql_sync_duration_seconds",
    "Time spent syncing Mongo persons to Postgres.",
    buckets=(0.1, 0.5, 1, 2, 5, 10, 30, 60, 120, 300),
)

sql_persons_synced = Counter(
    "talent_vault_sql_persons_synced_total",
    "Persons upserted into Postgres.",
)

# ---- Pipeline loop ----

pipeline_tick_duration_seconds = Histogram(
    "talent_vault_pipeline_tick_duration_seconds",
    "Time spent in one pipeline tick (aggregate window + optional sql sync).",
)

pipeline_last_inserted = Gauge(
    "talent_vault_pipeline_last_window_inserted",
    "Persons inserted by the most recent windowed aggregation pass.",
)

# ---- Real-time assembly via Redis ----

realtime_assembly_attempts = Counter(
    "talent_vault_realtime_assembly_attempts_total",
    "Personals seen by the consumer that triggered a real-time assembly attempt.",
)

realtime_persons_assembled = Counter(
    "talent_vault_realtime_persons_assembled_total",
    "Persons assembled in real time and upserted directly into Postgres.",
)

# ---- API ----

api_requests_total = Counter(
    "talent_vault_api_requests_total",
    "API requests received, labelled by method, path template and status code.",
    ["method", "path", "status"],
)

api_request_duration_seconds = Histogram(
    "talent_vault_api_request_duration_seconds",
    "API request latency, labelled by method and path template.",
    ["method", "path"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
)


def start_metrics_server(port: int = 9100) -> None:
    """Start an HTTP server exposing the metrics on /metrics.

    Used by the app container, which runs background workers and therefore
    does not have an HTTP framework of its own.
    """
    start_http_server(port)
