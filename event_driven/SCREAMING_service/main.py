import json
import logging
import time
from dotenv import load_dotenv
from common.rabbitmq import get_rabbitmq_connection
from common.config import settings

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        message['text'] = message['text'].upper()

        connection = get_rabbitmq_connection()
        channel = connection.channel()
        channel.queue_declare(queue=settings.PUBLISH_QUEUE)
        channel.basic_publish(
            exchange='',
            routing_key=settings.PUBLISH_QUEUE,
            body=json.dumps(message)
        )
        connection.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"Processed message from {message['user_alias']}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)


def main():
    while True:
        try:
            connection = get_rabbitmq_connection()
            channel = connection.channel()

            channel.queue_declare(queue=settings.SCREAMING_QUEUE)
            channel.basic_consume(
                queue=settings.SCREAMING_QUEUE,
                on_message_callback=callback
            )

            logger.info("Screaming service is waiting for messages...")
            channel.start_consuming()
        except Exception as e:
            logger.error(f"Connection lost: {e}")
            logger.info("Attempting to reconnect...")
            time.sleep(5)


if __name__ == "__main__":
    main()
