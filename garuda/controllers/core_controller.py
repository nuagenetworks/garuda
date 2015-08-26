# -*- coding: utf-8 -*-

from .models_controller import ModelsController
from .operations_manager import OperationsManager
from .process_manager import ProcessManager
from .push_controller import PushController
from .sessions_manager import SessionsManager

from channels.rest import RESTCommunicationChannel
from garuda.models import GAContext, GAResponse, GARequest, GAError

from uuid import uuid4


class CoreController(object):
    """

    """
    def __init__(self):
        """
        """
        self._uuid = str(uuid4())
        self._channels = []
        self._process_manager = ProcessManager()
        self._models_controller = ModelsController()
        self._sessions_manager = SessionsManager()
        self._push_controller = PushController()

        flask2000 = RESTCommunicationChannel(controller=self, port=2000, processes=10, debug=True, use_reloader=False)
        flask3000 = RESTCommunicationChannel(controller=self, port=3000, processes=10, debug=True, use_reloader=False)

        self.register_channel(flask2000)
        # self.register_channel(flask3000)

    @property
    def uuid(self):
        """
        """
        return self._uuid

    @property
    def models_controller(self):
        """
        """
        return self._models_controller

    @property
    def push_controller(self):
        """
        """
        return self._push_controller

    @property
    def sessions_manager(self):
        """
        """
        return self._sessions_manager

    def register_channel(self, channel):
        """
        """
        if channel not in self._channels:
            self._channels.append(channel)

    def unregister_channel(self, channel):
        """
        """
        if channel in self._channels:
            self._channels.remove(channel)

    def start(self):
        """
        """
        self.push_controller.start()

        for channel in self._channels:
            self._process_manager.start(channel.start)

    def is_running(self):
        """
        """
        return self._process_manager.is_running()

    def stop(self, signal=None, frame=None):
        """
        """
        self._process_manager.stop_all()

        for channel in self._channels:
            channel.stop()

        self.push_controller.stop()

    def execute(self, request):
        """
        """
        session_uuid = request.parameters['password'] if 'password' in request.parameters else None
        session = self.sessions_manager.get_session(uuid=session_uuid)
        context = GAContext(session=session, request=request)

        if session is None:
            context.report_error(type=GAError.TYPE_UNAUTHORIZED, property='', title='Unauthorized access', description='Could not grant access. Please log in.')
            return GAResponse(status=context.errors.type, content=context.errors)

        manager = OperationsManager(context=context, models_controller=self.models_controller)
        manager.run()

        if context.has_errors():
            return GAResponse(status=context.errors.type, content=context.errors)

        self.push_controller.add_notification(uuid=self.uuid, action='ACTION', entities=['COUCOU'])

        if request.action is GARequest.ACTION_READALL:
            return GAResponse(status=GAResponse.STATUS_SUCCESS, content=context.objects)

        return GAResponse(status=GAResponse.STATUS_SUCCESS, content=context.object)

    def execute_authenticate(self, request):
        """
        """
        session = self.sessions_manager.create_session(request=request, models_controller=self.models_controller, garuda_uuid=self.uuid)
        context = GAContext(session=session, request=request)

        if session is None:
            description = 'Unable to authenticate'
            context.report_error(type=GAError.TYPE_AUTHENTICATIONFAILURE, property='', title='Authentication failed!', description=description)

        if context.has_errors():
            return GAResponse(status=context.errors.type, content=context.errors)

        return GAResponse(status=GAResponse.STATUS_SUCCESS, content=session.user)

    def get_queue(self, request):
        """
        """

        session_uuid = request.parameters['password'] if 'password' in request.parameters else None
        session = self.sessions_manager.get_session(uuid=session_uuid)
        context = GAContext(session=session, request=request)

        if session is None:
            context.report_error(type=GAError.TYPE_UNAUTHORIZED, property='', title='Unauthorized access', description='Could not grant access. Please log in.')
            return GAResponse(status=context.errors.type, content=context.errors)

        session.is_listening_push_notifications = True
        self.sessions_manager.save(session)

        return self.push_controller.get_queue_for_session(session_uuid)
