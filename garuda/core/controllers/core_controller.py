# -*- coding: utf-8 -*-

import logging
import redis
import os
from uuid import uuid4

from .storage_controller import GAStorageController
from .operations_controller import GAOperationsController
from .push_controller import GAPushController
from .sessions_controller import GASessionsController
from .permissions_controller import GAPermissionsController
from .logic_controller import GALogicController

from garuda.core.lib import SDKLibrary
from garuda.core.models import GAContext, GAResponseFailure, GAResponseSuccess, GARequest, GAError

logger = logging.getLogger('garuda.core')


class GACoreController(object):
    """

    """
    def __init__(self, redis_info, authentication_plugins=[], logic_plugins=[], storage_plugins=[], permission_plugins=[]):
        """
        """
        self._uuid = str(uuid4())
        self._redis = redis.StrictRedis(host=redis_info['host'], port=redis_info['port'], db=redis_info['db'])
        self._running = False
        self._logic_controller = GALogicController(plugins=logic_plugins, core_controller=self)
        self._storage_controller = GAStorageController(plugins=storage_plugins, core_controller=self)
        self._sessions_controller = GASessionsController(plugins=authentication_plugins, core_controller=self, redis_conn=self._redis)
        self._permissions_controller = GAPermissionsController(plugins=permission_plugins, core_controller=self)

        self._push_controller = GAPushController(core_controller=self, redis_conn=self._redis)

    @property
    def uuid(self):
        """
        """
        return self._uuid

    @property
    def storage_controller(self):
        """
        """
        return self._storage_controller

    @property
    def logic_controller(self):
        """
        """
        return self._logic_controller

    @property
    def push_controller(self):
        """
        """
        return self._push_controller

    @property
    def permissions_controller(self):
        """
        """
        return self._permissions_controller

    @property
    def sessions_controller(self):
        """
        """
        return self._sessions_controller

    def start(self):
        """
        """
        if self._running: return
        self._running = True

        logger.debug('Starting core controller %s with pid %s' % (self.uuid, os.getpid()))
        self.push_controller.subscribe()
        self.sessions_controller.subscribe()


    def stop(self, signal=None, frame=None):
        """
        """
        if not self._running: return
        self._running = False

        logger.debug('Stopping core controller %s with pid %s' % (self.uuid, os.getpid()))

        self.sessions_controller.unsubscribe()
        self.push_controller.unsubscribe()

        self.storage_controller.unregister_all_plugins()
        self.permissions_controller.unregister_all_plugins()
        self.sessions_controller.unregister_all_plugins()

    def execute_model_request(self, request):
        """
        """
        session_uuid = self.sessions_controller.get_session_identifier(request=request)
        session = None

        logger.debug("finding session: %s" % session_uuid)
        if session_uuid:
            session = self.sessions_controller.get_session(session_uuid=session_uuid)

        if not session:
            session = self.sessions_controller.create_session(request=request)

            if session:
                return GAResponseSuccess(content=[session.root_object])

        context = GAContext(session=session, request=request)

        if not session:
            error = GAError(type=GAError.TYPE_UNAUTHORIZED,
                    title='Unauthorized access',
                    description='Could not grant access. Please log in.')

            context.report_error(error)

            return GAResponseFailure(content=context.errors)

        # reset the session ttl
        self.sessions_controller.reset_session_ttl(session)

        logger.debug('Execute action %s on session UUID=%s' % (request.action, session_uuid))

        operations_controller = GAOperationsController(context=context, logic_controller=self.logic_controller, storage_controller=self.storage_controller)
        operations_controller.run()

        response = context.make_response()

        if len(context.events) > 0:
            self.push_controller.push_events(events=context.events)

        return response

    def execute_events_request(self, request):
        """
        """
        session_uuid = request.token
        session = self.sessions_controller.get_session(session_uuid=session_uuid)
        context = GAContext(session=session, request=request)

        if session is None:
            error = GAError(type=GAError.TYPE_UNAUTHORIZED,
                            title='Unauthorized access',
                            description='Could not grant access. Please login.')

            context.report_error(error)
            return (GAResponseFailure(content=context.errors), None)

        # reset the session ttl
        self.sessions_controller.reset_session_ttl(session)

        return (session, None)
