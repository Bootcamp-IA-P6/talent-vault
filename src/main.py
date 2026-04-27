import threading

from src.consumer.kafka_consumer import run as run_consumer
from src.processing.sql_loader import load_persons_to_sql
from src.processing.transformer import aggregate_window
from src.utils.logger import logger

TICK_SECONDS = 10
WINDOW_SECONDS = 60


def pipeline_loop(stop_event: threading.Event) -> None:
    logger.info(
        "Pipeline loop running every {}s over a {}s window",
        TICK_SECONDS,
        WINDOW_SECONDS,
    )
    while not stop_event.is_set():
        try:
            inserted = aggregate_window(WINDOW_SECONDS)
            if inserted > 0:
                load_persons_to_sql()
        except Exception:
            logger.exception("Pipeline tick failed")
        stop_event.wait(TICK_SECONDS)


def main() -> None:
    logger.info("Starting Talent Vault pipeline...")

    stop = threading.Event()
    t = threading.Thread(target=pipeline_loop, args=(stop,), daemon=True)
    t.start()

    try:
        run_consumer()
    finally:
        stop.set()


if __name__ == "__main__":
    main()
