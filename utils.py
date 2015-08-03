# -*- coding: utf-8 -*-

from copy import deepcopy
from uuid import uuid4


class GASession(object):
    """

    """
    def __init__(self, resource=None, user=None, data={}, action=None):
        """

        """
        self.uuid = uuid4().hex
        self.resource = resource
        self.user = user
        self.data = data
        self.action = action


class GARequest(object):
    """

    """
    def __init__(self, method, url, data={}, headers={}, cookies=None):
        """
        """
        self.method = method
        self.url = url
        self.data = data
        self.headers = headers
        self.cookies = cookies

class GAResponse(object):
    """

    """
    def __init__(self, status, data, headers={}):
        """
        """
        self.status = status
        self.data = data
        self.headers = headers

class GAContext(object):
    """

    """
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_READ = 'read'
    ACTION_READALL = 'readall'

    def __init__(self, session, request):
        """
        """
        self._errors = []
        self.session = session
        self.request = request
        self.action = None
        self.parent_object = None
        self.object = None
        self.objects = []

    @property
    def errors(self):
        """
        """
        return self._errors

    def copy(self):
        """
        """
        return deepcopy(self)

    def merge_contexts(self, contexts):
        """
        """
        for context in contexts:
            if self.has_errors:
                self._errors += context.errors

            # TODO: Merge context object here...
            # Add the conflict in errors

            # Merge user_info

    def has_errors(self):
        """
        """
        return len(self._errors)

    def report_error(self, status, reason, suggestion=None):
        """
        """
        self._errors.append({'status': status, 'reason': reason, 'suggestion': suggestion})

    def clear_errrors(self):
        """
        """
        self._errors = []

class Resource(object):
    """
    """
    def __init__(self):
        """
        TEMPORARY OBJECT
        """
        self.rest_name = 'subnet'

from urlparse import urlparse
from parser import PathParser


class URLParser(object):
    """
    """

    def __init__(self, url):
        """
        """
        parse = urlparse(url)
        url_start = '/nuage/api/'

        path = parse.path
        if path.startswith(url_start):
            path = path[len(url_start):]

        if path.endswith('/'):
            path = path[:-1]

        index = path.index('/')

        self._version = path[:index]
        self._path = path[index + 1:]

        parser = PathParser()

        self._resources = parser.parse(self._path)

    @property
    def path(self):
        """
        """
        return self._path

    @property
    def version(self):
        """
        """
        return self._version

    @property
    def resources(self):
        """
        """
        return self._resources