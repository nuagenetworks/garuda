# -*- coding: utf-8 -*-

import os
import json
import logging
import falcon
import multiprocessing
from gunicorn.app.base import BaseApplication
from base64 import urlsafe_b64decode

from garuda.core.lib import SDKLibrary
from garuda.core.models import GAError, GAPluginManifest, GAPushNotification, GARequest, GAResponseFailure, GAResponseSuccess
from garuda.core.channels import GAChannel

from .constants import RESTConstants
from .parser import PathParser

logger = logging.getLogger('garuda.comm.rest')


class GAFalconChannel(GAChannel):
    """
    """

    def __init__(self, host='0.0.0.0', port=2000, push_timeout=60):
        """
        """
        super(GAFalconChannel, self).__init__()

        self._host = host
        self._port = port
        self._push_timeout = push_timeout
        self._number_of_workers = (multiprocessing.cpu_count() * 2) + 1

        self._falcon = falcon.API()
        self._falcon.add_sink(self._handle_requests)
        self._server = GAGUnicorn(app=self._falcon, host=self._host, port=self._port, number_of_workers=self._number_of_workers)

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='rest.falcon', version=1.0, identifier="garuda.communicationchannels.rest.falcon")

    def internal_thread_management(self):
        """
        """
        return True

    def start(self):
        """
        """
        logger.info("Communication listening to %s:%d" % (self._host, self._port))

        self._api_prefix = SDKLibrary().get_sdk('default').SDKInfo.api_prefix()

        logger.info("Starting gunicorn with %s workers" % self._number_of_workers)
        self._server.run()

    def stop(self):
        """
        """
        self._server.shutdown()

    def _handle_requests(self, http_request, http_response):
        """
        """
        parser = PathParser()
        parser.parse(path=http_request.path, url_prefix="%s/" % self._api_prefix)

        if parser.resources[0].name == 'event':
            self._handle_events_request(http_request, http_response)
        else:
            self._handle_model_request(http_request, http_response)

    def _handle_model_request(self, http_request, http_response):
        """
        """
        content         = self._extract_content(http_request)
        username, token = self._extract_auth(http_request.headers)
        filter          = self._extract_filter(http_request.headers)
        page, page_size = self._extract_paging(http_request.headers)
        order_by        = self._extract_ordering(http_request.headers)

        method          = http_request.method.upper()
        parameters      = http_request.params

        logger.info('> %s %s from %s' % (http_request.method, http_request.path, http_request.host))
        logger.debug(json.dumps(content, indent=4))

        parser = PathParser()
        resources = parser.parse(path=http_request.path, url_prefix="%s/" % self._api_prefix)

        action = self._determine_action(method, resources)

        ga_request = GARequest( action=action,
                                content=content,
                                parameters=parameters,
                                resources=resources,
                                username=username,
                                token=token,
                                filter=filter,
                                page=page,
                                page_size=page_size,
                                order_by=order_by,
                                channel=self)

        ga_response = self.core_controller.execute_model_request(request=ga_request)

        logger.info('< %s %s to %s' % (http_request.method, http_request.path, http_request.host))
        logger.debug(json.dumps(content, indent=4))

        self._update_http_response(http_response=http_response, action=action, ga_response=ga_response)

    def _handle_events_request(self, http_request, http_response):
        """
        """
        content = self._extract_content(http_request)
        parameters = http_request.params
        username, token = self._extract_auth(http_request.headers)

        logger.info('= %s %s from %s' % (http_request.method, http_request.path, http_request.host))

        ga_request = GARequest( action=GARequest.ACTION_LISTENEVENTS,
                                content=content,
                                parameters=parameters,
                                username=username,
                                token=token,
                                channel=self)

        session_uuid, ga_response_failure = self.core_controller.execute_events_request(request=ga_request)

        if ga_response_failure:
            self._update_http_response(http_response=http_response, action=GARequest.ACTION_READ, ga_response=ga_response_failure)
            return

        events = []

        for event in self.core_controller.push_controller.get_next_event(session_uuid=session_uuid):
            events.append(event)

        ga_notification = GAPushNotification(events=events)
        logger.info('< %s %s events to %s' % (http_request.method, http_request.path, http_request.host))
        self._update_events_response(http_response=http_response, ga_notification=ga_notification)

    def _determine_action(self, method, resources):
        """
        """
        if method == RESTConstants.HTTP_POST: return GARequest.ACTION_CREATE
        elif method == RESTConstants.HTTP_PUT: return GARequest.ACTION_ASSIGN if len(resources) == 2 else GARequest.ACTION_UPDATE
        elif method == RESTConstants.HTTP_DELETE: return GARequest.ACTION_DELETE
        elif method == RESTConstants.HTTP_HEAD: return GARequest.ACTION_COUNT
        elif method == RESTConstants.HTTP_GET: return GARequest.ACTION_READALL if not resources[-1].value else GARequest.ACTION_READ

        raise Exception("Unknown method %s" % method)

    def _extract_content(self, request):
        """

        """
        if not request.content_length:
            return {}

        return json.loads(request.stream.read())

        # we should raise a malformed query here

    def _extract_auth(self, headers):
        """
        """
        username = None
        token = None

        if 'AUTHORIZATION' in headers:
            encoded_auth = headers['AUTHORIZATION'][6:]  # XREST stuff
            decoded_auth = urlsafe_b64decode(str(encoded_auth))
            auth = decoded_auth.split(':')
            username = auth[0]
            token = auth[1]

        return username, token

    def _extract_filter(self, headers):
        """
        """
        if 'X-NUAGE-FILTER' in headers:
            return headers['X-NUAGE-FILTER']

        return None

    def _extract_paging(self, headers):
        """
        """
        page = None
        page_size = 500

        if 'X-NUAGE-PAGE' in headers:
            page = headers['X-NUAGE-PAGE']

        if 'X-NUAGE-PAGESIZE' in headers:
            page_size = headers['X-NUAGE-PAGESIZE']

        return page, page_size

    def _extract_ordering(self, headers):
        """
        """
        if 'X-NUAGE-ORDERBY' in headers:
            return headers['X-NUAGE-ORDERBY']

    def _convert_errors(self, action, response):
        """
        """
        properties = {}
        error_type = response.content[0].type if len(response.content) > 0 else None

        for error in response.content:
            if error.property_name not in properties:
                properties[error.property_name] = {
                    "property": error.property_name,
                    "type": error.type,
                    "descriptions": []}

            properties[error.property_name]["descriptions"].append(error.to_dict())

        if error_type == GAError.TYPE_INVALID:
            code = falcon.HTTP_400

        elif error_type == GAError.TYPE_UNAUTHORIZED:
            code = falcon.HTTP_401

        elif error_type == GAError.TYPE_AUTHENTICATIONFAILURE:
            code = falcon.HTTP_403

        elif error_type == GAError.TYPE_NOTFOUND:
            code = falcon.HTTP_404

        elif error_type == GAError.TYPE_NOTALLOWED:
            code = falcon.HTTP_405

        elif error_type == GAError.TYPE_CONFLICT:
            code = falcon.HTTP_409

        else:
            code = falcon.HTTP_520

        return (code, {"errors": properties.values()})

    def _convert_content(self, action, response):
        """
        """
        if type(response.content) is list:
            content = [obj.to_dict() for obj in response.content]

        elif hasattr(response.content, 'to_dict'):
            content = [response.content.to_dict()]

        else:
            content = str(response.content)

        if action is GARequest.ACTION_CREATE:
            code = falcon.HTTP_201

        elif content is None:
            code = falcon.HTTP_204

        else:
            code = falcon.HTTP_200

        return (code, content)

    def _update_http_response(self, http_response, action, ga_response):
        """
        """
        if isinstance(ga_response, GAResponseSuccess):
            code, content = self._convert_content(action, ga_response)

        else:
            code, content = self._convert_errors(action, ga_response)

        logger.debug(json.dumps(content, indent=4))

        http_response.body = json.dumps(content)
        http_response.status = code
        http_response.content_type = 'application/json'

        if ga_response.total_count is not None:
            http_response.set_header('X-Nuage-Count', str(ga_response.total_count))

        if ga_response.page is not None:
            http_response.set_header('X-Nuage-Page', str(ga_response.page))
        else:
            http_response.set_header('X-Nuage-Page', str(-1))

        if ga_response.page_size is not None:
            http_response.set_header('X-Nuage-PageSize', str(ga_response.page_size))

    def _update_events_response(self, http_response, ga_notification):
        """
        """
        content = ga_notification.to_dict()

        logger.debug(json.dumps(content, indent=4))

        http_response.body = json.dumps(content)
        http_response.status = falcon.HTTP_200
        http_response.content_type = 'application/json'


class GAGUnicorn(BaseApplication):

    def __init__(self, app, host, port, number_of_workers):
        """
        """
        self._app = app
        self._host = host
        self._port = port
        self._number_of_workers = number_of_workers
        super(GAGUnicorn, self).__init__()

    def load_config(self):
        """
        """
        self.cfg.set('bind', '%s:%s' % (self._host, self._port))
        self.cfg.set('workers', self._number_of_workers)
        self.cfg.set('worker_class', 'eventlet')

    def load(self):
        """
        """
        return self._app
