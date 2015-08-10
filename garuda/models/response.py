# -*- coding: utf-8 -*-

from uuid import uuid4


class GAResponse(object):
    """

    """
    STATUS_SUCCESS = 'SUCCESS'

    def __init__(self, status, content, parameters={}):
        """
        """
        self.uuid = uuid4().hex
        self.status = status
        self.content = content
        self.parameters = parameters
