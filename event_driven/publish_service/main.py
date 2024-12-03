import json
import logging
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from common.rabbitmq import get_rabbitmq_connection
from common.config import settings

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_email(user_alias, text):
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_USER
    msg['To'] = settings.RECIPIENT_EMAIL
    msg['Subject'] = f"New Message from {user_alias}"

    body = f"From user: {user_alias}\nMessage: {text}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        logger.info(f"Email sent successfully for user {user_alias}")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False


def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        if send_email(message['user_alias'], message['text']):
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)


def main():
    while True:
        try:
            connection = get_rabbitmq_connection()
            channel = connection.channel()

            channel.queue_declare(queue=settings.PUBLISH_QUEUE)
            channel.basic_consume(
                queue=settings.PUBLISH_QUEUE,
                on_message_callback=callback
            )

            logger.info("Publish service is waiting for messages...")
            channel.start_consuming()
        except Exception as e:
            logger.error(f"Connection lost: {e}")
            logger.info("Attempting to reconnect...")
            time.sleep(5)


if __name__ == "__main__":
    main()
