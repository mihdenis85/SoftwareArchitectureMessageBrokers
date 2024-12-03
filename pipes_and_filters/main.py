import os
import multiprocessing as mp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from filters.filter_service import FilterProcess
from filters.screaming_service import ScreamingProcess
from filters.publish_service import PublishProcess
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class Message(BaseModel):
    user_alias: str
    text: str


# Global queues
filter_input_queue = None
processes = []


@app.post("/message")
async def send_message(message: Message):
    try:
        filter_input_queue.put({
            'user_alias': message.user_alias,
            'text': message.text
        })
        return {"status": "Message sent successfully"}
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("startup")
async def startup_event():
    global filter_input_queue, processes

    # Create queues
    filter_input_queue = mp.Queue()
    screaming_queue = mp.Queue()
    publish_queue = mp.Queue()

    # Create and start processes
    filter_process = FilterProcess(
        input_queue=filter_input_queue,
        output_queue=screaming_queue
    )

    screaming_process = ScreamingProcess(
        input_queue=screaming_queue,
        output_queue=publish_queue
    )

    publish_process = PublishProcess(
        input_queue=publish_queue,
        output_queue=None
    )

    processes = [filter_process, screaming_process, publish_process]

    for process in processes:
        process.start()
        logger.info(f"Started process: {process.name}")


@app.on_event("shutdown")
async def shutdown_event():
    global processes, filter_input_queue

    # Signal processes to stop
    filter_input_queue.put(None)

    # Wait for all processes to finish
    for process in processes:
        process.join()
        logger.info(f"Stopped process: {process.name}")


def main():
    uvicorn.run(
        app,
        host=os.getenv('API_HOST', '0.0.0.0'),
        port=int(os.getenv('API_PORT', 8000))
    )


if __name__ == "__main__":
    main()