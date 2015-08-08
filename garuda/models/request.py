# -*- coding: utf-8 -*-


class GARequest(object):
    """

    """
    def __init__(self, action, url, data={}, resources=[], headers={}, cookies=None):
        """
        """
        self.action = action
        self.url = url
        self.data = data
        self.headers = headers
        self.cookies = cookies
        self.resources = resources
