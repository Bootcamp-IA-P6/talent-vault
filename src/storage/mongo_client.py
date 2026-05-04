from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent.parent.parent / ".env")

def get_db():
    client = MongoClient(
        host=os.getenv("MONGO_HOST", "localhost"),
        port=int(os.getenv("MONGO_PORT", 27017)),
        username=os.getenv("MONGO_USER"),
        password=os.getenv("MONGO_PASSWORD")
    )
    return client[os.getenv("MONGO_DB", "datagen")]