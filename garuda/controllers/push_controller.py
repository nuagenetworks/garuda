# -*- coding: utf-8 -*-

import json
import redis
import logging

logger = logging.getLogger('Garuda.RESTCommunicationChannel')

from Queue import Queue

from garuda.models import GAPushNotification
from garuda.config import GAConfig

from .sessions_manager import SessionsManager


class PushController(object):
    """

    """
    def __init__(self):
        """
        """
        self._redis = redis.StrictRedis(host=GAConfig.REDIS_HOST, port=GAConfig.REDIS_PORT, db=GAConfig.REDIS_DB)
        self._queues = dict()
        self._thread = None
        self._session_manager = SessionsManager()

    def start(self):
        """
        """
        logger.debug('Starting listening Redis pubsub')

        p = self._redis.pubsub()
        p.subscribe(**{'garuda-new-event': self.receive_events})

        self._thread = p.run_in_thread(sleep_time=0.001)

    def flush(self, garuda_uuid):
        """
        """
        self._session_manager.flush_garuda(garuda_uuid)

    def stop(self):
        """
        """
        if self._thread:
            self._thread.stop()
            self._thread = None

    def receive_events(self, message):
        """
        """
        print 'Receiving notification...'
        data = json.loads(message['data'])
        garuda_uuid = data['garuda_uuid']
        notification = GAPushNotification.from_dict(data['content'])

        session_uuids = self._session_manager.get_all(garuda_uuid=garuda_uuid, listening=True)

        for session_uuid in session_uuids:
            if session_uuid not in self._queues:
                continue

            queue = self._queues[session_uuid]
            queue.put(notification)

    def add_notification(self, garuda_uuid, action, entities):
        """
        """
        notification = GAPushNotification(action=action, entities=entities)
        data = dict()
        data['garuda_uuid'] = garuda_uuid
        data['content'] = notification.to_dict()
        self._redis.publish('garuda-new-event', json.dumps(data))

    def get_queue_for_session(self, session_uuid):
        """
        """
        if session_uuid not in self._queues:
            self._queues[session_uuid] = Queue()

        return self._queues[session_uuid]
