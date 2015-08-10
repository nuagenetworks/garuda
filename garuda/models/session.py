# -*- coding: utf-8 -*-

from uuid import uuid4


class GASession(object):
    """

    """

    def __init__(self, user=None, user_info={}, resources=[]):
        """

        """
        self.uuid = uuid4().hex
        self.user = user
        self.user_info = user_info
        self.resources = resources
