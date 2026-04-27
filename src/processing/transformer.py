from collections import defaultdict
from collections.abc import Iterable
from datetime import UTC, datetime, timedelta

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from src.storage.mongo_client import (
    build_client,
    get_database,
    get_persons_collection,
    get_raw_collection,
)
from src.utils.logger import logger


def load_raw_by_type(raw: Collection, since: datetime | None = None) -> dict[str, list[dict]]:
    query = {"received_at": {"$gte": since}} if since else {}
    grouped: dict[str, list[dict]] = defaultdict(list)
    for doc in raw.find(query, {"_id": 0, "type": 1, "payload": 1}):
        grouped[doc["type"]].append(doc["payload"])
    return grouped


def index_by(items: Iterable[dict], key: str) -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        value = item.get(key)
        if value is None:
            continue
        result[value].append(item)
    return result


def pop_match(index: dict[str, list[dict]], value: str | None) -> dict:
    if value is None:
        return {}
    bucket = index.get(value)
    if not bucket:
        return {}
    return bucket.pop(0)


def index_by_fullname_tokens(items: Iterable[dict]) -> dict[str, list[dict]]:
    """Index records by every whitespace-separated token in their fullname."""
    index: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        fullname = item.get("fullname") or ""
        for token in fullname.split():
            index[token].append(item)
    return index


def pop_fuzzy_match(
    index: dict[str, list[dict]],
    name: str | None,
    last_name: str | None,
) -> dict:
    """Find a record whose fullname contains both name and last_name as substrings."""
    if not name or not last_name:
        return {}
    bucket = index.get(last_name.split()[0], [])
    for record in bucket:
        fullname = record.get("fullname") or ""
        if name in fullname and last_name in fullname:
            for token in fullname.split():
                if record in index[token]:
                    index[token].remove(record)
            return record
    return {}


def build_person(
    personal: dict,
    bank_by_passport: dict[str, list[dict]],
    professional_index: dict[str, list[dict]],
    location_index: dict[str, list[dict]],
    net_by_address: dict[str, list[dict]],
) -> dict | None:
    passport = personal.get("passport")
    if not passport:
        return None

    name = personal.get("name") or ""
    last_name = personal.get("last_name") or ""
    fullname = f"{name} {last_name}".strip()

    bank = pop_match(bank_by_passport, passport)
    professional = pop_fuzzy_match(professional_index, name, last_name)
    location = pop_fuzzy_match(location_index, name, last_name)
    address = location.get("address")
    net = pop_match(net_by_address, address)

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


def _aggregate(since: datetime | None, log_prefix: str) -> tuple[int, int, int]:
    client = build_client()
    db = get_database(client)
    raw = get_raw_collection(db)
    persons = get_persons_collection(db)

    grouped = load_raw_by_type(raw, since=since)

    bank_by_passport = index_by(grouped.get("bank", []), "passport")
    professional_index = index_by_fullname_tokens(grouped.get("professional", []))
    location_index = index_by_fullname_tokens(grouped.get("location", []))
    net_by_address = index_by(grouped.get("net", []), "address")

    personals = grouped.get("personal", [])

    inserted = 0
    skipped = 0
    duplicates = 0

    for personal in personals:
        person = build_person(
            personal,
            bank_by_passport,
            professional_index,
            location_index,
            net_by_address,
        )
        if person is None:
            skipped += 1
            continue
        try:
            persons.insert_one(person)
            inserted += 1
        except DuplicateKeyError:
            duplicates += 1

    logger.info(
        "{} inserted={} duplicates={} skipped={} personals_seen={}",
        log_prefix,
        inserted,
        duplicates,
        skipped,
        len(personals),
    )
    client.close()
    return inserted, duplicates, skipped


def aggregate_batch() -> None:
    logger.info("Full batch aggregation starting...")
    _aggregate(since=None, log_prefix="[batch]")


def aggregate_window(window_seconds: int = 60) -> int:
    cutoff = datetime.now(UTC) - timedelta(seconds=window_seconds)
    inserted, _, _ = _aggregate(since=cutoff, log_prefix=f"[window {window_seconds}s]")
    return inserted


if __name__ == "__main__":
    aggregate_batch()
