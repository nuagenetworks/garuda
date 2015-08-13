# -*- coding: utf-8 -*-

from .process_manager import ProcessManager
from .operations_manager import OperationsManager
from .sessions_manager import SessionsManager
from .models_controller import ModelsController

from channels.rest import RESTCommunicationChannel
from garuda.models import GAContext, GAResponse, GARequest

from uuid import uuid4


class CoreController(object):
    """

    """
    def __init__(self):
        """
        """
        self._uuid = uuid4().hex
        self._channels = []
        self._process_manager = ProcessManager()
        self._models_controller = ModelsController()
        self._sessions_manager = SessionsManager()

        flask2000 = RESTCommunicationChannel(controller=self, port=2000, processes=3, debug=True, use_reloader=False)
        flask3000 = RESTCommunicationChannel(controller=self, port=3000, processes=3, debug=True, use_reloader=False)

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

    def execute(self, request):
        """
        """
        session_uuid = request.parameters['X-GASession'] if 'X-GASession' in request.parameters else None
        session = self.sessions_manager.get_session(uuid=session_uuid)

        context = GAContext(session=session, request=request)

        manager = OperationsManager(context=context, models_controller=self.models_controller)
        manager.run()

        if context.has_errors():
            return GAResponse(status=context.errors.type, content=context.errors)

        if request.action is GARequest.ACTION_READALL:
            return GAResponse(status=GAResponse.STATUS_SUCCESS, content=context.objects)

        return GAResponse(status=GAResponse.STATUS_SUCCESS, content=context.object)
