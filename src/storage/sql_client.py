from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.models.sql_models import Base
from src.utils.config import settings
from src.utils.logger import logger


def build_engine() -> Engine:
    uri = (
        f"postgresql+psycopg2://{settings.postgres_user}:{settings.postgres_password}"
        f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    )
    logger.info("Connecting to Postgres host={} port={}", settings.postgres_host, settings.postgres_port)
    return create_engine(uri, pool_pre_ping=True)


def create_schema(engine: Engine) -> None:
    Base.metadata.create_all(engine)


def build_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False)
