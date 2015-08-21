# -*- coding: utf-8 -*-

import redis
import json

from garuda.models import GASession, GAUser
from garuda.config import GAConfig


class SessionsManager(object):
    """
    """
    def __init__(self):
        """

        """
        self._redis = redis.StrictRedis(host=GAConfig.REDIS_HOST, port=GAConfig.REDIS_PORT, db=GAConfig.REDIS_DB)

    def get_session(self, uuid=None):
        """
        """
        stored_session = self._redis.get(uuid)

        if stored_session is None:
            session = GASession(user=GAUser())
        else:
            session = GASession.from_dict(json.loads(stored_session))

            if session.has_expired():
                session.renew()

        self._redis.set(session.uuid, json.dumps(session.to_dict()))

        return session

    def flush(self):
        """
        """
        self._redis.flushdb()
