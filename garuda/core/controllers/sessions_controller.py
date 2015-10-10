# -*- coding: utf-8 -*-

import logging
logging.getLogger

logger = logging.getLogger('garuda.controller.sessions')

import redis

from garuda.core.controllers.abstracts import GAPluginController
from garuda.core.plugins import GAAuthenticationPlugin
from garuda.core.models import GASession
from garuda.core.config import GAConfig

REDIS_ALL_KEY = '*'
REDIS_LISTENING_KEY = 'sessions:listen-for-push'
REDIS_SESSION_KEY = 'sessions:'
REDIS_GARUDA_KEY = 'garuda:'

REDIS_SESSION_TTL = 3600


class GASessionsController(GAPluginController):
    """
    """
    def __init__(self, plugins, core_controller):
        """

        """
        super(GASessionsController, self).__init__(plugins=plugins, core_controller=core_controller)
        self._redis = redis.StrictRedis(host=GAConfig.REDIS_HOST, port=GAConfig.REDIS_PORT, db=GAConfig.REDIS_DB)

    def register_plugin(self, plugin):
        """
        """
        super(GASessionsController, self).register_plugin(plugin=plugin, plugin_type=GAAuthenticationPlugin)


    def send_event(self, event, content):
        """
        """
        self._redis.publish(event, content)

    def save(self, session):
        """
        """
        logger.debug('Saving session uuid=%s for garuda_uuid=%s' % (session.uuid, session.garuda_uuid))
        self._redis.expire(session.uuid, REDIS_SESSION_TTL)

        if session.is_listening_push_notifications:
            logger.debug('Session is listening for push notification')
            self._redis.sadd(REDIS_LISTENING_KEY, REDIS_SESSION_KEY + session.uuid)

        self._redis.sadd(REDIS_GARUDA_KEY + session.garuda_uuid, REDIS_SESSION_KEY + session.uuid)

        return self._redis.hmset(REDIS_SESSION_KEY + session.uuid, session.to_hash())

    def get_all_sessions(self, garuda_uuid=None, listening=None):
        """
        """
        if garuda_uuid is None:
            logger.debug('Get all sessions stored in redis')
            return self._redis.keys("sessions*")

        garuda_key = REDIS_GARUDA_KEY + garuda_uuid

        if listening is None:
            logger.debug('Get all sessions for garuda_uuid=%s' % garuda_uuid)
            return self._redis.smembers(garuda_key)

        if listening is True:
            logger.debug('Get all sessions listening for push notification and for garuda_uuid=%s' % garuda_uuid)
            return self._redis.sinter(garuda_key, REDIS_LISTENING_KEY)

        return self._redis.sdiff(garuda_key, REDIS_LISTENING_KEY)

    def get_session(self, session_uuid):
        """
        """

        logger.debug('Get session with uuid=%s' % session_uuid)
        if session_uuid is None:
            return None

        session_hash = self._redis.hgetall(REDIS_SESSION_KEY + session_uuid)

        if session_hash is None or len(session_hash) == 0:
            logger.debug('No session found')
            return None

        logger.debug('Session found with uuid=%s' % session_uuid)
        session = GASession.from_hash(session_hash)

        self.save(session)

        return session

    def _plugin_for_request(self, request):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(request):
                return plugin
        return None

    def get_session_identifier(self, request):
        """
        """
        plugin = self._plugin_for_request(request)
        return plugin.get_session_identifier(request) if plugin else None

    def create_session(self, request, garuda_uuid):
        """
        """
        logger.debug('Creating session for garuda_uuid=%s' % garuda_uuid)
        session = GASession(garuda_uuid=garuda_uuid)
        plugin = self._plugin_for_request(request)

        root_object = plugin.authenticate(request=request, session=session)

        if not root_object:
            return None

        session.root_object = root_object
        self.save(session)

        return session

    def flush_garuda(self, garuda_uuid):
        """
        """
        logger.debug('Flushing Garuda Sessions')
        garuda_key = REDIS_GARUDA_KEY + garuda_uuid

        session_keys = self.get_all_sessions(garuda_uuid=garuda_uuid)

        if len(session_keys) == 0:
            return

        self._redis.delete(*session_keys)
        self._redis.srem(garuda_key, *session_keys)
        self._redis.srem(REDIS_LISTENING_KEY, *session_keys)

    def flush_database(self):
        """
        """
        self._redis.flushdb()
