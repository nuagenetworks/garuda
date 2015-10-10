# -*- coding: utf8 -*-

from locust import HttpLocust, TaskSet, task
from tdldk.v1_0 import *
import json

class UserBehavior(TaskSet):
    """
    """
    AUTH    = 'cm9vdDo4ZTI2ODU3YS04NDNhLTQ0ZmUtOWQ4Ny1kOWZmM2ZmYzQyMzI='
    LIST_ID = '19651d37-8334-481f-986c-4f1428bbf40f'
    TASK_ID = '628d097c-63c3-4239-9185-b09132797963'

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

    @task
    def create_delete_list(self):
        """
        """
        response = self.client.post("/lists", data=json.dumps({'title': 'test', 'description': 'test'}), headers={'Authorization': 'XREST %s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)
        data = json.loads(response.content)
        self.client.delete("/lists/%s" % data[0]["ID"], headers={'Authorization': 'XREST %s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)


class WebsiteUser(HttpLocust):
    """
    """
    task_set = UserBehavior
    min_wait=1000
    max_wait=1500