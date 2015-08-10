# -*- coding: utf-8 -*-

import json

from flask import Flask, request, make_response
from copy import deepcopy

from .utils.constants import RESTConstants
from garuda.exceptions import BadRequestException, NotFoundException, ConflictException, ActionNotAllowedException, GAException
from garuda.lib import PathParser
from garuda.models import GARequest, GASession, GAResponse
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
        self.app.add_url_rule('/<path:path>', 'vsd', self.index, methods=[RESTConstants.HTTP_GET, RESTConstants.HTTP_POST, RESTConstants.HTTP_PUT, RESTConstants.HTTP_DELETE, RESTConstants.HTTP_HEAD, RESTConstants.HTTP_OPTIONS])
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

    def _extract_content(self, content):
        """

        """
        return deepcopy(content)

    def _extract_parameters(self, parameters):
        """
        """
        params = {}

        for p in parameters:
            params[p[0]] = p[1]

        return params

    def make_channel_response(self, action, response):
        """
        """
        code = 520
        status = response.status
        content = response.content

        # Success
        if status == GAResponse.STATUS_SUCCESS:
            if action is GARequest.ACTION_CREATE:
                code = 201
            elif content is None or len(content) == 0:
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

        response = make_response(json.dumps(content))
        response.status_code = code
        response.mimetype = 'application/json'

        return response

    def determine_action(self, method, resources):
        """
        """
        if method is RESTConstants.HTTP_POST:
            return GARequest.ACTION_CREATE

        elif method is RESTConstants.HTTP_PUT:
            return GARequest.ACTION_UPDATE

        elif method is RESTConstants.HTTP_DELETE:
            return GARequest.ACTION_DELETE

        elif method in [RESTConstants.HTTP_GET, RESTConstants.HTTP_OPTIONS, RESTConstants.HTTP_HEAD]:

            if resources[-1].value is None:
                return GARequest.ACTION_READALL
            else:
                return GARequest.ACTION_READ

        raise Exception("Unknown action. This should never happen")

    def index(self, path):
        """
        """

        content = self._extract_content(request.json)
        parameters = self._extract_parameters(request.headers)
        method = request.method.upper()

        print '--- Request from %s ---' % parameters['Host']

        try:
            parser = PathParser()
            resources = parser.parse(path=path)

        except GAException as exc:
            exception_name = exc.__class__.__name__
            return self.make_channel_response(action=None, response=GAResponse(status=exception_name, content={u'description': 'Garuda failed with %s' % exception_name}))

        action = self.determine_action(method, resources)

        ga_request = GARequest(action=action, content=content, parameters=parameters)
        ga_session = GASession(user='me', resources=resources)

        ga_response = self.controller.execute(session=ga_session, request=ga_request)

        print '--- Response to %s ---' % parameters['Host']

        return self.make_channel_response(action=action, response=ga_response)
