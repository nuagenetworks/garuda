# -*- coding: utf-8 -*-

import json
import redis
import logging
import time
from Queue import Queue


from garuda.core.models import GAPushEvent, GAPushEventDrainer, GAResource, GARequest, GAContext
from garuda.core.lib import ThreadManager
from .operations_controller import GAOperationsController

logger = logging.getLogger('garuda.controller.push')


class GAPushController(object):
    """

    """
    def __init__(self, core_controller, redis_conn):
        """
        """
        self.core_controller = core_controller
        self._redis = redis_conn
        self._queues = dict()
        self._thread = None
        self._thread_manager = ThreadManager()

    def start(self):
        """
        """
        logger.debug('Starting listening Redis pubsub')

        p = self._redis.pubsub()
        p.subscribe(**{'event:new': self._on_redis_event})

        self._thread = p.run_in_thread(sleep_time=0.01)

    def stop(self):
        """
        """
        if self._thread:
            self._thread.stop()

    def _on_redis_event(self, content):
        """
        """
        data = json.loads(content['data'])
        logger.debug('Receives redis push:\n%s' % json.dumps(data, indent=4))

        garuda_uuid = data['garuda_uuid']
        events = [GAPushEvent.from_dict(event) for event in data['events']]

        self._enqueue_events(garuda_uuid=garuda_uuid, events=events)

    def _enqueue_events(self, garuda_uuid, events):
        """
        """
        session_uuids = self.core_controller.sessions_controller.get_all_sessions(garuda_uuid=garuda_uuid, listening=True)

        for session_uuid in session_uuids:
            if session_uuid not in self._queues:
                continue

            self._thread_manager.start(method=self._perform_enqueue_events, elements=events, session_uuid=session_uuid)

    def _perform_enqueue_events(self, session_uuid, events):
        """
        """
        events_to_send = []
        queue = self._queues[session_uuid]
        session = self.core_controller.sessions_controller.get_session(session_uuid=session_uuid)

        for event in events:

            entity = event.entity
            resources = [GAResource(name=entity.rest_name, value=entity.id)]
            request = GARequest(action=GARequest.ACTION_READ, resources=resources)
            context = GAContext(request=request, session=session)
            context.object = entity

            operation_manager = GAOperationsController(context=context,logic_controller=self.core_controller.logic_controller, storage_controller=self.core_controller.storage_controller)
            operation_manager.run()

            if not context.has_errors():
                event.entity = context.object
                events_to_send.append(event)

        logger.debug('Enqueueing events for session %s' % session_uuid)
        queue.put(events_to_send)

    def push_events(self, events):
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

        return GAPushEventDrainer(self._queues[session_uuid])
