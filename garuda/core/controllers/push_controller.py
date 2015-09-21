# -*- coding: utf-8 -*-

import json
import redis
import logging

logger = logging.getLogger('Garuda.PushController')

from Queue import Queue

from garuda.core.models import GAPushEvent
from garuda.core.config import GAConfig

from .sessions_manager import SessionsManager


class PushController(object):
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
        p.subscribe(**{'garuda-new-event': self.receive_event})

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

        for session_uuid in session_uuids:
            if session_uuid not in self._queues:
                continue

            queue = self._queues[session_uuid]
            # session = self.core_controller.sessions_manager.get(session_uuid=session_uuid)
            #
            # for entity in notification.entities:
            #     # TODO: Trigger a READ operation for each session
            #     resources = [GAResources(name=entity.parent_type, value=entity.parent_id), GARequest(name=entity.rest_name, value=entity.id)]
            #     request = GARequest(action=ACTION_READ, resources=resources)
            #     context = GAContext(request=request, session=session)
            #
            #     operation_manager = OperationManager(context=context)
            #     operation_manager.run()
            #
            #     if context.has_errors():
            #         # TODO: Send notification with error
            #
            #     else:

            queue.put(events)

    def add_events(self, events):
        """
        """
        data = dict()
        data['garuda_uuid'] = self.core_controller.uuid
        data['events'] = [event.to_dict() for event in events]
        self._redis.publish('garuda-new-event', json.dumps(data))

    def get_queue_for_session(self, session_uuid):
        """
        """
        if session_uuid not in self._queues:
            logger.debug('Creating queue for session uuid=%s' % session_uuid)
            self._queues[session_uuid] = Queue()

        return self._queues[session_uuid]
