# -*- coding: utf-8 -*-

import json
import redis
import logging
from Queue import Queue

from garuda.core.models import GAPushEvent, GAResource, GARequest, GAContext, GAPushEventQueue
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
        self._redis_event_thread = None
        self._pubsub_thread = None
        self._event_queues = {}
        self._pubsub = None

    def push_events(self, events):
        """
        """
        data = dict()
        data['garuda_uuid'] = self.core_controller.uuid
        data['events'] = [event.to_dict() for event in events]
        self._redis.publish('event:new', json.dumps(data))

    def subscribe(self):
        """
        """
        self._pubsub = self._redis.pubsub()
        self._pubsub.subscribe('event:new')
        self._pubsub_thread = ThreadManager.start_thread(self._listen_to_redis_events)

    def unsubscribe(self):
        """
        """
        ThreadManager.stop_thread(self._pubsub_thread)
        self._pubsub.unsubscribe()
        self._pubsub = None

    def get_next_event(self, session):
        """
        """
        for event in self._queue_for_session_uuid(session.uuid):
            yield event

    def _listen_to_redis_events(self):
        """
        """
        for content in self._pubsub.listen():

            # TODO: manage the subscrition is not a event thing
            try:
                data = json.loads(content['data'])
            except:
                continue

            events = [GAPushEvent.from_dict(event) for event in data['events']]
            #logger.debug('Receives redis push:\n%s' % json.dumps(data, indent=4))

            for session in self.core_controller.sessions_controller.get_all_local_sessions(listening=True):

                events_to_send = []

                for event in events:

                    resources = [GAResource(name=event.entity.rest_name, value=event.entity.id)]
                    request = GARequest(action=GARequest.ACTION_READ, resources=resources)
                    context = GAContext(request=request, session=session)
                    context.object = event.entity

                    operation_manager = GAOperationsController( context=context,
                                                                logic_controller=self.core_controller.logic_controller,
                                                                storage_controller=self.core_controller.storage_controller)
                    operation_manager.run()

                    if not context.has_errors():
                        event.entity = context.object
                        events_to_send.append(event)

                if len(events_to_send):

                    logger.info("Adding events queue for session uuid: %s" % session.uuid)
                    queue = self._queue_for_session_uuid(session.uuid)
                    queue.put(events_to_send)

    ## Utilities

    def _queue_for_session_uuid(self, session_uuid):
        """
        """
        if not session_uuid in self._event_queues:
            self._event_queues[session_uuid] = GAPushEventQueue(queue=Queue(), timeout=7, accumulation_time=0.3)

        return self._event_queues[session_uuid]