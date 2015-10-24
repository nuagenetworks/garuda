# -*- coding: utf-8 -*-

import logging
from uuid import uuid4
import json

from garuda.core.lib import ThreadManager

logger = logging.getLogger('garuda.controller')

class GAController(object):
    """
    """
    def __init__(self, core_controller, redis_conn=None):
        """
        """

        if not core_controller:
            raise Exception("core_controller must be given to all GAController subclasses")

        self._core_controller = core_controller
        self._redis           = redis_conn
        self._uuid            = str(uuid4())

        if self._redis:
            self._pubsub          = self._redis.pubsub()
            self._pubsub_thread   = None
            self._subscriptions   = {}

    @classmethod
    def identifier(cls):
        """
        """
        raise NotImplementedError("identifier class method must be implemented")

    @property
    def core_controller(self):
        """
        """
        return self._core_controller

    @property
    def redis(self):
        """
        """
        return self._redis

    @property
    def uuid(self):
        """
        """
        return self._uuid

    def ready(self):
        """
        """
        pass

    def start(self):
        """
        """
        pass

    def stop(self):
        """
        """
        pass

    # messaging

    def subscribe(self, channel, handler):
        """
        """
        self._subscriptions[channel] = handler

    def unsubscribe(self, channel):
        """
        """
        if channel in self._subscriptions:
            del self._subscriptions[channel]

        self._pubsub.unsubscribe(channel)

    def unsubscribe_all(self):
        """
        """
        self._pubsub.unsubscribe()

    def publish(self, channel, data):
        """
        """
        self.redis.publish(channel, json.dumps(data))

    def start_listening_to_events(self):
        """
        """
        for channel in self._subscriptions:
            self._pubsub.subscribe(channel)

        self._pubsub_thread = ThreadManager.start_thread(self._listen_to_redis_events)

    def stop_listening_to_events(self):
        """
        """
        if not self._pubsub_thread:
            return

        ThreadManager.stop_thread(self._pubsub_thread)
        self._pubsub_thread = None

    def _listen_to_redis_events(self):
        """
        """
        for event in self._pubsub.listen():

            if event['type'] in ('subscribe', 'unsubscribe'):
                continue

            channel = event['channel']

            if channel in self._subscriptions:
                handler = self._subscriptions[channel]
                handler(event['data'])



