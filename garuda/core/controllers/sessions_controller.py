# -*- coding: utf-8 -*-

import logging
import redis
import os

from garuda.core.controllers.abstracts import GAPluginController
from garuda.core.plugins import GAAuthenticationPlugin
from garuda.core.models import GASession
from garuda.core.lib import ThreadManager

logging.getLogger
logger = logging.getLogger('garuda.controller.sessions')

REDIS_SESSION_TTL = 600


class GASessionsController(GAPluginController):
    """
    """
    def __init__(self, plugins, core_controller, redis_conn):
        """

        """
        super(GASessionsController, self).__init__(plugins=plugins, core_controller=core_controller)
        self._redis = redis_conn
        self._garuda_uuid = self.core_controller.uuid
        self._pubsub = self._redis.pubsub()
        self._pubsub_thread = None
        self._local_sessions_redis_key = None
        self._local_listening_sessions_redis_key = None

    def register_plugin(self, plugin):
        """
        """
        super(GASessionsController, self).register_plugin(plugin=plugin, plugin_type=GAAuthenticationPlugin)

    def get_session_identifier(self, request):
        """
        """
        plugin = self._plugin_for_request(request)
        return plugin.get_session_identifier(request) if plugin else None

    @property
    def local_sessions_redis_key(self):
        """
        """
        if not self._local_sessions_redis_key:
            self._local_sessions_redis_key = 'gnode:%s-%s:sessions' % (self._garuda_uuid, os.getpid())

        return self._local_sessions_redis_key

    @property
    def local_listening_sessions_redis_key(self):
        """
        """
        if not self._local_listening_sessions_redis_key:
            self._local_listening_sessions_redis_key =  'gnode:%s-%s:sessions:listening' % (self._garuda_uuid, os.getpid())

        return self._local_listening_sessions_redis_key

    def subscribe(self):
        """
        """
        self._pubsub.psubscribe('__keyevent@0__:expired')
        self._pubsub_thread = ThreadManager.start_thread(self._listen_to_redis_event)

    def unsubscribe(self):
        """
        """
        self._pubsub.punsubscribe('__keyevent@0:expired')
        ThreadManager.stop_thread(self._pubsub_thread)

    def get_all_local_sessions(self, listening=None):
        """
        """
        session_keys = self._get_all_local_session_keys(listening=listening)
        return [self._get_session_from_key(key) for key in session_keys]

    def get_session(self, session_uuid):
        """
        """
        return self._get_session_from_key('sessions:' + session_uuid)

    def create_session(self, request):
        """
        """
        logger.debug('Creating session for garuda_uuid=%s' % self._garuda_uuid)
        session = GASession(garuda_uuid=self._garuda_uuid)
        plugin = self._plugin_for_request(request)

        if plugin is None:
            logger.warn('No plugin found to create session')
            return None

        root_object = plugin.authenticate(request=request, session=session)

        if not root_object:
            return None

        session.root_object = root_object
        self._save_session(session)

        return session

    def reset_session_ttl(self, session):
        """
        """
        self._save_session(session) # we might find something better

    def set_session_listening_status(self, session, status):
        """
        """
        logger.debug('Set session key %s listening status: %s' % (session.redis_key, status))
        session.is_listening_push_notifications = status

        if status:
            self._redis.sadd(self.local_listening_sessions_redis_key, session.redis_key)
        else:
            self._redis.srem(self.local_listening_sessions_redis_key, session.redis_key)

        self._save_session(session)

    def flush_local_sessions(self):
        """
        """
        logger.debug('Flushing garuda session %s' % self.local_sessions_redis_key)

        session_keys = self._get_all_local_session_keys()

        if len(session_keys) == 0:
            return

        self._redis.delete(*session_keys)
        self._redis.srem(self.local_sessions_redis_key, *session_keys)
        self._redis.srem(self.local_listening_sessions_redis_key, *session_keys)

    ## Utilties

    def _save_session(self, session):
        """
        """

        logger.debug('Saving session key  %s for in garuda set %s)' % (session.redis_key, self.local_sessions_redis_key))

        self._redis.hmset(session.redis_key, session.to_hash())
        self._redis.sadd(self.local_sessions_redis_key, session.redis_key)
        self._redis.expire(session.redis_key, REDIS_SESSION_TTL)

        if session.is_listening_push_notifications:
            self._redis.sadd(self.local_listening_sessions_redis_key, session.redis_key)


    def _listen_to_redis_event(self):
        """
        """
        for event in self._pubsub.listen():
            if not event['pattern']:
                continue

            session_key = event['data']
            self._redis.srem(self.local_sessions_redis_key, session_key)
            self._redis.srem(self.local_listening_sessions_redis_key, session_key)

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
            return self._redis.smembers(self.local_listening_sessions_redis_key)
        else:
            return self._redis.smembers(self.local_sessions_redis_key)

    def _plugin_for_request(self, request):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(request):
                return plugin
        return None