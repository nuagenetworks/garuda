# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger('garuda.corecontroller')

from .model_controller import GAModelController
from .operations_manager import GAOperationsManager
from .push_controller import GAPushController
from .sessions_manager import GASessionsManager
from .permissions_controller import GAPermissionsController
from .communication_channels_controller import GACommunicationChannelsController

from garuda.core.lib import SDKsManager
from garuda.core.models import GAContext, GAResponse, GARequest, GAError, GAPushEvent

from uuid import uuid4

import ssl

class GACoreController(object):
    """

    """
    def __init__(self, sdks_manager, communication_channel_plugins=[], authentication_plugins=[], model_controller_plugins=[], permission_controller_plugins=[]):
        """
        """
        self._uuid = str(uuid4())
        self._model_controller = GAModelController(plugins=model_controller_plugins, core_controller=self)
        self._sessions_manager = GASessionsManager(plugins=authentication_plugins, core_controller=self)
        self._push_controller = GAPushController(core_controller=self)
        self._permissions_controller = GAPermissionsController(plugins=permission_controller_plugins, core_controller=self)
        self._communication_channels_controller = GACommunicationChannelsController(plugins=communication_channel_plugins, core_controller=self)
        self._sdks_manager = sdks_manager

    @property
    def uuid(self):
        """
        """
        return self._uuid

    @property
    def model_controller(self):
        """
        """
        return self._model_controller

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
    def sessions_manager(self):
        """
        """
        return self._sessions_manager

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
        self.communication_channels_controller.stop()
        self.push_controller.flush(garuda_uuid=self.uuid)
        self.push_controller.stop()

    def execute(self, request):
        """
        """
        session_uuid = self.sessions_manager.get_session_identifier(request=request)

        if session_uuid:
            session = self.sessions_manager.get_session(session_uuid=session_uuid)

        if not session:
            session = self.sessions_manager.create_session(request=request, garuda_uuid=self.uuid)

            if session:
                return GAResponse(status=GAResponse.STATUS_SUCCESS, content=[session.root_object])

        context = GAContext(session=session, request=request)

        if not session:
            context.report_error(type=GAError.TYPE_UNAUTHORIZED, property='', title='Unauthorized access', description='Could not grant access. Please log in.')
            return GAResponse(status=context.errors.type, content=context.errors)

        logger.debug('Execute action %s on session UUID=%s' % (request.action, session_uuid))

        manager = GAOperationsManager(context=context, model_controller=self.model_controller)
        manager.run()

        if context.has_errors():
            return GAResponse(status=context.errors.type, content=context.errors)

        if request.action is GARequest.ACTION_READALL:
            return GAResponse(status=GAResponse.STATUS_SUCCESS, content=context.objects)

        if len(context.events) > 0:
            self.push_controller.add_events(events=context.events)

        return GAResponse(status=GAResponse.STATUS_SUCCESS, content=context.object)

    def execute_authenticate(self, request):
        """
        """
        session = self.sessions_manager.create_session(request=request, garuda_uuid=self.uuid)
        context = GAContext(session=session, request=request)

        logger.debug('Execute action %s on session UUID=%s' % (request.action, session.uuid if session else None))

        if session is None:
            description = 'Unable to authenticate'
            context.report_error(type=GAError.TYPE_AUTHENTICATIONFAILURE, property='', title='Authentication failed!', description=description)

        if context.has_errors():
            return GAResponse(status=context.errors.type, content=context.errors)

        return GAResponse(status=GAResponse.STATUS_SUCCESS, content=[session.user])

    def get_queue(self, request):
        """
        """

        session_uuid = request.parameters['password'] if 'password' in request.parameters else None
        session = self.sessions_manager.get(session_uuid=session_uuid)
        # context = GAContext(session=session, request=request)

        if session is None:
            # TODO: Create a GAResponse
            # context.report_error(type=GAError.TYPE_UNAUTHORIZED, property='', title='Unauthorized access', description='Could not grant access. Please log in.')
            return None

        logger.debug('Set listening %s session UUID=%s for push notification' % (request.action, session_uuid))

        session.is_listening_push_notifications = True
        self.sessions_manager.save(session)

        queue = self.push_controller.get_queue_for_session(session.uuid)

        return queue
