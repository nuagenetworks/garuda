# -*- coding: utf8 -*-

from locust import HttpLocust, TaskSet, task
from tdldk.v1_0 import *
import json
import uuid

class UserBehavior(TaskSet):
    """
    """
    AUTH    = 'XREST cm9vdDozMmZiNmQwNC0wZjM0LTQzNjItYmI3YS05YjA4NGUyOTkwMGY='
    LIST_ID = '561b1cc37ddf1f4a092a83f5'
    TASK_ID = '561b1cc37ddf1f4a092a83f6'
    USER_ID = '561b1cc37ddf1f4a092a83f9'

    def on_start(self):
        pass

    @task
    def lists(self):
        """
        """
        self.client.get("/lists", headers={'Authorization': '%s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)

    @task
    def one_list(self):
        """
        """
        self.client.get("/lists/%s" % self.LIST_ID, headers={'Authorization': '%s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)

    @task
    def users(self):
        """
        """
        self.client.get("/users", headers={'Authorization': '%s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)

    @task
    def tasks_in_list(self):
        """
        """
        self.client.get("/lists/%s/tasks" % self.LIST_ID, headers={'Authorization': '%s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)

    @task
    def users_in_task(self):
        """
        """
        self.client.get("/tasks/%s/users" % self.TASK_ID, headers={'Authorization': '%s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)

    @task
    def create_delete_list(self):
        """
        """
        response = self.client.post("/lists", data=json.dumps({'title': 'test', 'description': 'test'}), headers={'Authorization': '%s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)
        data = json.loads(response.content)
        self.client.delete("/lists/%s" % data[0]["ID"], headers={'Authorization': '%s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)

    @task
    def assign_unassign(self):
        """
        """
        response = self.client.put("/task/%s/users" % self.TASK_ID, data=json.dumps([self.USER_ID]), headers={'Authorization': '%s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)
        response = self.client.put("/task/%s/users" % self.TASK_ID, data=json.dumps([]), headers={'Authorization': '%s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)

    @task
    def update(self):
        """
        """
        self.client.put("/lists/%s" % self.LIST_ID, data=json.dumps({'title': str(uuid.uuid4()), 'description': 'test'}), headers={'Authorization': '%s' % self.AUTH, 'X-Nuage-Organization':'csp'}, verify=False)


class WebsiteUser(HttpLocust):
    """
    """
    task_set = UserBehavior
    min_wait=5
    max_wait=10