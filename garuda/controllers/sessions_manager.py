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

    def _publish(self, event, content):
        """
        """
        self._redis.publish(event, content)

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

        self.save(session)

        return session

    def create_session(self, request, models_controller, garuda_uuid):
        """
        """
        session = GASession(garuda_uuid=garuda_uuid)

        authentication_controller = AuthenticationController()

        user = authentication_controller.authenticate(request=request, models_controller=models_controller)

        if user is None or user.api_key is None:
            return None

        session.user_info['APIKey'] = user.api_key
        user.api_key = session.uuid
        session.user = GAUser(api_key=user.api_key, username=user.user_name, id=user.id, email=user.email, firstname=user.first_name, lastname=user.last_name)

        self.save(session)
        return session

    def save(self, session):
        """
        """
        # TODO: Use redis expiration date here
        session.renew()

        return self._redis.set(session.uuid, json.dumps(session.to_dict()))

    def flush(self):
        """
        """
        self._redis.flushdb()
