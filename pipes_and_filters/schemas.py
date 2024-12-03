from pydantic import BaseModel


class Message(BaseModel):
    user_alias: str
    text: str
