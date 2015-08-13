# -*- coding: utf-8 -*-

from garuda.models import GASession


class SessionsManager(object):
    """
    """
    def __init__(self):
        """

        """
        self._sessions = {}

    def get_session(self, uuid=None):
        """
        """
        if uuid is None or uuid not in self._sessions:
            session = GASession()
            self._sessions[session.uuid] = session

        else:
            session = self._sessions[uuid]

            if session.has_expired():
                session.renew()

        return session
