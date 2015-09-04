# -*- coding: utf-8 -*-

from uuid import uuid4
from datetime import datetime

from garuda.core.config import GAConfig
from .abstracts import GASerializable


class GAPushNotification(GASerializable):
    """

    """
    def __init__(self, action=None, entities=[]):
        """
        """
        GASerializable.__init__(self)

        self.action = action
        self.creation_date = datetime.now()
        self.entities = entities
        self._uuid = str(uuid4())

        self.register_attribute(type=str, internal_name='action')
        self.register_attribute(type=list, internal_name='entities')
        self.register_attribute(type=datetime, internal_name='creation_date')
        self.register_attribute(type=str, internal_name='_uuid')

    @property
    def uuid(self):
        """
        """
        return self._uuid
