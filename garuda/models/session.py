# -*- coding: utf-8 -*-

from uuid import uuid4


class GASession(object):
    """

    """

    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_READ = 'read'
    ACTION_READALL = 'readall'

    def __init__(self, user=None, data={}, resources=[], action=None):
        """

        """
        self.uuid = uuid4().hex
        self.user = user
        self.data = data
        self.action = action
        self.resources = resources
