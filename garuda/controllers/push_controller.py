# -*- coding: utf-8 -*-

import json
import redis

from Queue import Queue

from garuda.models import GAPushNotification
from garuda.config import GAConfig


class PushController(object):
    """

    """
    def __init__(self):
        """
        """
        self._redis = redis.StrictRedis(host=GAConfig.REDIS_HOST, port=GAConfig.REDIS_PORT, db=GAConfig.REDIS_DB)
        self._queues = dict()
        self._thread = None

    def start(self):
        """
        """
        p = self._redis.pubsub()
        p.subscribe(**{'garuda-new-event': self.receive_events})

        print 'starting push controller %s' % self._redis

        self._thread = p.run_in_thread(sleep_time=0.001)

    def stop(self):
        """
        """
        print 'stoping push controller %s' % self

        if self._thread:
            self._thread.stop()
            self._thread = None

    def receive_events(self, message):
        """
        """
        print 'Receiving notification...'
        print message

    def add_notification(self, uuid, action, entities):
        """
        """
        notification = GAPushNotification(action=action, entities=entities)
        data = dict()
        data['uuid'] = uuid  # Garuda uuid
        data['content'] = notification.to_dict()
        self._redis.publish('garuda-new-event', json.dumps(data))

    def get_queue_for_session(self, session_uuid):
        """
        """
        print 'Get queue to %s ' % session_uuid

        if session_uuid not in self._queues:
            print 'Creating queue'
            self._queues[session_uuid] = Queue()

        return self._queues[session_uuid]
