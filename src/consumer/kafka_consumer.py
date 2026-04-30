import json
import signal
from collections.abc import Iterator

from kafka import KafkaConsumer

from src.monitoring.metrics import (
    kafka_messages_consumed,
    realtime_assembly_attempts,
    realtime_persons_assembled,
)
from src.processing.sql_loader import upsert_person
from src.storage.mongo_client import build_client, get_database, get_raw_collection, insert_raw
from src.storage.redis_client import build_client as build_redis_client
from src.storage.redis_client import register_fragment, try_assemble_person
from src.storage.sql_client import build_engine, build_session_factory, create_schema
from src.utils.config import settings
from src.utils.logger import logger

MessageType = str

PERSONAL = "personal"
BANK = "bank"
PROFESSIONAL = "professional"
LOCATION = "location"
NET = "net"
UNKNOWN = "unknown"


def classify(payload: dict) -> MessageType:
    keys = set(payload.keys())

    if {"name", "last_name", "passport", "email"} <= keys:
        return PERSONAL
    if {"passport", "IBAN", "salary"} <= keys:
        return BANK
    if {"company", "job"} <= keys:
        return PROFESSIONAL
    if {"fullname", "city", "address"} <= keys:
        return LOCATION
    if keys == {"address", "IPv4"}:
        return NET
    return UNKNOWN


def build_consumer() -> KafkaConsumer:
    return KafkaConsumer(
        settings.kafka_topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_group_id,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        client_id="talent-vault-consumer",
    )


def stream_messages(consumer: KafkaConsumer) -> Iterator[tuple[MessageType, dict]]:
    for record in consumer:
        payload = record.value
        yield classify(payload), payload


def run() -> None:
    logger.info(
        "Connecting consumer broker={} topic={} group={}",
        settings.kafka_bootstrap_servers,
        settings.kafka_topic,
        settings.kafka_group_id,
    )
    consumer = build_consumer()
    mongo_client = build_client()
    collection = get_raw_collection(get_database(mongo_client))

    redis_client = build_redis_client()
    sql_engine = build_engine()
    create_schema(sql_engine)
    sql_session_factory = build_session_factory(sql_engine)
    ttl = settings.redis_fragment_ttl_seconds

    stop = False

    def handle_sigterm(signum, _frame):
        nonlocal stop
        logger.info("Received signal {}, shutting down...", signum)
        stop = True
        consumer.close()

    signal.signal(signal.SIGINT, handle_sigterm)
    signal.signal(signal.SIGTERM, handle_sigterm)

    try:
        for msg_type, payload in stream_messages(consumer):
            insert_raw(collection, msg_type, payload)
            kafka_messages_consumed.labels(type=msg_type).inc()

            try:
                register_fragment(redis_client, msg_type, payload, ttl)
            except Exception:
                logger.exception("Failed to register fragment in Redis (continuing)")

            identifier = payload.get("passport") or payload.get("fullname") or payload.get("address")
            logger.info("stored type={} key={}", msg_type, identifier)

            if msg_type == PERSONAL:
                realtime_assembly_attempts.inc()
                try:
                    person = try_assemble_person(redis_client, payload)
                except Exception:
                    logger.exception("Real-time assembly failed (falling back to batch)")
                    person = None
                if person is not None:
                    try:
                        with sql_session_factory() as session:
                            upsert_person(session, person)
                        realtime_persons_assembled.inc()
                        logger.info(
                            "[realtime] assembled passport={} fullname={}",
                            person["passport"],
                            person["fullname"],
                        )
                    except Exception:
                        logger.exception("Real-time upsert to Postgres failed")

            if stop:
                break
    finally:
        consumer.close()
        mongo_client.close()
        sql_engine.dispose()
        try:
            redis_client.close()
        except Exception:
            pass
        logger.info("Consumer closed")


if __name__ == "__main__":
    run()
