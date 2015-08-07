# -*- coding: utf-8 -*-

from copy import deepcopy
from uuid import uuid4

from gaexceptions import NotFoundException


class GASession(object):
    """

    """

    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_READ = 'read'
    ACTION_READALL = 'readall'

    def __init__(self, user=None, data={}, resources=[], action=None):
        """

        """
        self.uuid = uuid4().hex
        self.user = user
        self.data = data
        self.action = action
        self.resources = resources


class GARequest(object):
    """

    """
    def __init__(self, action, url, data={}, resources=[], headers={}, cookies=None):
        """
        """
        self.action = action
        self.url = url
        self.data = data
        self.headers = headers
        self.cookies = cookies
        self.resources = resources


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

    def __init__(self, session, request):
        """
        """
        self._errors = []
        self.session = session
        self.request = request
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

    def _error_index(self, property):
        """
        """
        for index, error in enumerate(self._errors):
            if error['property'] is property:
                return index

        return -1

    def report_error(self, property, title, description, suggestion=None):
        """
        """
        index = self._error_index(property)

        if index < 0:
            error = {u'property': property, u'descriptions': []}
            self._errors.append(error)
        else:
            error = self._errors[index]

        error['descriptions'].append({u'title': title, u'description': description, u'suggestion':suggestion})

    def clear_errors(self):
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

