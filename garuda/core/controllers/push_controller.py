# -*- coding: utf-8 -*-

import json
import redis
import logging
from Queue import Queue

from garuda.core.models import GAPushEvent, GAResource, GARequest, GAContext, GAPushEventQueue, GAController
from garuda.core.lib import ThreadManager
from .operations_controller import GAOperationsController

logger = logging.getLogger('garuda.controller.push')


class GAPushController(GAController):
    """

    """
    def __init__(self, core_controller, redis_conn):
        """
        """
        super(GAPushController, self).__init__(core_controller=core_controller, redis_conn=redis_conn)
        self._event_queues = {}
        self.subscribe(channel='event:new', handler=self._on_new_push_event)

    @classmethod
    def identifier(cls):
        """
        """
        return 'garuda.controller.push'

    def start(self):
        """
        """

        self.start_listening_to_events()
        pass

    def stop(self):
        """
        """
        self.stop_listening_to_events()

    def push_events(self, events):
        """
        """
        self.publish('event:new', [event.to_dict() for event in events])

    def get_next_event(self, session):
        """
        """
        for event in self._queue_for_session_uuid(session.uuid):
            yield event

    def _on_new_push_event(self, data):
        """
        """

        data = json.loads(data)

        events = [GAPushEvent.from_dict(event) for event in data]

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
            self._event_queues[session_uuid] = GAPushEventQueue(queue=Queue(), timeout=60, accumulation_time=0.3)

        return self._event_queues[session_uuid]