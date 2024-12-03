import multiprocessing as mp
import logging

logger = logging.getLogger(__name__)


class ScreamingProcess(mp.Process):
    def __init__(self, input_queue, output_queue):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.name = "ScreamingProcess"

    def run(self):
        logger.info(f"{self.name} started")
        while True:
            message = self.input_queue.get()

            if message is None:
                if self.output_queue:
                    self.output_queue.put(None)
                break

            try:
                message['text'] = message['text'].upper()
                self.output_queue.put(message)
                logger.info(f"Message screamed: {message['user_alias']}")
            except Exception as e:
                logger.error(f"Error in {self.name}: {e}")

        logger.info(f"{self.name} stopped")
