# -*- coding: utf-8 -*-

from garuda.models import GASession


class SessionManager(object):
    """
    """

    _sessions = {}

    @classmethod
    def get_session(cls, uuid=None):
        """
        """

        if uuid is None or uuid not in cls._sessions:
            session = GASession()
            cls._sessions[session.uuid] = session

        else:
            session = cls._sessions[uuid]

            if session.has_expired():
                session.renew()

        return session
