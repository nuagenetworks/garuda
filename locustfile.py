# -*- coding: utf8 -*-

from locust import HttpLocust, TaskSet, task

## TODO: remove this at some point. this is the SSL ugly patch
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

## Monkey patch to use PROTOCOL_TLSv1 by default in requests
from functools import wraps
def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar

PoolManager.__init__ = sslwrap(PoolManager.__init__)
## end of monkey patch



class UserBehavior(TaskSet):
    """
    """
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass


    # @task
    # def enterprises(self):
    #     """
    #     """
    #     self.client.get("/enterprises", headers={'Authorization': 'XREST Y3Nwcm9vdDo5ODIwY2ZlMi01ODFmLTQxZGItYmM5OC0wZDNkMDJmYWM5MDM=', 'X-Nuage-Organization':'csp'}, verify=False)
    #
    # @task
    # def subnets(self):
    #     """
    #     """
    #     self.client.get("/subnets", headers={'Authorization': 'XREST Y3Nwcm9vdDo5ODIwY2ZlMi01ODFmLTQxZGItYmM5OC0wZDNkMDJmYWM5MDM=', 'X-Nuage-Organization':'csp'}, verify=False)
    #
    # @task
    # def domain(self):
    #     """
    #     """
    #     self.client.get("/enterprises/b554017b-8f51-4a39-8139-08a3d7f01951/domains", headers={'Authorization': 'XREST Y3Nwcm9vdDo5ODIwY2ZlMi01ODFmLTQxZGItYmM5OC0wZDNkMDJmYWM5MDM=', 'X-Nuage-Organization':'csp'}, verify=False)

    @task
    def vspkonly(self):
        """
        """
        self.client.get("/vspkonly", headers={'Authorization': 'XREST Y3Nwcm9vdDo5ODIwY2ZlMi01ODFmLTQxZGItYmM5OC0wZDNkMDJmYWM5MDM=', 'X-Nuage-Organization':'csp'}, verify=False)

class WebsiteUser(HttpLocust):
    """
    """
    task_set = UserBehavior
    min_wait=1000
    max_wait=1500