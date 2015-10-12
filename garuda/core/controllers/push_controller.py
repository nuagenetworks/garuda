# -*- coding: utf-8 -*-

import gevent
import json
import redis
import logging

logger = logging.getLogger('garuda.controller.push')

from Queue import Queue

from garuda.core.models import GAPushEvent, GAResource, GARequest, GAContext

from .operations_controller import GAOperationsController


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

    def start(self):
        """
        """
        logger.debug('Starting listening Redis pubsub')

        p = self._redis.pubsub()
        p.subscribe(**{'event:new': self.receive_event})

        self._thread = p.run_in_thread(sleep_time=1.0)

    def stop(self):
        """
        """
        self._send_events_to_garuda(garuda_uuid=self.core_controller.uuid, events=[GAPushEvent(action=self.core_controller.GARUDA_TERMINATE_EVENT)])

        if self._thread:
            self._thread.stop()

    def receive_event(self, content):
        """
        """
        data = json.loads(content['data'])
        logger.debug('Receives message:\n%s' % json.dumps(data, indent=4))

        garuda_uuid = data['garuda_uuid']
        events = [GAPushEvent.from_dict(event) for event in data['events']]

        self._send_events_to_garuda(garuda_uuid=garuda_uuid, events=events)

    def _send_events_to_garuda(self, garuda_uuid, events):
        """
        """
        session_uuids = self.core_controller.sessions_controller.get_all_sessions(garuda_uuid=garuda_uuid, listening=True)

        jobs = []
        for session_uuid in session_uuids:
            jobs.append(gevent.spawn(self._send_events, session_uuid=session_uuid, events=events))

    def _send_events(self, session_uuid, events):
        """
        """
        if session_uuid not in self._queues:
            return

        events_to_send = []
        queue = self._queues[session_uuid]
        session = self.core_controller.sessions_controller.get_session(session_uuid=session_uuid)

        for event in events:

            if event.action == self.core_controller.GARUDA_TERMINATE_EVENT:
                events_to_send.append(event)
                continue

            entity = event.entity
            resources = [GAResource(name=entity.rest_name, value=entity.id)]
            request = GARequest(action=GARequest.ACTION_READ, resources=resources)
            context = GAContext(request=request, session=session)
            context.object = entity

            operation_manager = GAOperationsController(context=context, storage_controller=self.core_controller.storage_controller)
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
