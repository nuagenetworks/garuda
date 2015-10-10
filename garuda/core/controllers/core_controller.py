# -*- coding: utf-8 -*-

import importlib
import ssl
import logging
import redis
from uuid import uuid4

from .storage_controller import GAStorageController
from .operations_controller import GAOperationsController
from .push_controller import GAPushController
from .sessions_controller import GASessionsController
from .permissions_controller import GAPermissionsController
from .channels_controller import GAChannelsController
from .logic_controller import GALogicController

from garuda.core.lib import SDKLibrary
from garuda.core.models import GAContext, GAResponse, GARequest, GAError

logger = logging.getLogger('garuda.core')

class GACoreController(object):
    """

    """

    GARUDA_TERMINATE_EVENT = 'GARUDA_TERMINATE_EVENT'

    def __init__(self, sdks_info, redis_info, channels=[], authentication_plugins=[], logic_plugins=[], storage_plugins=[], permission_plugins=[]):
        """
        """
        self._uuid = str(uuid4())
        self._sdk_library = SDKLibrary()
        self._redis = redis.StrictRedis(host=redis_info['host'], port=redis_info['port'], db=redis_info['db'])

        for sdk_info in sdks_info:
            self._sdk_library.register_sdk(identifier=sdk_info['identifier'], sdk=importlib.import_module(sdk_info['module']))


        self._channels_controller = GAChannelsController(plugins=channels, core_controller=self)
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

    @property
    def channels_controller(self):
        """
        """
        return self._channels_controller

    @property
    def sdk_library(self):
        """
        """
        return self._sdk_library

    def start(self):
        """
        """
        logger.debug('Starting core controller')

        self.push_controller.start()
        self.channels_controller.start()

        logger.info('Garuda is initialized and ready to rock! (Press CTRL+C to quit)')

    def stop(self, signal=None, frame=None):
        """
        """
        logger.debug('Stopping core controller')

        self.storage_controller.unregister_all_plugins()
        self.permissions_controller.unregister_all_plugins()
        self.sessions_controller.unregister_all_plugins()
        self.channels_controller.unregister_all_plugins()

        self.push_controller.stop()
        self.channels_controller.stop()
        self.sessions_controller.flush_garuda(self.uuid)

        logger.info('Garuda has stopped.')

    def execute(self, request):
        """
        """
        session_uuid = self.sessions_controller.get_session_identifier(request=request)

        if session_uuid:
            session = self.sessions_controller.get_session(session_uuid=session_uuid)

        if not session:
            session = self.sessions_controller.create_session(request=request, garuda_uuid=self.uuid)

            if session:
                return GAResponse(status=GAResponse.STATUS_SUCCESS, content=[session.root_object])

        context = GAContext(session=session, request=request)

        if not session:
            error = GAError(type=GAError.TYPE_UNAUTHORIZED,
                    title='Unauthorized access',
                    description='Could not grant access. Please log in.')

            context.report_error(error)

            return GAResponse(status=context.errors.type, content=context.errors)

        logger.debug('Execute action %s on session UUID=%s' % (request.action, session_uuid))

        operations_controller = GAOperationsController(context=context, logic_controller=self.logic_controller, storage_controller=self.storage_controller)
        operations_controller.run()

        if context.has_errors():
            return GAResponse(status=context.errors.type, content=context.errors)

        if request.action is GARequest.ACTION_READALL:
            return GAResponse(status=GAResponse.STATUS_SUCCESS, content=context.objects)

        if len(context.events) > 0:
            self.push_controller.add_events(events=context.events)

        return GAResponse(status=GAResponse.STATUS_SUCCESS, content=context.object)

    def get_queue(self, request):
        """
        """

        session_uuid = request.parameters['password'] if 'password' in request.parameters else None
        session = self.sessions_controller.get_session(session_uuid=session_uuid)
        # context = GAContext(session=session, request=request)

        if session is None:
            # TODO: Create a GAResponse
            # context.report_error(type=GAError.TYPE_UNAUTHORIZED, property='', title='Unauthorized access', description='Could not grant access. Please log in.')
            return None

        logger.debug('Set listening %s session UUID=%s for push notification' % (request.action, session_uuid))

        session.is_listening_push_notifications = True
        self.sessions_controller.save(session)

        queue = self.push_controller.get_queue_for_session(session.uuid)

        return queue
