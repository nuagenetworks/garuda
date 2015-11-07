# -*- coding: utf-8 -*-

import logging
from uuid import uuid4

from garuda.core.lib import ThreadManager

logger = logging.getLogger('garuda.controller')


class GAController(object):
    """
    """
    def __init__(self, core_controller):
        """
        """

        if not core_controller:
            raise RuntimeError("a valid core_controller must be given to all GAController subclasses")

        self._core_controller = core_controller
        self._uuid = str(uuid4())

        if self.redis:
            self._pubsub = self.redis.pubsub()
            self._pubsub_thread = None
            self._subscriptions = {}

    @classmethod
    def identifier(cls):  # pragma: no cover
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
        return self.core_controller.redis

    @property
    def redis_host(self):
        """
        """
        return self.core_controller.redis_host

    @property
    def redis_port(self):
        """
        """
        return self.core_controller.redis_port

    @property
    def redis_db(self):
        """
        """
        return self.core_controller.redis_db

    @property
    def uuid(self):
        """
        """
        return self._uuid

    @property
    def subscriptions(self):
        """
        """
        return self._subscriptions

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

        if self._pubsub_thread:
            self._pubsub.subscribe(channel)

    def unsubscribe(self, channel):
        """
        """
        if channel in self._subscriptions:
            del self._subscriptions[channel]

        if self._pubsub_thread:
            self._pubsub.unsubscribe(channel)

    def unsubscribe_all(self):
        """
        """
        self._subscriptions = {}

        if self._pubsub_thread:
            self._pubsub.unsubscribe()

    def publish(self, channel, data):
        """
        """
        self.redis.publish(channel, data)

    def start_listening_to_events(self):
        """
        """
        if self._pubsub_thread:
            return

        for channel in self._subscriptions:
            self._pubsub.subscribe(channel)

        self._pubsub_thread = ThreadManager.start_thread(self._listen_to_redis_events)

    def stop_listening_to_events(self):
        """
        """
        if not self._pubsub_thread:
            return

        self._pubsub.unsubscribe()
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
