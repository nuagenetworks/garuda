# -*- coding: utf-8 -*-

from uuid import uuid4
from datetime import datetime

from garuda.config import GAConfig


class GAPushNotification(object):
    """

    """
    def __init__(self, action=None, entities=[]):
        """
        """
        self.action = action
        self.creation_date = datetime.now()
        self.entities = entities
        self._uuid = str(uuid4())

    @property
    def uuid(self):
        """
        """
        return self._uuid

    def to_dict(self):
        """
        """

        to_dict = dict()

        to_dict['action'] = self.action
        to_dict['creation_date'] = self.creation_date.strftime(GAConfig.DATE_FORMAT)
        to_dict['entities'] = self.entities
        to_dict['uuid'] = self.uuid

        return to_dict

    @classmethod
    def from_dict(cls, a_dict):
        """
        """
        instance = cls()

        instance._uuid = a_dict['uuid']
        instance.action = a_dict['action']
        instance.entities = a_dict['entities']
        instance.creation_date = datetime.strptime(a_dict['creation_date'], GAConfig.DATE_FORMAT)

        return instance
