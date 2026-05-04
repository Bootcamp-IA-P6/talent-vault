from prometheus_client import Counter, Histogram, Gauge

# ─── Consumer ─────────────────────────────────────────

MESSAGES_CONSUMED = Counter(
    "kafka_messages_consumed_total",
    "Total de mensajes consumidos desde Kafka",
    ["doc_type"]
)

MESSAGES_UNKNOWN = Counter(
    "kafka_messages_unknown_total",
    "Total de mensajes no clasificados"
)

BATCH_FLUSHED = Counter(
    "redis_batch_flushed_total",
    "Total de batches volcados de Redis a MongoDB",
    ["doc_type"]
)

BATCH_FLUSH_DURATION = Histogram(
    "redis_batch_flush_duration_seconds",
    "Tiempo en volcar un batch de Redis a MongoDB",
    ["doc_type"]
)

REDIS_CACHE_SIZE = Gauge(
    "redis_cache_size",
    "Mensajes actualmente en caché de Redis por tipo",
    ["doc_type"]
)

# ─── Transformer ──────────────────────────────────────

PERSONS_PROCESSED = Counter(
    "transformer_persons_processed_total",
    "Total de personas procesadas por el transformer"
)

PERSONS_SKIPPED = Counter(
    "transformer_persons_skipped_total",
    "Total de personas omitidas por datos incompletos"
)

TRANSFORMER_DURATION = Histogram(
    "transformer_run_duration_seconds",
    "Tiempo total de ejecución del transformer"
)

# ─── API ──────────────────────────────────────────────

API_REQUESTS = Counter(
    "api_requests_total",
    "Total de peticiones a la API",
    ["method", "endpoint", "status_code"]
)

API_LATENCY = Histogram(
    "api_request_duration_seconds",
    "Latencia de las peticiones a la API",
    ["endpoint"]
)