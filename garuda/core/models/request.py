# -*- coding: utf-8 -*-

from uuid import uuid4


class GARequest(object):
    """

    """
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_READ = 'read'
    ACTION_READALL = 'readall'
    ACTION_ASSIGN = 'assign'
    ACTION_AUTHENTICATE = 'authenticate'
    ACTION_LISTENEVENTS = 'listen events'

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

