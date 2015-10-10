# -*- coding: utf-8 -*-

import json
import logging

logger = logging.getLogger('garuda.comm.rest')

from base64 import urlsafe_b64decode

from copy import deepcopy
from Queue import Empty
from urlparse import urlparse
from uuid import uuid4

from flask import Flask, request, make_response

from .constants import RESTConstants

from garuda.core.config import GAConfig
from garuda.core.lib import PathParser, SDKsManager
from garuda.core.models import GARequest, GAResponse, GAError, GAErrorsList, GAPushNotification
from garuda.core.plugins import GAPluginManifest
from garuda.core.channels import GAChannel


class GARESTChannel(GAChannel):
    """

    """

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='ReST Communication Channel', version=1.0, identifier="garuda.communicationchannels.rest")

    def __init__(self, host='0.0.0.0', port=2000):
        """
        """
        # mute flask logging for now
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        self._uuid = str(uuid4())
        self._is_running = False
        self._controller = None
        self._host = host
        self._port = port

        self._flask = Flask(self.__class__.__name__)
        self._flask.add_url_rule('/favicon.ico', 'favicon', self.favicon, methods=[RESTConstants.HTTP_GET])

        # Events
        self._flask.add_url_rule('/events', 'listen_events', self.listen_events, methods=[RESTConstants.HTTP_GET], strict_slashes=False, defaults={'path': ''})
        self._flask.add_url_rule('/<path:path>events', 'listen_events', self.listen_events, methods=[RESTConstants.HTTP_GET], strict_slashes=False)

        # Other requests
        self._flask.add_url_rule('/<path:path>', 'vsd', self.index, methods=[RESTConstants.HTTP_GET, RESTConstants.HTTP_POST, RESTConstants.HTTP_PUT, RESTConstants.HTTP_DELETE, RESTConstants.HTTP_HEAD, RESTConstants.HTTP_OPTIONS], strict_slashes=False)

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

    def start(self):
        """
        """
        if self.is_running:
            return

        self._is_running = True

        logger.info("Communication channel listening on %s:%d" % (self._host, self._port))
        self._flask.run(host=self._host, port=self._port, threaded=True, debug=False, use_reloader=False)

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

        if type(content) is GAErrorsList:
            return {"errors": content.to_dict()}

        elif type(content) is list:
            return [obj.to_dict() for obj in content]

        elif hasattr(content, 'to_dict'):
            return [content.to_dict()]

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
            if len(resources) == 2: # this is a PUT /A/id/B, which means this is an membership relationship
                return GARequest.ACTION_ASSIGN
            else:
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

        logger.info('> %s %s from %s' % (request.method, request.path, parameters['Host']))
        logger.debug(json.dumps(parameters, indent=4))

        parser = PathParser()
        resources = parser.parse(path=path, url_prefix="%s/" % SDKsManager().get_sdk("current").SDKInfo.api_prefix())

        action = self.determine_action(method, resources)

        ga_request = GARequest(action=action, content=content, parameters=parameters, resources=resources, channel=self)
        ga_response = self.core_controller.execute(request=ga_request)

        logger.info('< %s %s to %s' % (request.method, request.path, parameters['Host']))

        return self.make_http_response(action=action, response=ga_response)

    def favicon(self):
        """
        """
        logger.debug('Asking for favicon...')
        response = make_response()
        response.status_code = 200
        response.mimetype = 'application/json'

        return response

    def listen_events(self, path):
        """
        """
        content = self._extract_content(request)
        parameters = self._extract_parameters(request.headers)

        logger.info('= %s %s from %s' % (request.method, request.path, parameters['Host']))
        logger.debug(json.dumps(parameters, indent=4))

        ga_request = GARequest(action=GARequest.ACTION_LISTENEVENTS, content=content, parameters=parameters, channel=self)

        queue = self.core_controller.get_queue(request=ga_request)

        if queue is None:
            return self.make_http_response(action='FUCK', response=GAResponse(status='UNAUTHORIZED', content='Queue is None!'))

        try:
            events = queue.get(timeout=GAConfig.PUSH_TIMEOUT)

            if events[0].action == self.core_controller.GARUDA_TERMINATE_EVENT:
                ga_notification = GAPushNotification()
            else:
                ga_notification = GAPushNotification(events=events)

            logger.debug('Communication channel receive notification %s ' % ga_notification.to_dict())
            queue.task_done()
        except Empty:
            ga_notification = GAPushNotification()

        logger.info('< %s %s events to %s' % (request.method, request.path, parameters['Host']))

        return self.make_notification_response(notification=ga_notification)
