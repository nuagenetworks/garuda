# -*- coding: utf8 -*-

from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    """
    """
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        # self.login()
        pass

    @task
    def enterprises(self):
        """
        """
        self.client.get("/enterprises")

    @task
    def subnets(self):
        """
        """
        self.client.get("/subnets")
    #
    # @task
    # def index(self):
    #     """
    #     """
    #     self.client.get("/")

class WebsiteUser(HttpLocust):
    """
    """
    task_set = UserBehavior
    min_wait=1000
    max_wait=1500