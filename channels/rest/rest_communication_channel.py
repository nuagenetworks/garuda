# -*- coding: utf-8 -*-

import json

from flask import Flask, request, make_response
from copy import deepcopy

from .utils import GarudaHTTPException
from garuda.exceptions import BadRequestException, NotFoundException, ConflictException, ActionNotAllowedException
from garuda.lib import PathParser
from garuda.models import GARequest, GASession
from garuda.models.abstracts import CommunicationChannel


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

    def abort_with_error(code, data):
        """
        """
        raise GarudaHTTPException(code=code, data=data)

    def make_channel_response(self, action, response):
        """
        """
        code = 520  # unknown error
        status = response['status']
        data = response['data']

        # Success
        if status is 'SUCCESS':
            if action is GASession.ACTION_CREATE:
                code = 201
            elif data is None or len(data) == 0:
                code = 204
            else:
                code = 200

        # Errors
        elif status is BadRequestException.__name__:
            code = 400
        elif status is NotFoundException.__name__:
            code = 404
        elif status is ConflictException.__name__:
            code = 409
        elif status is ActionNotAllowedException.__name__:
            code = 405

        response = make_response(json.dumps(data))
        response.status_code = code
        response.mimetype = 'application/json'

        return response

    def index(self, path):
        """
        """

        data = self._extract_data(request.json)
        headers = self._extract_headers(request.headers)

        print '--- Request from %s ---' % headers['Host']

        try:
            parser = PathParser()
            resources = parser.parse(path=path)

        except NotFoundException:
            self.abort_with_error(code=404, data={u'error_code': 40401, u'message': 'NOT FOUND'})

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

        return self.make_channel_response(action=action, response=response)
