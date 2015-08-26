# -*- coding: utf-8 -*-

from uuid import uuid4
from datetime import datetime, timedelta

from garuda.config import GAConfig

from .user import GAUser


class GASession(object):
    """

    """

    HOUR_TO_LIVE = 1

    def __init__(self, garuda_uuid, user=None, user_info={}):
        """

        """
        self._uuid = str(uuid4())
        self._garuda_uuid = garuda_uuid
        self._expiration_date = None
        self.user = user
        self.user_info = user_info
        self.is_listening_push_notifications = False

        self.renew()

    @property
    def uuid(self):
        """
        """
        return self._uuid

    @property
    def expiration_date(self):
        """
        """
        return self._expiration_date

    def renew(self):
        """
        """
        self._expiration_date = datetime.today() + timedelta(hours=GASession.HOUR_TO_LIVE)

    def has_expired(self):
        """
        """
        return datetime.today() > self._expiration_date

    def to_dict(self):
        """
        """

        to_dict = dict()

        to_dict['uuid'] = self._uuid
        to_dict['garuda_uuid'] = self._garuda_uuid
        to_dict['expiration_date'] = self._expiration_date.strftime(GAConfig.DATE_FORMAT)
        to_dict['user'] = self.user.to_dict()
        to_dict['user_info'] = self.user_info
        to_dict['is_listening_push_notifications'] = self.is_listening_push_notifications

        return to_dict

    @classmethod
    def from_dict(cls, a_dict):
        ""
        ""
        instance = cls(garuda_uuid=a_dict['garuda_uuid'])
        instance._uuid = a_dict['uuid']
        instance._expiration_date = datetime.strptime(a_dict['expiration_date'], GAConfig.DATE_FORMAT)
        instance.user = GAUser.from_dict(a_dict['user'])
        instance.user_info = a_dict['user_info']
        instance.is_listening_push_notifications = a_dict['is_listening_push_notifications']

        return instance
