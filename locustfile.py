import random
import os
import psutil
from locust import HttpUser, task, between, events
from gevent.pool import Pool

TARGET = "https://abc.xyz"

CPU_CORES = psutil.cpu_count(logical=True)

print(f"Detected CPU cores: {CPU_CORES}")

class WebsiteUser(HttpUser):

    host = TARGET
    wait_time = between(0.1, 0.5)

    @task(5)
    def homepage(self):
        self.client.get("/", name="homepage")

    @task(3)
    def blog(self):
        self.client.get("/blog", name="blog")

    @task(2)
    def random_page(self):
        pages = [
            "/",
            "/about",
            "/contact",
            "/blog",
        ]
        page = random.choice(pages)
        self.client.get(page, name="random_page")

request_count = 0

@events.request.add_listener
def request_handler(request_type, name, response_time, response_length, response, context, exception, **kwargs):
    global request_count
    request_count += 1

    if request_count % 1000 == 0:
        print(f"Total Requests: {request_count}")