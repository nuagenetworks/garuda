# -*- coding: utf-8 -*-

from uuid import uuid4
from .abstracts import GASerializable


class GAPushNotification(GASerializable):
    """

    """

    def __init__(self, events=[]):
        """
        """
        GASerializable.__init__(self)

        self.events = events
        self._uuid = str(uuid4())

        self.register_attribute(type=list, internal_name='events')
        self.register_attribute(type=str, internal_name='_uuid')

    @property
    def uuid(self):
        """
        """
        return self._uuid
