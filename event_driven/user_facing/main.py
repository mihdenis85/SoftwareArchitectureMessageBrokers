import json
import logging
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from common.rabbitmq import get_rabbitmq_connection
from common.config import settings
from schemas import Message

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/message")
async def send_message(message: Message):
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()

        channel.queue_declare(queue=settings.FILTER_QUEUE)

        channel.basic_publish(
            exchange='',
            routing_key=settings.FILTER_QUEUE,
            body=json.dumps({
                'user_alias': message.user_alias,
                'text': message.text
            })
        )

        connection.close()
        logger.info(f"Message from {message.user_alias} sent successfully")
        return {"status": "Message sent successfully"}
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
