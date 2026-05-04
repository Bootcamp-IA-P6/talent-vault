import threading
import time
import schedule
import uvicorn
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")

from src.consumer.kafka_consumer import run_consumer
from src.processing.transformer import run_transformer
from src.utils.logger import logger
import os

TRANSFORMER_INTERVAL = int(os.getenv("TRANSFORMER_INTERVAL_MINUTES", 5))


def start_api():
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, log_level="warning")


def run_scheduler():
    """Ejecuta el transformer cada X minutos en bucle."""
    logger.info(f"Scheduler iniciado — transformer cada {TRANSFORMER_INTERVAL} minutos")

    # Primera ejecución inmediata al arrancar
    run_transformer()

    schedule.every(TRANSFORMER_INTERVAL).minutes.do(run_transformer)

    while True:
        schedule.run_pending()
        time.sleep(30)


def main():
    logger.info("Arrancando Talent Vault...")

    # Consumer en hilo separado (bucle infinito)
    consumer_thread = threading.Thread(target=run_consumer, daemon=True, name="kafka-consumer")
    consumer_thread.start()
    logger.info("Consumer iniciado en hilo separado")

    # Scheduler del transformer en hilo separado
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True, name="transformer-scheduler")
    scheduler_thread.start()
    logger.info(f"Transformer scheduler iniciado — cada {TRANSFORMER_INTERVAL} minutos")

    # API en el hilo principal
    logger.info("Iniciando API en http://0.0.0.0:8000")
    start_api()


if __name__ == "__main__":
    main()