# test_kafka.py
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "probando",
    bootstrap_servers="localhost:29092",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    group_id="test-debug-99",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    consumer_timeout_ms=10000  # para que no se quede colgado, para a los 10s
)

count = 0
for message in consumer:
    print(f"✅ Mensaje recibido: {message.value}")
    count += 1
    if count >= 3:
        break

print(f"Total recibidos: {count}")
consumer.close()