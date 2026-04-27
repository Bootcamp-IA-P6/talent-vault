from collections.abc import Generator

from sqlalchemy.orm import Session

from src.storage.sql_client import build_engine, build_session_factory

_engine = build_engine()
_session_factory = build_session_factory(_engine)


def get_session() -> Generator[Session, None, None]:
    with _session_factory() as session:
        yield session
