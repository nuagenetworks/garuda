# -*- coding: utf-8 -*-

import json
import logging

logger = logging.getLogger('Garuda.RESTCommunicationChannel')

from base64 import urlsafe_b64decode

from copy import deepcopy
from Queue import Empty
from urlparse import urlparse
from uuid import uuid4

from flask import Flask, request, make_response

from .utils.constants import RESTConstants
from garuda.core.config import GAConfig
from garuda.core.lib import PathParser
from garuda.core.models import GARequest, GAResponse, GAError, GAPushNotification
from garuda.core.plugins import GACommunicationChannel


class RESTCommunicationChannel(GACommunicationChannel):
    """

    """
    def __init__(self, **kwargs):
        """
        """
        self._uuid = str(uuid4())
        self._is_running = False
        self._controller = None

        self.app = Flask(self.__class__.__name__)
        self.app.add_url_rule('/favicon.ico', 'favicon', self.favicon, methods=[RESTConstants.HTTP_GET])

        # Authentication
        self.app.add_url_rule('/me', 'authenticate', self.authenticate, methods=[RESTConstants.HTTP_GET], strict_slashes=False, defaults={'path': ''})
        self.app.add_url_rule('/<path:path>me', 'authenticate', self.authenticate, methods=[RESTConstants.HTTP_GET], strict_slashes=False)

        # Events
        self.app.add_url_rule('/events', 'listen_events', self.listen_events, methods=[RESTConstants.HTTP_GET], strict_slashes=False, defaults={'path': ''})
        self.app.add_url_rule('/<path:path>events', 'listen_events', self.listen_events, methods=[RESTConstants.HTTP_GET], strict_slashes=False)

        # Other requests
        self.app.add_url_rule('/<path:path>', 'vsd', self.index, methods=[RESTConstants.HTTP_GET, RESTConstants.HTTP_POST, RESTConstants.HTTP_PUT, RESTConstants.HTTP_DELETE, RESTConstants.HTTP_HEAD, RESTConstants.HTTP_OPTIONS], strict_slashes=False)
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

    @property
    def controller(self):
        """
        """
        return self._controller

    @controller.setter
    def controller(self, value):
        """
        """
        self._controller = value

    def channel_type(self):
        """
        """
        return CommunicationChannel.CHANNEL_TYPE_REST

    def start(self):
        """
        """
        if self.is_running:
            return

        self._is_running = True
        logger.debug('Channel starting')
        self.app.run(**self.start_parameters)

    def stop(self):
        """
        """
        if not self.is_running:
            return

        self._is_running = False

    def _extract_content(self, request):
        """

        """
        content = request.get_json(force=True, silent=True)
        if content:
            return deepcopy(content)

        return dict()

    def _extract_parameters(self, parameters):
        """
        """
        params = {}

        for p in parameters:
            params[p[0]] = p[1]

        if 'Authorization' in parameters:
            encoded_auth = parameters['Authorization'][6:]  # XREST stuff
            decoded_auth = urlsafe_b64decode(str(encoded_auth))
            auth = decoded_auth.split(':')
            params['username'] = auth[0]
            params['password'] = auth[1]

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

    def make_http_response(self, action, response):
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

        elif status == GAError.TYPE_UNAUTHORIZED:
            code = 401

        elif status == GAError.TYPE_AUTHENTICATIONFAILURE:
            code = 403

        elif status == GAError.TYPE_NOTFOUND:
            code = 404

        elif status == GAError.TYPE_NOTALLOWED:
            code = 405

        elif status == GAError.TYPE_CONFLICT:
            code = 409

        logger.debug(json.dumps(content, indent=4))

        response = make_response(json.dumps(content))
        response.status_code = code
        response.mimetype = 'application/json'

        return response

    def make_notification_response(self, notification):
        """
        """
        content = notification.to_dict()

        logger.debug(json.dumps(content, indent=4))

        response = make_response(json.dumps(content))
        response.status_code = 200
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

        content = self._extract_content(request)
        parameters = self._extract_parameters(request.headers)
        method = request.method.upper()

        logger.info('>>>> Request on %s %s from %s' % (request.method, request.path, parameters['Host']))
        logger.debug(json.dumps(parameters, indent=4))

        parser = PathParser()
        resources = parser.parse(path=path)

        action = self.determine_action(method, resources)

        ga_request = GARequest(action=action, content=content, parameters=parameters, resources=resources, channel=self)
        ga_response = self.core_controller.execute(request=ga_request)

        logger.info('<<<< Response for %s %s to %s' % (request.method, request.path, parameters['Host']))

        return self.make_http_response(action=action, response=ga_response)

    def favicon(self):
        """
        """
        logger.debug('Asking for favicon...')
        response = make_response()
        response.status_code = 200
        response.mimetype = 'application/json'

        return response

    def authenticate(self, path):
        """
        """
        content = self._extract_content(request)
        parameters = self._extract_parameters(request.headers)

        logger.info('>>>> Authenticate on %s %s from %s ---' % (request.method, request.path, parameters['Host']))
        logger.debug(json.dumps(parameters, indent=4))

        parser = PathParser()
        resources = parser.parse(path)
        action = GARequest.ACTION_AUTHENTICATE

        ga_request = GARequest(action=action, content=content, parameters=parameters, resources=resources, channel=self)
        ga_response = self.core_controller.execute_authenticate(request=ga_request)

        logger.info('<<<< Response for %s %s authentication to %s' % (request.method, request.path, parameters['Host']))

        return self.make_http_response(action=action, response=ga_response)

    def listen_events(self, path):
        """
        """
        content = self._extract_content(request)
        parameters = self._extract_parameters(request.headers)

        logger.info('>>>> Listening %s %s from %s' % (request.method, request.path, parameters['Host']))
        logger.debug(json.dumps(parameters, indent=4))

        ga_request = GARequest(action=GARequest.ACTION_LISTENEVENTS, content=content, parameters=parameters, channel=self)

        queue = self.core_controller.get_queue(request=ga_request)

        if queue is None:
            return self.make_http_response(action='FUCK', response=GAResponse(status='UNAUTHORIZED', content='Queue is None!'))

        try:
            events = queue.get(timeout=GAConfig.PUSH_TIMEOUT)
            ga_notification = GAPushNotification(events=events)
            logger.debug('Communication channel receive notification %s ' % ga_notification.to_dict())
            queue.task_done()
        except Empty:
            ga_notification = GAPushNotification()

        logger.info('<<<< Response for %s %s events to %s' % (request.method, request.path, parameters['Host']))

        return self.make_notification_response(notification=ga_notification)
