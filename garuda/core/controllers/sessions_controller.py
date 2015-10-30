# -*- coding: utf-8 -*-

import logging
import redis
import os
import msgpack

from garuda.core.models import GAPluginController
from garuda.core.plugins import GAAuthenticationPlugin
from garuda.core.models import GASession
from garuda.core.lib import ThreadManager

logging.getLogger
logger = logging.getLogger('garuda.controller.sessions')


class GASessionsController(GAPluginController):
    """
    """
    def __init__(self, plugins, core_controller, redis_conn):
        """

        """
        super(GASessionsController, self).__init__(plugins=plugins, core_controller=core_controller, redis_conn=redis_conn)

        self._garuda_uuid = self.core_controller.uuid
        self._default_session_ttl = 300
        self._local_sessions_redis_key = None
        self._local_listening_sessions_redis_key = None

        self.subscribe(channel='__keyevent@0__:expired', handler=self._on_session_expiration)

    @classmethod
    def identifier(cls):
        """
        """
        return 'garuda.controller.sessions'

    @classmethod
    def managed_plugin_type(cls):
        """
        """
        return GAAuthenticationPlugin

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

    def start(self):
        """
        """
        self.start_listening_to_events()

    def stop(self):
        """
        """
        self.stop_listening_to_events()
        self.flush_local_sessions()

    def get_all_local_sessions(self, listening=False):
        """
        """
        session_keys = self._get_all_session_keys(listening=listening, local_only=True)

        if not len(session_keys):
            return []

        return [self._get_session_from_key(key) for key in session_keys]

    def get_all_local_session_keys(self, listening=False):
        """
        """
        return self._get_all_session_keys(listening=listening, local_only=True)

    def get_all_sessions(self):
        """
        """
        session_keys = self._get_all_session_keys(local_only=False)

        if not len(session_keys):
            return []

        return [self._get_session_from_key(key) for key in session_keys]

    def get_all_session_keys(self):
        """
        """
        return self._get_all_session_keys(local_only=False)

    def get_session(self, session_uuid):
        """
        """
        return self._get_session_from_key('sessions:' + session_uuid)

    def create_session(self, request):
        """
        """
        logger.debug('Creating session for garuda_uuid=%s (ttl=%s)' % (self._garuda_uuid, self._default_session_ttl))
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

    def delete_session(self, session):
        """
        """
        logger.debug('Deleting session %s' % session.uuid)

        print ('Deleting session %s' % (session.redis_key))
        self.redis.delete(session.redis_key)

    def reset_session_ttl(self, session):
        """
        """
        logger.debug('Reseting ttl for session key  %s for in garuda set %s)' % (session.redis_key, self.local_sessions_redis_key))

        self.redis.persist(session.redis_key)
        self.redis.expire(session.redis_key, self._default_session_ttl)

    def set_session_listening_status(self, session, status):
        """
        """
        logger.debug('Set session key %s listening status: %s' % (session.redis_key, status))

        if status:
            self.redis.sadd(self.local_listening_sessions_redis_key, session.redis_key)
        else:
            self.redis.srem(self.local_listening_sessions_redis_key, session.redis_key)

        self.reset_session_ttl(session)

    def flush_local_sessions(self):
        """
        """
        logger.debug('Cleaning up local garuda session sets %s and %s' % (self.local_sessions_redis_key, self.local_listening_sessions_redis_key))

        self.redis.delete(self.local_sessions_redis_key)
        self.redis.delete(self.local_listening_sessions_redis_key)

    ## Utilties

    def _save_session(self, session):
        """
        """
        logger.debug('Saving session key  %s for in garuda set %s)' % (session.redis_key, self.local_sessions_redis_key))

        self.redis.hmset(session.redis_key, session.to_hash())
        self.redis.sadd(self.local_sessions_redis_key, session.redis_key)
        self.redis.expire(session.redis_key, self._default_session_ttl)

    def _on_session_expiration(self, data):
        """
        """
        session_key = data
        self.redis.srem(self.local_sessions_redis_key, session_key)
        self.redis.srem(self.local_listening_sessions_redis_key, session_key)

        self.core_controller.push_controller.delete_event_queue(session_key)

    def _get_session_from_key(self, session_key):
        """
        """
        session_data = self.redis.hgetall(session_key)

        if not session_data or not len(session_data):
            return None

        return GASession.from_hash(session_data)

    def _get_all_session_keys(self, listening=False, local_only=True):
        """
        """
        if local_only and listening:
            return self.redis.smembers(self.local_listening_sessions_redis_key)
        elif local_only and not listening:
            return self.redis.smembers(self.local_sessions_redis_key)
        else:
            return self.redis.keys('sessions:*')

    def _plugin_for_request(self, request):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(request):
                return plugin
        return None