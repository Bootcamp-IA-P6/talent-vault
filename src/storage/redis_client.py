import redis
import json
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent.parent / ".env")


def get_redis() -> redis.Redis:
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD", None),
        decode_responses=True
    )


def push_to_cache(r: redis.Redis, doc_type: str, data: dict) -> int:
    """
    Añade un documento a la lista de Redis correspondiente a su tipo.
    Devuelve el tamaño actual de la lista.
    """
    key = f"cache:{doc_type}"
    return r.rpush(key, json.dumps(data))


def flush_cache(r: redis.Redis, doc_type: str) -> list[dict]:
    """
    Extrae y vacía todos los documentos de una lista de Redis.
    Devuelve la lista de dicts listos para insertar en MongoDB.
    """
    key = f"cache:{doc_type}"
    pipeline = r.pipeline()
    pipeline.lrange(key, 0, -1)
    pipeline.delete(key)
    results, _ = pipeline.execute()
    return [json.loads(item) for item in results]


def cache_size(r: redis.Redis, doc_type: str) -> int:
    """Devuelve cuántos documentos hay en caché para un tipo."""
    return r.llen(f"cache:{doc_type}")