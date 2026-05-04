from kafka import KafkaConsumer
from dotenv import load_dotenv
from pathlib import Path
import time
import json
import os

load_dotenv(Path(__file__).parent.parent.parent / ".env")

from src.consumer.utils import classify
from src.storage.mongo_client import get_db
from src.storage.redis_client import get_redis, push_to_cache, flush_cache
from src.utils.logger import logger as log
from src.monitoring.metrics import (
    MESSAGES_CONSUMED,
    MESSAGES_UNKNOWN,
    BATCH_FLUSHED,
    BATCH_FLUSH_DURATION,
    REDIS_CACHE_SIZE,
)

BATCH_SIZE = int(os.getenv("REDIS_BATCH_SIZE", 50))


def flush_to_mongo(collections: dict, r, doc_type: str):
    """Vuelca el batch de Redis a MongoDB y registra métricas."""
    start = time.time()
    docs = flush_cache(r, doc_type)
    if docs:
        collections[doc_type].insert_many(docs)
        duration = time.time() - start
        BATCH_FLUSHED.labels(doc_type=doc_type).inc()
        BATCH_FLUSH_DURATION.labels(doc_type=doc_type).observe(duration)
        log.info(f"Batch volcado a MongoDB | type={doc_type} | docs={len(docs)} | duration={duration:.3f}s")


def run_consumer():
    """Punto de entrada del consumer."""

    log.info("Iniciando conexión con Kafka...")
    consumer = KafkaConsumer(
        os.getenv("KAFKA_TOPIC", "probando"),
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092"),
        auto_offset_reset=os.getenv("KAFKA_AUTO_OFFSET_RESET", "earliest"),
        enable_auto_commit=True,
        group_id=os.getenv("KAFKA_GROUP_ID", "data-engineering-consumer"),
        api_version=(2, 0, 2),
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )

    log.info("Iniciando conexión con Redis...")
    r = get_redis()

    log.info("Iniciando conexión con MongoDB...")
    db = get_db()

    collections = {
        "personal_data":     db["personal_data"],
        "location":          db["location"],
        "professional_data": db["professional_data"],
        "bank_data":         db["bank_data"],
        "net_data":          db["net_data"],
    }

    log.info(f"Conectado a Kafka [{os.getenv('KAFKA_TOPIC')}] | Redis | MongoDB [{os.getenv('MONGO_DB')}]")
    log.info(f"Batch size: {BATCH_SIZE} mensajes por tipo antes de volcar a MongoDB")
    log.info("Esperando mensajes...")

    for message in consumer:
        data     = message.value
        doc_type = classify(data)

        if doc_type == "unknown":
            MESSAGES_UNKNOWN.inc()
            log.warning(f"Mensaje no clasificado | offset={message.offset} | data={data}")
            continue

        MESSAGES_CONSUMED.labels(doc_type=doc_type).inc()

        size = push_to_cache(r, doc_type, data)
        REDIS_CACHE_SIZE.labels(doc_type=doc_type).set(size)
        log.debug(f"offset={message.offset} | type={doc_type} | cache_size={size}")

        if size >= BATCH_SIZE:
            flush_to_mongo(collections, r, doc_type)
            REDIS_CACHE_SIZE.labels(doc_type=doc_type).set(0)


if __name__ == "__main__":
    run_consumer()