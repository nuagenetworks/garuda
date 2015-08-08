# -*- coding: utf-8 -*-

from .process_manager import ProcessManager
from .operations_manager import OperationsManager
from channels.rest import RESTCommunicationChannel
from garuda.models import GAContext


class CoreController(object):
    """

    """
    def __init__(self):
        """
        """
        self._channels = []
        self._process_manager = ProcessManager()

        flask2000 = RESTCommunicationChannel(controller=self, port=2000, debug=True, use_reloader=False)
        flask3000 = RESTCommunicationChannel(controller=self, port=3000, debug=True, use_reloader=False)

        self.register_channel(flask2000)
        self.register_channel(flask3000)

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

    def execute(self, session, request):
        """
        """
        # TODO: Indicate what to do in the operation

        context = GAContext(session=session, request=request)

        try:
            manager = OperationsManager(context=context)
            manager.run()
        except Exception as exc:
            return {'status': exc.__class__.__name__, 'data': context.errors}

        # TODO: Create response from context

        return {'status': 'SUCCESS', 'data': 'ok'}