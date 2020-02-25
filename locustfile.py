from locust import HttpLocust, TaskSequence, seq_task, between
from locust.exception import StopLocust
from users import *
from hash import *
import locust.stats
import random

locust.stats.CSV_STATS_INTERVAL_SEC = 5


class LoginWithUniqueUsersSteps(TaskSequence):
    url_part = "/api/vote.dll"
    user_id = "NOT_FOUND"
    hash_id = "NOT_FOUND"

    def on_start(self):
        if len(USER) > 0:
            self.user_id = USER.pop()
        if len(HASH) > 0:
            self.hash_id = HASH.pop()

    @seq_task(1)
    def visit_site(self):
        self.client.get(self.url_part, params={"ID": self.hash_id, "USERID": f"{self.user_id}"})

    @seq_task(2)
    def fill_form(self):
        self.client.post(self.url_part, params={"ID": self.hash_id, "USERID": f"{self.user_id}"},
                         data={'WHO': f"{random.randrange(1, 10, 1)}", "POINTS": "999", "RODO_ACCEPT": "1"})

    @seq_task(3)
    def visit_thank_you_page(self):
        self.client.get(self.url_part, params={"ID": self.hash_id})
        raise StopLocust()


class LoginWithUniqueUsersTest(HttpLocust):
    task_set = LoginWithUniqueUsersSteps
    host = "https://example.com"
    wait_time = between(5, 10)

    def __init__(self):
        super(LoginWithUniqueUsersTest, self).__init__()
