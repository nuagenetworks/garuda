# -*- coding: utf-8 -*-

import json

from copy import deepcopy
from uuid import uuid4

from flask import Flask, request, make_response

from .utils.constants import RESTConstants
from garuda.lib import PathParser
from garuda.models import GARequest, GAResponse, GAError
from garuda.models.abstracts import CommunicationChannel
from garuda.config import GAConfig


class RESTCommunicationChannel(CommunicationChannel):
    """

    """
    def __init__(self, controller, **kwargs):
        """
        """
        self._uuid = uuid4().hex
        self._is_running = False
        self.controller = controller
        self.app = Flask(self.__class__.__name__)

        self.app.add_url_rule('/favicon.ico', 'favicon', self.favicon)
        self.app.add_url_rule('/vspkonly', 'vspk-only', self.vspkonly)
        self.app.add_url_rule('/<path:path>', 'vsd', self.index, methods=[RESTConstants.HTTP_GET, RESTConstants.HTTP_POST, RESTConstants.HTTP_PUT, RESTConstants.HTTP_DELETE, RESTConstants.HTTP_HEAD, RESTConstants.HTTP_OPTIONS])
        self.start_parameters = kwargs

    @property
    def uuid(self):
        """
        """
        return self._uuid

    @property
    def is_running(self):
        """
        """
        return self._is_running

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

    def _convert_content(self, content):
        """
        """

        if type(content) is list:
            results = []

            for obj in content:
                if hasattr(obj, 'to_dict'):
                    results.append(obj.to_dict())
                else:
                    results.append(str(content))

            return results

        if hasattr(content, 'to_dict'):
            return content.to_dict()

        return str(content)

    def make_channel_response(self, action, response):
        """
        """
        code = 520
        status = response.status
        content = self._convert_content(response.content)

        # Success
        if status == GAResponse.STATUS_SUCCESS:
            if action is GARequest.ACTION_CREATE:
                code = 201

            elif content is None or (type(content) is list and len(content) == 0):
                code = 204

            else:
                code = 200

        # Errors
        elif status == GAError.TYPE_INVALID:
            code = 400

        elif status == GAError.TYPE_NOTFOUND:
            code = 404

        elif status == GAError.TYPE_CONFLICT:
            code = 409

        elif status == GAError.TYPE_NOTALLOWED:
            code = 405

        response = make_response(json.dumps(content))
        response.status_code = code
        response.mimetype = 'application/json'

        return response

    def determine_action(self, method, resources):
        """
        """
        if method == RESTConstants.HTTP_POST:
            return GARequest.ACTION_CREATE

        elif method == RESTConstants.HTTP_PUT:
            return GARequest.ACTION_UPDATE

        elif method == RESTConstants.HTTP_DELETE:
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

        parser = PathParser()
        resources = parser.parse(path=path)

        action = self.determine_action(method, resources)

        ga_request = GARequest(action=action, content=content, parameters=parameters, resources=resources, channel=self.uuid)
        ga_response = self.controller.execute(request=ga_request)

        print '--- Response to %s ---' % parameters['Host']

        return self.make_channel_response(action=action, response=ga_response)

    def favicon(self):
        """
        """
        response = make_response()
        response.status_code = 200
        response.mimetype = 'application/json'

        return response

    def vspkonly(self):
        """
        """
        from vspk.vsdk.v3_2 import NUVSDSession, NUEnterprise
        session = NUVSDSession(username=GAConfig.VSD_USERNAME, password=GAConfig.VSD_PASSWORD, enterprise=GAConfig.VSD_ENTERPRISE, api_url=GAConfig.VSD_API_URL)
        session.start()

        enterprise = NUEnterprise(id='080a15cf-defb-4aec-af70-883ca69bfdea')
        domains = enterprise.domains.get()

        ga_response = GAResponse(status=GAResponse.STATUS_SUCCESS, content=domains)
        return self.make_channel_response(action='readall', response=ga_response)
