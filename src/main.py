import threading
import uvicorn
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")

from src.consumer.kafka_consumer import run_consumer
from src.utils.logger import logger


def start_api():
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, log_level="warning")


def main():
    logger.info("Arrancando Talent Vault...")

    # Consumer en hilo separado (bucle infinito)
    consumer_thread = threading.Thread(target=run_consumer, daemon=True, name="kafka-consumer")
    consumer_thread.start()
    logger.info("Consumer iniciado en hilo separado")

    # API en el hilo principal (bloquea hasta que se detiene)
    logger.info("Iniciando API en http://0.0.0.0:8000")
    start_api()


if __name__ == "__main__":
    main()