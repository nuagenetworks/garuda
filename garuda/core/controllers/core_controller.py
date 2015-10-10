# -*- coding: utf-8 -*-

import importlib
import logging
import ssl
from uuid import uuid4

from .storage_controller import GAStorageController
from .operations_controller import GAOperationsController
from .push_controller import GAPushController
from .sessions_controller import GASessionsController
from .permissions_controller import GAPermissionsController
from .communication_channels_controller import GACommunicationChannelsController

from garuda.core.lib import SDKsManager
from garuda.core.models import GAContext, GAResponse, GARequest, GAError

logger = logging.getLogger('garuda.corecontroller')


class GACoreController(object):
    """

    """

    GARUDA_TERMINATE_EVENT = 'GARUDA_TERMINATE_EVENT'

    def __init__(self, sdks_info, communication_channel_plugins=[], authentication_plugins=[], storage_plugins=[], permission_controller_plugins=[]):
        """
        """

        self._sdks_manager = SDKsManager()

        for sdk_info in sdks_info:
            self._sdks_manager.register_sdk(identifier=sdk_info['identifier'], sdk=importlib.import_module(sdk_info['module']))

        self._uuid = str(uuid4())
        self._storage_controller = GAStorageController(plugins=storage_plugins, core_controller=self)
        self._sessions_controller = GASessionsController(plugins=authentication_plugins, core_controller=self)
        self._push_controller = GAPushController(core_controller=self)
        self._permissions_controller = GAPermissionsController(plugins=permission_controller_plugins, core_controller=self)
        self._communication_channels_controller = GACommunicationChannelsController(plugins=communication_channel_plugins, core_controller=self)

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
    def communication_channels_controller(self):
        """
        """
        return self._communication_channels_controller

    @property
    def sdks_manager(self):
        """
        """
        return self._sdks_manager

    def start(self):
        """
        """
        logger.debug('Starting core controller')

        self.push_controller.start()
        self.communication_channels_controller.start()

    def stop(self, signal=None, frame=None):
        """
        """
        logger.debug('Stopping core controller')

        self.storage_controller.unregister_all_plugins()
        self.permissions_controller.unregister_all_plugins()
        self.sessions_controller.unregister_all_plugins()
        self.communication_channels_controller.unregister_all_plugins()

        self.push_controller.stop()
        self.communication_channels_controller.stop()
        self.sessions_controller.flush_garuda(self.uuid)

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

        operations_controller = GAOperationsController(context=context, storage_controller=self.storage_controller)
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
