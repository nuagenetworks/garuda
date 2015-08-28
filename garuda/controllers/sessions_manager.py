# -*- coding: utf-8 -*-

import redis

from .authentication_controller import AuthenticationController

from garuda.models import GASession, GAUser
from garuda.config import GAConfig

REDIS_ALL_KEY = '*'
REDIS_LISTENING_KEY = 'sessions-listenning'
REDIS_GARUDA_KEY = 'sessions-for-garuda-'

REDIS_SESSION_TTL = 3600


class SessionsManager(object):
    """
    """
    def __init__(self):
        """

        """
        self._redis = redis.StrictRedis(host=GAConfig.REDIS_HOST, port=GAConfig.REDIS_PORT, db=GAConfig.REDIS_DB)

    def send_event(self, event, content):
        """
        """
        self._redis.publish(event, content)

    def save(self, session):
        """
        """
        self._redis.expire(session.uuid, REDIS_SESSION_TTL)

        if session.is_listening_push_notifications:
            self._redis.sadd(REDIS_LISTENING_KEY, session.uuid)

        self._redis.sadd(REDIS_GARUDA_KEY + session.garuda_uuid, session.uuid)

        return self._redis.hmset(session.uuid, session.to_hash())

    def get_all(self, garuda_uuid=None, listening=None):
        """
        """
        if garuda_uuid is None:
            return self._redis.keys(REDIS_ALL_KEY)

        garuda_key = REDIS_GARUDA_KEY + garuda_uuid

        if listening is None:
            return self._redis.smembers(garuda_key)

        if listening is True:
            return self._redis.sinter(garuda_key, REDIS_LISTENING_KEY)

        return self._redis.sdiff(garuda_key, REDIS_LISTENING_KEY)

    def get(self, session_uuid):
        """
        """

        if session_uuid is None:
            return None

        session_hash = self._redis.hgetall(session_uuid)

        if session_hash is None or len(session_hash) == 0:
            return None

        session = GASession.from_hash(session_hash)

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

    def flush_garuda(self, garuda_uuid):
        """
        """
        garuda_key = REDIS_GARUDA_KEY + garuda_uuid

        session_uuids = self.get_all(garuda_uuid=garuda_uuid)

        if len(session_uuids) == 0:
            return

        self._redis.delete(*session_uuids)
        self._redis.srem(garuda_key, *session_uuids)
        self._redis.srem(REDIS_LISTENING_KEY, *session_uuids)

    def flush(self):
        """
        """
        self._redis.flushdb()
