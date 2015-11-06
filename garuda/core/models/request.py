# -*- coding: utf-8 -*-

from uuid import uuid4


class GARequest(object):
    """

    """
    ACTION_CREATE = 'CREATE'
    ACTION_UPDATE = 'UPDATE'
    ACTION_DELETE = 'DELETE'
    ACTION_READ = 'READ'
    ACTION_READALL = 'READ_ALL'
    ACTION_ASSIGN = 'ASSIGN'
    ACTION_COUNT = 'COUNT'
    ACTION_LISTENEVENTS = 'LISTEN'

    def __init__(self, action, channel=None, content={}, resources=[], username=None, token=None, cookies=None, filter=None, order_by=None, page=None, page_size=None, parameters={}):
        """
        """
        self._uuid = str(uuid4())
        self.action = action
        self.content = content
        self.parameters = parameters
        self.cookies = cookies
        self.resources = resources
        self.channel = channel
        self.username = username
        self.token = token
        self.filter = filter
        self.order_by = order_by
        self.page = page
        self.page_size = page_size

    @property
    def uuid(self):
        """
        """
        return self._uuid
