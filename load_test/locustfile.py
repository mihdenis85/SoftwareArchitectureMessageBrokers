from locust import HttpUser, task, between
import random


class MessageUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def send_message(self):
        message = {
            "user_alias": f"user_{random.randint(1, 1000)}",
            "text": f"Test message {random.randint(1, 1000)}"
        }
        self.client.post("/message", json=message)
