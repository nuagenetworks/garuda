# -*- coding: utf-8 -*-

import json

from flask import Flask, request, make_response
from copy import deepcopy

from .utils.constants import RESTConstants
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
        self.app.add_url_rule('/<path:path>', 'vsd', self.index, methods=[RESTConstants.HTTP_POST, RESTConstants.HTTP_PUT, RESTConstants.HTTP_DELETE, RESTConstants.HTTP_HEAD, RESTConstants.HTTP_OPTIONS])
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

    def make_channel_response(self, action, response):
        """
        """
        code = 520  # unknown error
        status = response['status']
        data = response['data']

        # Success
        if status == 'SUCCESS':
            if action is GASession.ACTION_CREATE:
                code = 201
            elif data is None or len(data) == 0:
                code = 204
            else:
                code = 200

        # Errors
        elif status == BadRequestException.__name__:
            code = 400
        elif status == NotFoundException.__name__:
            code = 404
        elif status == ConflictException.__name__:
            code = 409
        elif status == ActionNotAllowedException.__name__:
            code = 405

        response = make_response(json.dumps(data))
        response.status_code = code
        response.mimetype = 'application/json'

        return response

    def determine_action(self, method, resources):
        """
        """
        if method is RESTConstants.HTTP_POST:
            return GASession.ACTION_CREATE

        elif method is RESTConstants.HTTP_PUT:
            return GASession.ACTION_UPDATE

        elif method is RESTConstants.HTTP_DELETE:
            return GASession.ACTION_DELETE

        elif method in [RESTConstants.HTTP_GET, RESTConstants.HTTP_OPTIONS, RESTConstants.HTTP_HEAD]:

            if resources[-1].value is None:
                return GASession.ACTION_READALL
            else:
                return GASession.ACTION_READ

        raise Exception("Unknown action. This should never happen");

    def index(self, path):
        """
        """

        data = self._extract_data(request.json)
        headers = self._extract_headers(request.headers)
        method = request.method.upper()

        print '--- Request from %s ---' % headers['Host']

        try:
            parser = PathParser()
            resources = parser.parse(path=path)

        except Exception as exc:
            exception_name = exc.__class__.__name__
            return self.make_channel_response(action=None, response={u'status': exception_name, u'data':{u'description': 'Garuda failed with %s' % exception_name}})

        action = self.determine_action(method, resources)

        ga_request = GARequest(action=action, url=request.url, data=data, headers=headers)
        ga_session = GASession(user='me', data={}, action=action, resources=resources)

        response = self.controller.execute(session=ga_session, request=ga_request)

        print '--- Response to %s ---' % headers['Host']

        return self.make_channel_response(action=action, response=response)
