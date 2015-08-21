# -*- coding: utf-8 -*-

from uuid import uuid4
from datetime import datetime, timedelta

from garuda.config import GAConfig


class GAUser(object):
    """

    """

    def __init__(self, user=None, user_info={}):
        """

        """
        self.username = 'Christophe'
        self.password = 'Serafin'

    def to_dict(self):
        """
        """

        to_dict = dict()

        to_dict['username'] = self.username
        to_dict['password'] = self.password

        return to_dict

    @classmethod
    def from_dict(cls, a_dict):
        ""
        ""
        instance = cls()
        instance.username = a_dict['username']
        instance.password = a_dict['password']

        return instance
