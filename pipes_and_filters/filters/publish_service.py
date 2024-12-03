import os
import multiprocessing as mp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class PublishProcess(mp.Process):
    def __init__(self, input_queue, output_queue):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.name = "PublishProcess"

    def send_email(self, user_alias, text):
        msg = MIMEMultipart()
        msg['From'] = os.getenv('EMAIL_USER')
        msg['To'] = os.getenv('RECIPIENT_EMAIL')
        msg['Subject'] = f"New Message from {user_alias}"

        body = f"From user: {user_alias}\nMessage: {text}"
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT')))
            server.starttls()
            server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    def run(self):
        logger.info(f"{self.name} started")
        while True:
            message = self.input_queue.get()

            if message is None:
                break

            try:
                if self.send_email(message['user_alias'], message['text']):
                    logger.info(f"Email sent for user: {message['user_alias']}")
                else:
                    logger.error(f"Failed to send email for user: {message['user_alias']}")
            except Exception as e:
                logger.error(f"Error in {self.name}: {e}")

        logger.info(f"{self.name} stopped")
