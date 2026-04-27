from kafka import KafkaConsumer
from dotenv import load_dotenv
from pathlib import Path
import json
import os


load_dotenv(Path(__file__).parent.parent.parent / ".env")

from src.storage.mongo_client import get_db

# ─── Kafka ────────────────────────────────────────────
consumer = KafkaConsumer(
    os.getenv("KAFKA_TOPIC", "probando"),
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092"),
    auto_offset_reset=os.getenv("KAFKA_AUTO_OFFSET_RESET", "earliest"),
    enable_auto_commit=True,
    group_id=os.getenv("KAFKA_GROUP_ID", "data-engineering-consumer"),
    api_version=(2,0,2),
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

# ─── MongoDB ──────────────────────────────────────────
db = get_db()

collections = {
    "personal_data":     db["personal_data"],
    "location":          db["location"],
    "professional_data": db["professional_data"],
    "bank_data":         db["bank_data"],
    "net_data":          db["net_data"],
}

def classify(msg: dict) -> str:
    if "sex"     in msg: return "personal_data"
    if "city"    in msg: return "location"
    if "company" in msg: return "professional_data"
    if "IBAN"    in msg: return "bank_data"
    if "IPv4"    in msg: return "net_data"
    return "unknown"

print(f"✅ Conectado a Kafka y MongoDB")
print("⏳ Esperando mensajes...\n")

for message in consumer:
    data = message.value
    doc_type = classify(data)

    if doc_type == "unknown":
        print(f"[WARN] offset {message.offset} — no clasificado: {data}")
        continue

    result = collections[doc_type].insert_one(data)
    print(f"[offset {message.offset}] {doc_type:20s} → _id: {result.inserted_id}")