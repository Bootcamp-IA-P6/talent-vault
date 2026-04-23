from src.consumer.kafka_consumer import run as run_consumer
from src.utils.logger import logger


def main():
    logger.info("Starting Talent Vault pipeline...")
    run_consumer()


if __name__ == "__main__":
    main()
