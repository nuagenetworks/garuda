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
    ACTION_LISTENEVENTS = 'LISTEN'

    def __init__(self, action, channel=None, content={}, resources=[], parameters={}, cookies=None):
        """
        """
        self._uuid = str(uuid4())
        self.action = action
        self.content = content
        self.parameters = parameters
        self.cookies = cookies
        self.resources = resources
        self.channel = channel

    @property
    def uuid(self):
        """
        """
        return self._uuid

