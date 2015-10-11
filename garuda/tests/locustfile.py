# -*- coding: utf8 -*-

from locust import HttpLocust, TaskSet, task
from tdldk.v1_0 import *
import json

class UserBehavior(TaskSet):
    """
    """
    AUTH    = 'cm9vdDo5Zjk3NmQ1MC02YTA3LTQyM2ItODAxYy1jZDJjZTQyMmYwNjE='
    LIST_ID = 'b7c1df62-0bf3-437a-9bf6-a8822a1b1fee'
    TASK_ID = '118f0eb4-6434-4594-b9f7-f3799ba6905c'

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
    min_wait=10
    max_wait=15