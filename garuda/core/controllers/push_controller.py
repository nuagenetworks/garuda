# -*- coding: utf-8 -*-

import logging
import msgpack

from garuda.core.models import GAPushEvent, GAResource, GARequest, GAContext, GAController
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
        pipeline = self.redis.pipeline()

        # we loop on every system wide sessions
        for session in self.core_controller.sessions_controller.get_all_sessions():

            session_events = []

            # for every objects in the events, we check that the session's user has a permission
            # and if so, we add the permitted objects to the session_events list
            for event in events:
                if self.core_controller.permissions_controller.has_permission(resource=session.root_object.id, target=event.entity, permission='read'):
                    session_events.append(event)

            # Then, if there is at least one permitted entity in the events list, we pack them
            # and plublish it to the redis pipeline
            if len(session_events):
                packs = [msgpack.packb(session_event.to_dict()) for session_event in session_events]
                event_queue_key = 'eventqueue:%s' % session.redis_key
                logger.debug('Adding %d event pack(s) to the session event queue: %s' % (len(events), event_queue_key))
                pipeline.lpush(event_queue_key, *packs)

        # Finally we execute the redis pipeline
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

        key, pack = blob
        event = GAPushEvent.from_dict(data=msgpack.unpackb(pack))
        resources = [GAResource(name=event.entity.rest_name, value=event.entity.id)]
        request = GARequest(action=GARequest.ACTION_READ, resources=resources)
        context = GAContext(request=request, session=session)
        context.object = event.entity

        # operation_manager = GAOperationsController(context=context,
        #                                            logic_controller=self.core_controller.logic_controller,
        #                                            storage_controller=self.core_controller.storage_controller)
        # operation_manager.run()

        # if not context.has_errors:
        #     logger.debug('Returning one event to session %s' % session.redis_key)
        return event

    def is_event_queue_empty(self, session):
        """
        """
        return self.redis.llen('eventqueue:%s' % session.redis_key) == 0

    def delete_event_queue(self, session_key):
        """
        """
        self.redis.delete('eventqueue:%s' % session_key)
