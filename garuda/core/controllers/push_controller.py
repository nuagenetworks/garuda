# -*- coding: utf-8 -*-

import gevent
import json
import redis
import logging

logger = logging.getLogger('garuda.pushcontroller')

from Queue import Queue

from garuda.core.models import GAPushEvent, GAResource, GARequest, GAContext
from garuda.core.config import GAConfig

from .operations_manager import GAOperationsManager


class GAPushController(object):
    """

    """
    def __init__(self, core_controller):
        """
        """
        self.core_controller = core_controller
        self._redis = redis.StrictRedis(host=GAConfig.REDIS_HOST, port=GAConfig.REDIS_PORT, db=GAConfig.REDIS_DB)
        self._queues = dict()
        self._thread = None

    def start(self):
        """
        """
        logger.debug('Starting listening Redis pubsub')

        p = self._redis.pubsub()
        p.subscribe(**{'event:new': self.receive_event})

        self._thread = p.run_in_thread(sleep_time=0.001)

    def flush(self, garuda_uuid):
        """
        """
        self.core_controller.sessions_manager.flush_garuda(garuda_uuid)

    def stop(self):
        """
        """
        if self._thread:
            self._thread.stop()

    def receive_event(self, content):
        """
        """
        data = json.loads(content['data'])
        logger.info('Receives message:\n%s' % json.dumps(data, indent=4))

        garuda_uuid = data['garuda_uuid']
        events = [GAPushEvent.from_dict(event) for event in data['events']]

        session_uuids = self.core_controller.sessions_manager.get_all(garuda_uuid=garuda_uuid, listening=True)

        jobs = []
        for session_uuid in session_uuids:
            jobs.append(gevent.spawn(self._send_events, session_uuid=session_uuid, events=events))

        gevent.joinall(jobs)

    def _send_events(self, session_uuid, events):
        """
        """
        if session_uuid not in self._queues:
            return

        events_to_send = []
        queue = self._queues[session_uuid]
        session = self.core_controller.sessions_manager.get(session_uuid=session_uuid)

        for event in events:
            entity = event.entity
            resources = [GAResource(name=entity.rest_name, value=entity.id)]
            request = GARequest(action=GARequest.ACTION_READ, resources=resources)
            context = GAContext(request=request, session=session)
            context.object = entity

            operation_manager = GAOperationsManager(context=context, model_controller=self.core_controller.model_controller)
            operation_manager.run()

            if not context.has_errors():
                event.entity = context.object
                events_to_send.append(event)

        logger.debug('Sending events to REST Communication Channel %s' % events_to_send)
        queue.put(events_to_send)

    def add_events(self, events):
        """
        """
        data = dict()
        data['garuda_uuid'] = self.core_controller.uuid
        data['events'] = [event.to_dict() for event in events]
        self._redis.publish('event:new', json.dumps(data))

    def get_queue_for_session(self, session_uuid):
        """
        """
        session_uuid = "sessions:%s" % session_uuid

        if session_uuid not in self._queues:
            logger.debug('Creating queue for %s' % session_uuid)
            self._queues[session_uuid] = Queue()

        return self._queues[session_uuid]
