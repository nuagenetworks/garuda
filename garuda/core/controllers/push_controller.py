# -*- coding: utf-8 -*-

import json
import redis
import logging
import msgpack

from garuda.core.models import GAPushEvent, GAResource, GARequest, GAContext, GAController
from garuda.core.lib import ThreadManager
from .operations_controller import GAOperationsController

logger = logging.getLogger('garuda.controller.push')

class GAPushController(GAController):
    """

    """

    @classmethod
    def identifier(cls):
        """
        """
        return 'garuda.controller.push'

    def push_events(self, events):
        """
        """
        packs = [msgpack.packb(event.to_dict()) for event in events]

        pipeline = self.redis.pipeline()

        for session_key in self.core_controller.sessions_controller.get_all_session_keys():
            event_queue_key = 'eventqueue:%s' % session_key
            logger.debug('Adding %d event pack(s) to the session event queue: %s' % (len(events), event_queue_key))
            pipeline.lpush(event_queue_key, *packs)

        logger.debug('Executing event queue command pipeline...')
        pipeline.execute()
        logger.debug('Event queue command pipeline executed')

    def get_next_event(self, session, timeout=None):
        """
        """
        event_queue_key = 'eventqueue:%s' % session.redis_key

        logger.debug('Waiting for event to be popped out of event queue: %s' % event_queue_key)

        blob = self.redis.brpop([event_queue_key], timeout=timeout)

        logger.debug('Popping one event from the session event queue %s' % event_queue_key)

        if not blob:
            return

        key, pack      = blob
        event          = GAPushEvent.from_dict(data=msgpack.unpackb(pack))
        resources      = [GAResource(name=event.entity.rest_name, value=event.entity.id)]
        request        = GARequest(action=GARequest.ACTION_READ, resources=resources)
        context        = GAContext(request=request, session=session)
        context.object = event.entity

        operation_manager = GAOperationsController( context=context,
                                                    logic_controller=self.core_controller.logic_controller,
                                                    storage_controller=self.core_controller.storage_controller)
        operation_manager.run()

        if not context.has_errors():
            logger.debug('Returning one event to session %s' % session.redis_key)
            return event

    def is_event_queue_empty(self, session):
        """
        """
        return self.redis.llen('eventqueue:%s' % session.redis_key) == 0

    def delete_event_queue(self, session_key):
        """
        """
        self.redis.delete('eventqueue:%s' % session_key)
