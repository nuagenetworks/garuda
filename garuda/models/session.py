# -*- coding: utf-8 -*-

from uuid import uuid4
from datetime import datetime, timedelta


class GASession(object):
    """

    """

    HOUR_TO_LIVE = 1

    def __init__(self, user=None, user_info={}):
        """

        """
        self._uuid = uuid4().hex
        self._expiration_date = None
        self.user = user
        self.user_info = user_info

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
