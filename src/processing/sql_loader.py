from sqlalchemy.dialects.postgresql import insert

from src.models.sql_models import Person
from src.storage.mongo_client import build_client, get_database, get_persons_collection
from src.storage.sql_client import build_engine, build_session_factory, create_schema
from src.utils.logger import logger

PERSON_FIELDS = {c.name for c in Person.__table__.columns}


def project_to_sql(doc: dict) -> dict:
    return {field: doc.get(field) for field in PERSON_FIELDS}


def load_persons_to_sql(batch_size: int = 500) -> None:
    engine = build_engine()
    create_schema(engine)
    session_factory = build_session_factory(engine)

    mongo = build_client()
    persons_col = get_persons_collection(get_database(mongo))

    total = persons_col.count_documents({})
    logger.info("Loading {} persons from Mongo into Postgres...", total)

    buffer: list[dict] = []
    inserted = 0
    updated = 0

    with session_factory() as session:
        for doc in persons_col.find({}, {"_id": 0}):
            buffer.append(project_to_sql(doc))
            if len(buffer) >= batch_size:
                stats = _flush(session, buffer)
                inserted += stats[0]
                updated += stats[1]
                buffer.clear()
        if buffer:
            stats = _flush(session, buffer)
            inserted += stats[0]
            updated += stats[1]

    mongo.close()
    engine.dispose()
    logger.info("Done. processed={} (upsert by passport)", inserted + updated)


def _flush(session, rows: list[dict]) -> tuple[int, int]:
    stmt = insert(Person).values(rows)
    update_cols = {c.name: c for c in stmt.excluded if c.name != "passport"}
    stmt = stmt.on_conflict_do_update(index_elements=["passport"], set_=update_cols)
    result = session.execute(stmt)
    session.commit()
    return (result.rowcount or 0, 0)


if __name__ == "__main__":
    load_persons_to_sql()
