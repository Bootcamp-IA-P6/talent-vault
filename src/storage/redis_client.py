"""Redis-backed fragment buffer for real-time person assembly.

For every fragment that arrives from Kafka, the consumer also stores it in
Redis with a TTL. When a `personal` fragment lands, we attempt to find its
four siblings already buffered in Redis. If all are present we emit a fully
assembled person directly to Postgres, skipping the periodic Mongo aggregator.

Key layout (NAMESPACE = "tv"):

    tv:personal:{passport}              STRING  json(payload)
    tv:bank:{passport}                  STRING  json(payload)
    tv:net:{address}                    STRING  json(payload)
    tv:professional:rec:{uuid}          STRING  json(payload)
    tv:professional:tok:{token}         SET     {uuid, ...}     # one entry per token of fullname
    tv:location:rec:{uuid}              STRING  json(payload)
    tv:location:tok:{token}             SET     {uuid, ...}

The token-set strategy mirrors the in-memory `index_by_fullname_tokens` used
by the batch transformer, so the same fuzzy-match constraint applies:
a record matches when its fullname contains both `name` and `last_name`.
"""

import json
import uuid

import redis

from src.utils.config import settings

NAMESPACE = "tv"


def build_client() -> redis.Redis:
    return redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        decode_responses=True,
    )


def _key(*parts: str) -> str:
    return ":".join((NAMESPACE, *parts))


def register_fragment(client: redis.Redis, type_: str, payload: dict, ttl: int) -> None:
    """Buffer a freshly arrived fragment in Redis, keyed for later assembly."""
    if type_ == "personal":
        passport = payload.get("passport")
        if passport:
            client.setex(_key("personal", passport), ttl, json.dumps(payload))
        return

    if type_ == "bank":
        passport = payload.get("passport")
        if passport:
            client.setex(_key("bank", passport), ttl, json.dumps(payload))
        return

    if type_ == "net":
        address = payload.get("address")
        if address:
            client.setex(_key("net", address), ttl, json.dumps(payload))
        return

    if type_ in ("professional", "location"):
        fullname = payload.get("fullname") or ""
        tokens = fullname.split()
        if not tokens:
            return
        rec_id = uuid.uuid4().hex
        client.setex(_key(type_, "rec", rec_id), ttl, json.dumps(payload))
        pipe = client.pipeline()
        for token in tokens:
            tok_key = _key(type_, "tok", token)
            pipe.sadd(tok_key, rec_id)
            pipe.expire(tok_key, ttl)
        pipe.execute()


def _pop_fuzzy(client: redis.Redis, type_: str, name: str, last_name: str) -> dict | None:
    """Find and consume a buffered record whose fullname contains both name and last_name."""
    if not name or not last_name:
        return None

    name_tok = name.split()[0]
    last_tok = last_name.split()[0]
    name_key = _key(type_, "tok", name_tok)
    last_key = _key(type_, "tok", last_tok)

    candidates = client.sinter(name_key, last_key)
    for rec_id in candidates:
        rec_key = _key(type_, "rec", rec_id)
        raw = client.get(rec_key)
        if not raw:
            client.srem(name_key, rec_id)
            client.srem(last_key, rec_id)
            continue
        record = json.loads(raw)
        fullname = record.get("fullname") or ""
        if name in fullname and last_name in fullname:
            pipe = client.pipeline()
            pipe.delete(rec_key)
            for token in fullname.split():
                pipe.srem(_key(type_, "tok", token), rec_id)
            pipe.execute()
            return record
    return None


def try_assemble_person(client: redis.Redis, personal: dict) -> dict | None:
    """Try to assemble a full person using the personal fragment + buffered siblings.

    Returns the assembled person dict on success, or None if any sibling is
    still missing. On success all five fragments are removed from Redis;
    partial consumption may happen on failure (the lost fragment is still in
    Mongo, so the batch path remains the safety net).
    """
    passport = personal.get("passport")
    name = personal.get("name") or ""
    last_name = personal.get("last_name") or ""
    if not passport or not name or not last_name:
        return None

    bank_raw = client.get(_key("bank", passport))
    if not bank_raw:
        return None
    bank = json.loads(bank_raw)

    professional = _pop_fuzzy(client, "professional", name, last_name)
    if not professional:
        return None
    location = _pop_fuzzy(client, "location", name, last_name)
    if not location:
        return None

    address = location.get("address")
    if not address:
        return None
    net_raw = client.get(_key("net", address))
    if not net_raw:
        return None
    net = json.loads(net_raw)

    pipe = client.pipeline()
    pipe.delete(_key("personal", passport))
    pipe.delete(_key("bank", passport))
    pipe.delete(_key("net", address))
    pipe.execute()

    fullname = f"{name} {last_name}".strip()
    sex = personal.get("sex")
    if isinstance(sex, list):
        sex = sex[0] if sex else None

    return {
        "passport": passport,
        "name": personal.get("name"),
        "last_name": personal.get("last_name"),
        "fullname": fullname,
        "email": personal.get("email"),
        "telfnumber": personal.get("telfnumber"),
        "sex": sex,
        "IBAN": bank.get("IBAN"),
        "salary": bank.get("salary"),
        "company": professional.get("company"),
        "company_address": professional.get("company address"),
        "company_email": professional.get("company_email"),
        "company_telfnumber": professional.get("company_telfnumber"),
        "job": professional.get("job"),
        "city": location.get("city"),
        "address": address,
        "IPv4": net.get("IPv4"),
    }
