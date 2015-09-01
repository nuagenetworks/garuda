# -*- coding: utf-8 -*-

import json

from uuid import uuid4

from .user import GAUser
from .abstracts import GASerializable


class GASession(GASerializable):
    """

    """

    HOUR_TO_LIVE = 3600

    def __init__(self, garuda_uuid=None, user=None, user_info={}):
        """

        """
        GASerializable.__init__(self)

        self._uuid = str(uuid4())
        self._garuda_uuid = garuda_uuid
        self.user = user
        self.user_info = user_info
        self.is_listening_push_notifications = False


        self.register_attribute(type=str, internal_name='_uuid')
        self.register_attribute(type=str, internal_name='_garuda_uuid')
        self.register_attribute(type=GAUser, internal_name='user')
        self.register_attribute(type=dict, internal_name='user_info')
        self.register_attribute(type=bool, internal_name='is_listening_push_notifications')

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
