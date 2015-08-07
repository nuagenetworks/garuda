# -*- coding: utf-8 -*-

from flask import Flask, request, make_response
from copy import deepcopy

from gaexceptions import NotImplementedException, NotFoundException
from parser import PathParser
from utils import GARequest, GASession, Resource


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

    def is_running(self):
        """

        """
        raise NotImplementedException('CommunicationChannel should implement is running method')

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


import json

from werkzeug.exceptions import HTTPException

class GarudaHTTPException(HTTPException):
    """  """

    data = dict()

    def __init__(self, code, data):
        """ Init """

        super(GarudaHTTPException, self).__init__()
        self.code = code
        self.data = data

    def get_body(self, environ):
        """Get the JSON body."""

        return json.dumps(self.data)

    def get_headers(self, environ):
        """Get a list of headers."""

        # options_resp = make_default_options_response()

        return [('Content-Type', 'application/json'),
                ('Content-Length', len(self.get_body(environ))),
                ('Access-Control-Max-Age', '1')]


def abort_with_error(code, data):
    """
    """
    raise GarudaHTTPException(code=code, data=data)


def create_response(code, data):
    """
    """
    response = make_response(json.dumps(data))

    response.status_code = code
    response.mimetype = 'application/json'

    return response


class RESTCommunicationChannel(CommunicationChannel):
    """

    """
    def __init__(self, controller, **kwargs):
        """
        """
        self._is_running = False
        self.controller = controller
        self.app = Flask(self.__class__.__name__)

        self.app.add_url_rule('/', 'vsd', self.index, defaults={'path': ''})
        self.app.add_url_rule('/<path:path>', 'vsd', self.index, methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD'])
        self.start_parameters = kwargs

    def start(self):
        """
        """
        if self.is_running:
            return

        self._is_running = True
        self.app.run(**self.start_parameters)

    def stop(self):
        """
        """
        if not self.is_running:
            return

        self._is_running = False

    @property
    def is_running(self):
        """
        """
        return self._is_running

    def _extract_data(self, data):
        """

        """
        return deepcopy(data)

    def _extract_headers(self, headers):
        """
        """
        headers = {}

        for header in request.headers:
            headers[header[0]] = header[1]

        return headers

    def index(self, path):
        """
        """

        data = self._extract_data(request.json)
        headers = self._extract_headers(request.headers)

        print '--- Request from %s ---' % headers['Host']

        try:
            parser = PathParser()
            resources = parser.parse(path=path)

        except NotFoundException as exception:
            abort_with_error(code=404, data={u'error_code': 40401, u'message': 'NOT FOUND'})

        resources = parser.resources
        method = request.method.upper()

        if method is 'POST':
            action = GASession.ACTION_CREATE

        elif method is 'PUT':
            action = GASession.ACTION_UPDATE

        elif method is 'DELETE':
            action = GASession.ACTION_DELETE

        elif method in ['GET', 'OPTIONS', 'HEAD']:

            if resources[-1].value is None:
                action = GASession.ACTION_READALL
            else:
                action = GASession.ACTION_READ

        ga_request = GARequest(action=action, url=request.url, data=data, headers=headers)
        ga_session = GASession(user='me', data={}, action=action, resources=resources)

        response = self.controller.execute(session=ga_session, request=ga_request)

        print '--- Response to %s ---' % headers['Host']

        if response['status'] >= 400:
            http_response = create_response(response['status'], response['errors'])
        else:
            http_response = create_response(response['status'], response['data'])

        return http_response
