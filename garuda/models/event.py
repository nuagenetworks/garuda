# -*- coding: utf-8 -*-

from uuid import uuid4
from datetime import datetime

from garuda.config import GAConfig
from .abstracts import GASerializable

class GAEvent(GASerializable):
    """

    """
    def __init__(self, garuda_uuid, action=None, content=[]):
        """
        """
        GASerializable.__init__(self)

        self.action = action
        self.content = content
        self.creation_date = datetime.now()
        self._garuda_uuid = garuda_uuid
        self._uuid = str(uuid4())

        self.register_attribute(type=str, internal_name='action')
        self.register_attribute(type=dict, internal_name='content')
        self.register_attribute(type=datetime, internal_name='creation_date')
        self.register_attribute(type=str, internal_name='_garuda_uuid')
        self.register_attribute(type=str, internal_name='_uuid')

    @property
    def uuid(self):
        """
        """
        return self._uuid

    @property
    def garuda_uuid(self):
        """
        """
        return self._garuda_uuid