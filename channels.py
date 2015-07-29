# -*- coding: utf-8 -*-

from gaexceptions import NotImplementedException
from utils import GARequest, GASession
from controllers import CoreController, OperationsManager


class CommunicationChannel(object):
    """

    """
    def start(self):
        """
        """
        raise NotImplementedException('CommunicationChannel should implement start method')

    def stop(self):
        """
        """
        raise NotImplementedException('CommunicationChannel should implement stop method')

    def receive(self):
        """

        """
        raise NotImplementedException('CommunicationChannel should implement receive method')

    def send(self):
        """

        """
        raise NotImplementedException('CommunicationChannel should implement send method')

    def push(self):
        """

        """
        raise NotImplementedException('CommunicationChannel should implement push method')


from flask import Flask, request
import threading


class StoppableThread(threading.Thread):
    """

    """

    def __init__(self, *args, **kwargs):
        """
        """
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

    def stop(self):
        """
        """
        self._stop.set()

    def stopped(self):
        """
        """
        return self._stop.isSet()


class RESTCommunicationChannel(CommunicationChannel):
    """

    """
    def __init__(self):
        """
        """
        self.thread = None
        self.app = Flask(self.__class__.__name__)
        self.app.add_url_rule('/', 'index', self.index)

    def start(self, *args, **kwargs):
        """

        """
        self.thread = StoppableThread(target=self.app.run, args=args, kwargs=kwargs)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """
        """
        print 'stopping...'
        self.thread.stop()

    def index(self):
        """ """
        ga_request = GARequest(method=request.method, url=request.url, data=request.data, headers=request.headers, cookies=request.cookies)
        ga_session = GASession()

        core = CoreController(session=ga_session, request=ga_request)

        operation = OperationsManager(context=core.context)
        operation.do_read_operation()

        return ga_session.uuid
