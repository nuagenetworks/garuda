# -*- coding: utf-8 -*-

import redis
import json

from .authentication_controller import AuthenticationController

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
        if uuid is None:
            return None

        stored_session = self._redis.get(uuid)

        if stored_session is None:
            return None

        session = GASession.from_dict(json.loads(stored_session))

        if session.has_expired():
            return None

        # TODO: Use redis expiration date here
        session.renew()

        self._redis.set(session.uuid, json.dumps(session.to_dict()))

        return session

    def create_session(self, request, models_controller):
        """
        """
        session = GASession()

        authentication_controller = AuthenticationController()

        user = authentication_controller.authenticate(request=request, models_controller=models_controller)

        if user is None or user.api_key is None:
            return None

        session.user_info['APIKey'] = user.api_key
        user.api_key = session.uuid
        session.user = user

        self._redis.set(session.uuid, json.dumps(session.to_dict()))
        return session

    def flush(self):
        """
        """
        self._redis.flushdb()
