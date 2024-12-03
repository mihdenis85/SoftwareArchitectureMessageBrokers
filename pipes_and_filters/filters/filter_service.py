import multiprocessing as mp
import logging

logger = logging.getLogger(__name__)

STOP_WORDS = ['bird-watching', 'ailurophobia', 'mango']


class FilterProcess(mp.Process):
    def __init__(self, input_queue, output_queue):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.name = "FilterProcess"

    def run(self):
        logger.info(f"{self.name} started")
        while True:
            message = self.input_queue.get()

            if message is None:
                if self.output_queue:
                    self.output_queue.put(None)
                break

            try:
                text = message['text'].lower()
                if not any(word in text for word in STOP_WORDS):
                    self.output_queue.put(message)
                    logger.info(f"Message passed filter: {message['user_alias']}")
                else:
                    logger.info(f"Message filtered out: {message['user_alias']}")
            except Exception as e:
                logger.error(f"Error in {self.name}: {e}")

        logger.info(f"{self.name} stopped")
