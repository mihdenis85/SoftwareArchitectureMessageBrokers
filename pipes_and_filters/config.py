from os import getenv

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SMTP_SERVER: str = getenv("SMTP_SERVER")
    SMTP_PORT: int = getenv("SMTP_PORT")
    EMAIL_USER: str = getenv("EMAIL_USER")
    EMAIL_PASSWORD: str = getenv("EMAIL_PASSWORD")
    RECIPIENT_EMAIL: str = getenv("RECIPIENT_EMAIL")

    FILTER_QUEUE: str = getenv("FILTER_QUEUE")
    STREAMING_QUEUE: str = getenv("STREAMING_QUEUE")
    PUBLISH_QUEUE: str = getenv("PUBLISH_QUEUE")


settings = Settings()
