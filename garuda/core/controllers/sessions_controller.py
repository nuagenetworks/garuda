# -*- coding: utf-8 -*-

import logging
import redis

from garuda.core.controllers.abstracts import GAPluginController
from garuda.core.plugins import GAAuthenticationPlugin
from garuda.core.models import GASession

logging.getLogger
logger = logging.getLogger('garuda.controller.sessions')


REDIS_ALL_KEY = '*'
REDIS_LISTENING_KEY = 'sessions:listen-for-push'
REDIS_SESSION_KEY = 'sessions:'
REDIS_GARUDA_KEY = 'garuda:'
REDIS_SESSION_TTL = 600


class GASessionsController(GAPluginController):
    """
    """
    def __init__(self, plugins, core_controller, redis_conn):
        """

        """
        super(GASessionsController, self).__init__(plugins=plugins, core_controller=core_controller)
        self._redis = redis_conn
        self.garuda_uuid = self.core_controller.uuid

    @property
    def garuda_redis_key(self):
        """
        """
        return '%s-%s' % (REDIS_GARUDA_KEY, self.garuda_uuid)

    def register_plugin(self, plugin):
        """
        """
        super(GASessionsController, self).register_plugin(plugin=plugin, plugin_type=GAAuthenticationPlugin)

    def save(self, session):
        """
        """
        logger.debug('Saving session uuid=%s for garuda_uuid=%s' % (session.uuid, session.garuda_uuid))

        if session.is_listening_push_notifications:
            logger.debug('Session is listening for push notification')
            self._redis.sadd(REDIS_LISTENING_KEY, REDIS_SESSION_KEY + session.uuid)

        self._redis.sadd(self.garuda_redis_key, REDIS_SESSION_KEY + session.uuid)
        self._redis.expire(REDIS_SESSION_KEY + session.uuid, REDIS_SESSION_TTL)

        return self._redis.hmset(REDIS_SESSION_KEY + session.uuid, session.to_hash())

    def get_all_local_sessions(self, listening=None):
        """
        """
        session_keys = self._get_all_local_session_keys(listening=listening)
        return [self._get_session_from_key(key) for key in session_keys]

    def get_session(self, session_uuid):
        """
        """
        return self._get_session_from_key(REDIS_SESSION_KEY + session_uuid)

    def create_session(self, request):
        """
        """
        logger.debug('Creating session for garuda_uuid=%s' % self.garuda_uuid)
        session = GASession(garuda_uuid=self.garuda_uuid)
        plugin = self._plugin_for_request(request)

        if plugin is None:
            logger.warn('No plugin found to create session')
            return None

        root_object = plugin.authenticate(request=request, session=session)

        if not root_object:
            return None

        session.root_object = root_object
        self.save(session)

        return session

    def flush_local_sessions(self):
        """
        """
        logger.debug('Flushing Local Garuda Sessions')

        session_keys = self._get_all_local_session_keys()

        if len(session_keys) == 0:
            return

        self._redis.delete(*session_keys)
        self._redis.srem(self.garuda_redis_key, *session_keys)
        self._redis.srem(REDIS_LISTENING_KEY, *session_keys)

    ## Utilties

    def _get_session_from_key(self, session_key):
        """
        """
        session_hash = self._redis.hgetall(session_key)

        if not session_hash or not len(session_hash):
            return None

        return GASession.from_hash(session_hash)

    def _get_all_local_session_keys(self, listening=False):
        """
        """
        if listening:
            logger.debug('Get all listening sessions for garuda_uuid=%s' % self.garuda_uuid)
            return self._redis.sinter(self.garuda_redis_key, REDIS_LISTENING_KEY)
        else:
            logger.debug('Get all sessions for garuda_uuid=%s' % self.garuda_uuid)
            return self._redis.sdiff(self.garuda_redis_key, REDIS_LISTENING_KEY)

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