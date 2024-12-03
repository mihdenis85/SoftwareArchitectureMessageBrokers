from os import getenv

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RABBITMQ_USER: str = getenv('RABBITMQ_USER')
    RABBITMQ_PASSWORD: str = getenv('RABBITMQ_PASSWORD')
    RABBITMQ_HOST: str = getenv('RABBITMQ_HOST')
    RABBITMQ_PORT: int = getenv('RABBITMQ_PORT')

    SMTP_SERVER: str = getenv('SMTP_SERVER')
    SMTP_PORT: int = getenv('SMTP_PORT')
    EMAIL_USER: str = getenv('EMAIL_USER')
    EMAIL_PASSWORD: str = getenv('EMAIL_PASSWORD')
    RECIPIENT_EMAIL: str = getenv('RECIPIENT_EMAIL')

    FILTER_QUEUE: str = getenv('FILTER_QUEUE')
    SCREAMING_QUEUE: str = getenv('SCREAMING_QUEUE')
    PUBLISH_QUEUE: str = getenv('PUBLISH_QUEUE')


settings = Settings()
