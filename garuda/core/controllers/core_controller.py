# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger('Garuda.CoreController')

from .model_controller import ModelController
from .operations_manager import OperationsManager
from .thread_manager import ThreadManager
from .push_controller import PushController
from .sessions_manager import SessionsManager
from .permissions_controller import PermissionsController

from garuda.core.lib import SDKsManager
from garuda.core.models import GAContext, GAResponse, GARequest, GAError, GAPushEvent

from uuid import uuid4

import ssl

class CoreController(object):
    """

    """
    def __init__(self, sdks_manager, communication_channels=[], authentication_plugins=[], model_controller_plugins=[], permission_controller_plugins=[]):
        """
        """
        self._uuid = str(uuid4())
        self._channels = []
        self._thread_manager = ThreadManager()
        self._model_controller = ModelController(plugins=model_controller_plugins)
        self._sessions_manager = SessionsManager(plugins=authentication_plugins)
        self._push_controller = PushController(core_controller=self)
        self._permissions_controller = PermissionsController(plugins=permission_controller_plugins)
        self._sdks_manager = sdks_manager

        for channel in communication_channels:
            self.register_channel(channel)


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
    def sdks_manager(self):
        """
        """
        return self._sdks_manager

    def register_channel(self, channel):
        """
        """
        logger.debug('Register channel %s' % channel)
        if channel not in self._channels:
            channel.controller = self
            self._channels.append(channel)

    def unregister_channel(self, channel):
        """
        """
        logger.debug('Unregister channel %s' % channel)
        if channel in self._channels:
            self._channels.remove(channel)

    def start(self):
        """
        """
        logger.debug('Starting core controller')

        self.push_controller.start()

        for channel in self._channels:
            logger.debug('Starting channel %s' % channel)
            self._thread_manager.start(channel.start)

    def is_running(self):
        """
        """
        return self._thread_manager.is_running()

    def stop(self, signal=None, frame=None):
        """
        """
        logger.debug('Stopping core controller')
        self._thread_manager.stop_all()
        self.push_controller.flush(garuda_uuid=self.uuid)
        self.push_controller.stop()

    def execute(self, request):
        """
        """
        session_uuid = request.parameters['password'] if 'password' in request.parameters else None
        session = self.sessions_manager.get(session_uuid=session_uuid)
        context = GAContext(session=session, request=request)

        logger.debug('Execute action %s on session UUID=%s' % (request.action, session_uuid))

        if session is None:
            context.report_error(type=GAError.TYPE_UNAUTHORIZED, property='', title='Unauthorized access', description='Could not grant access. Please log in.')
            return GAResponse(status=context.errors.type, content=context.errors)

        manager = OperationsManager(context=context, model_controller=self.model_controller)
        manager.run()

        if context.has_errors():
            return GAResponse(status=context.errors.type, content=context.errors)

        if request.action is GARequest.ACTION_READALL:
            return GAResponse(status=GAResponse.STATUS_SUCCESS, content=context.objects)

        # Sample code
        context.add_event(GAPushEvent(action='TOTO', entity=context.object))
        context.add_event(GAPushEvent(action=request.action, entity=context.object))
        # End sample code

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
