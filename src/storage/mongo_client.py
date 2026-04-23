from datetime import UTC, datetime

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from src.utils.config import settings
from src.utils.logger import logger

RAW_COLLECTION = "raw_messages"
PERSONS_COLLECTION = "persons"


def build_client() -> MongoClient:
    uri = (
        f"mongodb://{settings.mongo_user}:{settings.mongo_password}"
        f"@{settings.mongo_host}:{settings.mongo_port}/?authSource=admin"
    )
    logger.info("Connecting to MongoDB host={} port={}", settings.mongo_host, settings.mongo_port)
    return MongoClient(uri)


def get_database(client: MongoClient) -> Database:
    return client[settings.mongo_db]


def get_raw_collection(db: Database) -> Collection:
    collection = db[RAW_COLLECTION]
    collection.create_index("type")
    collection.create_index("received_at")
    return collection


def get_persons_collection(db: Database) -> Collection:
    collection = db[PERSONS_COLLECTION]
    collection.create_index("passport", unique=True)
    return collection


def insert_raw(collection: Collection, message_type: str, payload: dict) -> None:
    document = {
        "type": message_type,
        "payload": payload,
        "received_at": datetime.now(UTC),
    }
    collection.insert_one(document)
