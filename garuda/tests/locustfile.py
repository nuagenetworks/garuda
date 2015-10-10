# -*- coding: utf8 -*-

from locust import HttpLocust, TaskSet, task
from tdldk.v1_0 import *


class UserBehavior(TaskSet):
    """
    """
    AUTH    = 'cm9vdDoxMjJkZWE1ZC02YjhjLTQ3MWMtOGQ3NC1iNDk1ODE4OTc5YTM='
    LIST_ID = 'cc2ba6ad-33f4-4b4d-9fad-034df4d7db1f'
    TASK_ID = 'c5781f4f-2f92-44fe-b96b-84eef98914d9'

    def on_start(self):
        pass

    @task
    def lists(self):
        """
        """
        self.client.get("/lists", headers={'Authorization': 'XREST %s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)

    @task
    def users(self):
        """
        """
        self.client.get("/users", headers={'Authorization': 'XREST %s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)

    @task
    def tasks_in_list(self):
        """
        """
        self.client.get("/lists/%s/tasks" % self.LIST_ID, headers={'Authorization': 'XREST %s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)

    @task
    def users_in_task(self):
        """
        """
        self.client.get("/tasks/%s/users" % self.TASK_ID, headers={'Authorization': 'XREST %s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)


class WebsiteUser(HttpLocust):
    """
    """
    task_set = UserBehavior
    min_wait=1000
    max_wait=1500