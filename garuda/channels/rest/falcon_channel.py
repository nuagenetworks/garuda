# -*- coding: utf-8 -*-

import json
import logging
import falcon
import time
import multiprocessing
from gunicorn.app.base import BaseApplication
from base64 import urlsafe_b64decode

from garuda.core.lib import GASDKLibrary
from garuda.core.models import GAError, GAPluginManifest, GAPushNotification, GARequest, GAResponseSuccess
from garuda.core.channels import GAChannel

from .constants import RESTConstants
from .parser import GAPathParser

logger = logging.getLogger('garuda.comm.rest')


class GAFalconChannel(GAChannel):  # pragma: no cover
    """
    """

    def __init__(self, ssl_certificate='', ssl_key='', host='0.0.0.0', port=2000, push_timeout=60):
        """
        """
        super(GAFalconChannel, self).__init__()

        self._host = host
        self._port = port
        self._push_timeout = push_timeout
        self._number_of_workers = (multiprocessing.cpu_count() * 2) + 1
        self._falcon = falcon.API()
        self._falcon.add_sink(self._handle_requests)
        self._server = GAGUnicorn(app=self._falcon,
                                  host=self._host,
                                  port=self._port,
                                  ssl_certificate=ssl_certificate,
                                  ssl_key=ssl_key,
                                  number_of_workers=self._number_of_workers,
                                  timeout=push_timeout + 20,
                                  worker_init=self._worker_init,
                                  worker_exit=self._worker_exit)

    def _worker_init(self, worker):
        """
        """
        self.core_controller.start()

    def _worker_exit(self, worker):
        """
        """
        self.core_controller.stop()

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='rest.falcon', version=1.0, identifier="garuda.communicationchannels.rest.falcon")

    def run(self):
        """
        """
        self._api_prefix = GASDKLibrary().get_sdk('default').SDKInfo.api_prefix()

        logger.info("Listening to inbound connection on %s:%d" % (self._host, self._port))

        logger.info("Starting gunicorn with %s workers" % self._number_of_workers)

        try:
            self._server.run()
        except:
            pass

    def _handle_requests(self, http_request, http_response):
        """
        """
        parser = GAPathParser()
        parser.parse(path=http_request.path, url_prefix="%s/" % self._api_prefix)

        if parser.resources[0].name == 'event':
            self._handle_event_request(http_request, http_response)
        else:
            self._handle_model_request(http_request, http_response)

    def _handle_model_request(self, http_request, http_response):
        """
        """
        method = http_request.method.upper()

        if method == RESTConstants.HTTP_OPTIONS:
            self._update_options_response(http_response=http_response)
            return

        parameters = http_request.params
        content = self._extract_content(http_request)
        username, token = self._extract_auth(http_request.headers)
        filter = self._extract_filter(http_request.headers)
        page, page_size = self._extract_paging(http_request.headers)
        order_by = self._extract_ordering(http_request.headers)

        logger.debug('> %s %s from %s' % (http_request.method, http_request.path, http_request.host))
        # logger.debug(json.dumps(content, indent=4))

        parser = GAPathParser()
        resources = parser.parse(path=http_request.path, url_prefix="%s/" % self._api_prefix)
        action = self._determine_action(http_request.method, resources)

        ga_request = GARequest(action=action,
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

        logger.debug('< %s %s to %s' % (http_request.method, http_request.path, http_request.host))
        # logger.debug(json.dumps(content, indent=4))

        self._update_http_response(http_response=http_response, action=action, ga_response=ga_response)

    def _handle_event_request(self, http_request, http_response):
        """
        """
        method = http_request.method.upper()

        if method == RESTConstants.HTTP_OPTIONS:
            self._update_options_response(http_response=http_response)
            return

        content = self._extract_content(http_request)
        parameters = http_request.params
        username, token = self._extract_auth(http_request.headers)

        logger.info('= %s %s from %s' % (http_request.method, http_request.path, http_request.host))

        ga_request = GARequest(action=GARequest.ACTION_LISTENEVENTS,
                               content=content,
                               parameters=parameters,
                               username=username,
                               token=token,
                               channel=self)

        session, ga_response_failure = self.core_controller.execute_events_request(request=ga_request)

        if ga_response_failure:
            self._update_http_response(http_response=http_response, action=GARequest.ACTION_READ, ga_response=ga_response_failure)
            return

        self.core_controller.sessions_controller.set_session_listening_status(session=session, status=True)

        events = []
        # event = self.core_controller.push_controller.get_next_event(session=session, timeout=self._push_timeout)
        # events.append(event)
        while True:

            event = self.core_controller.push_controller.get_next_event(session=session, timeout=self._push_timeout)

            # timeout expired and nothing to pop
            if not event:
                break

            events.append(event)

            if len(events) >= 100:
                break

            if self.core_controller.push_controller.is_event_queue_empty(session=session):

                time.sleep(0.3)

                # if this is still empty, we send back the info
                if self.core_controller.push_controller.is_event_queue_empty(session=session):
                    break

        ga_notification = GAPushNotification(events=events)
        logger.info('< %s %s events to %s' % (http_request.method, http_request.path, http_request.host))
        self._update_events_response(http_response=http_response, ga_notification=ga_notification)

        self.core_controller.sessions_controller.set_session_listening_status(session=session, status=False)

    def _determine_action(self, method, resources):
        """
        """
        method = method.upper()

        if method == RESTConstants.HTTP_POST:
            return GARequest.ACTION_CREATE
        elif method == RESTConstants.HTTP_PUT:
            return GARequest.ACTION_ASSIGN if len(resources) == 2 else GARequest.ACTION_UPDATE
        elif method == RESTConstants.HTTP_DELETE:
            return GARequest.ACTION_DELETE
        elif method == RESTConstants.HTTP_HEAD:
            return GARequest.ACTION_COUNT
        elif method == RESTConstants.HTTP_GET:
            return GARequest.ACTION_READALL if not resources[-1].value else GARequest.ACTION_READ

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

        # logger.debug(json.dumps(content, indent=4))

        http_response.body = json.dumps(content)
        http_response.status = code
        http_response.content_type = 'application/json'

        self._set_cors_headers(http_response=http_response)

        if ga_response.total_count is not None:
            http_response.set_header('X-Nuage-Count', str(ga_response.total_count))

        if ga_response.page is not None:
            http_response.set_header('X-Nuage-Page', str(ga_response.page))
        else:
            http_response.set_header('X-Nuage-Page', str(-1))

        if ga_response.page_size is not None:
            http_response.set_header('X-Nuage-PageSize', str(ga_response.page_size))

        http_response.set_header('X-Nuage-OrderBy', 'name ASC')

    def _update_events_response(self, http_response, ga_notification):
        """
        """
        content = ga_notification.to_dict()

        # logger.debug(json.dumps(content, indent=4))

        http_response.body = json.dumps(content)
        http_response.status = falcon.HTTP_200
        http_response.content_type = 'application/json'

        self._set_cors_headers(http_response=http_response)

    def _update_options_response(self, http_response):
        """
        """
        http_response.status = falcon.HTTP_200
        self._set_cors_headers(http_response=http_response)

    def _set_cors_headers(self, http_response):
        """
        """
        http_response.set_header('Access-Control-Allow-Origin', '*')
        http_response.set_header('Access-Control-Expose-Headers', 'X-Requested-With, X-Nuage-Organization, X-Nuage-Count, X-Nuage-Page, X-Nuage-PageSize, X-Nuage-OrderBy, X-Nuage-Filter, X-Nuage-FilterType')
        http_response.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, HEAD, OPTIONS')
        http_response.set_header('Access-Control-Allow-Headers', 'Authorization, Content-Type, Cache-Control, If-Modified-Since, X-Requested-With, X-Nuage-Organization, X-Nuage-Count, X-Nuage-Page, X-Nuage-PageSize, X-Nuage-OrderBy, X-Nuage-Filter, X-Nuage-FilterType')
        http_response.set_header('Access-Control-Allow-Credentials', 'true')


class GAGUnicorn(BaseApplication):  # pragma: no cover

    def __init__(self, app, host, port, ssl_certificate, ssl_key, number_of_workers, timeout, worker_init, worker_exit):
        """
        """
        self._app = app
        self._host = host
        self._port = port
        self._ssl_certificate = ssl_certificate
        self._ssl_key = ssl_key
        self._timeout = timeout
        self._worker_init = worker_init
        self._worker_exit = worker_exit
        self._number_of_workers = number_of_workers
        super(GAGUnicorn, self).__init__()

    def load_config(self):
        """
        """
        self.cfg.set('bind', '%s:%s' % (self._host, self._port))
        self.cfg.set('workers', self._number_of_workers)
        self.cfg.set('worker_class', 'gevent')
        self.cfg.set('timeout', self._timeout)
        self.cfg.set('max_requests', 5000)
        self.cfg.set('proc_name', 'garuda-worker')
        self.cfg.set('reload', False)
        self.cfg.set('loglevel', 'warning')

        if self._ssl_certificate and self._ssl_key:
            self.cfg.set('keyfile', self._ssl_key)
            self.cfg.set('certfile', self._ssl_certificate)

        def post_worker_init(worker):
            self._worker_init(worker)

        def worker_exit(server, worker):
            self._worker_exit(worker)

        self.cfg.set('post_worker_init', post_worker_init)
        self.cfg.set('worker_exit', worker_exit)

    def load(self):
        """
        """
        return self._app
