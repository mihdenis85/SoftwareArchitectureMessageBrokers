import time
import pika
import logging

from common.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_rabbitmq_connection(max_retries: int = 3, retry_delay: int = 5) -> pika.BlockingConnection | None:
    retries = 0
    while retries < max_retries:
        try:
            credentials = pika.PlainCredentials(
                settings.RABBITMQ_USER,
                settings.RABBITMQ_PASSWORD
            )
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.RABBITMQ_HOST,
                    port=settings.RABBITMQ_PORT,
                    credentials=credentials,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            logger.info("Successfully connected to RabbitMQ")
            return connection
        except Exception as e:
            retries += 1
            if retries == max_retries:
                logger.error(f"Failed to connect to RabbitMQ")
                raise
            logger.warning(
                f"Failed to connect to RabbitMQ (attempt {retries}/{max_retries}). Retrying...")
            time.sleep(retry_delay)
