# -*- coding: utf-8 -*-

from .request import GARequest
from .response import GAResponseSuccess, GAResponseFailure


class GAContext(object):
    """

    """
    def __init__(self, session, request):
        """
        """
        self.object = None
        self.objects = []
        self.parent_object = None
        self.request = request
        self.session = session
        self.total_count = 0

        self.user_info = {}
        self._errors = []
        self._events = []

    # Properties

    @property
    def errors(self):
        """
        """
        return self._errors

    @property
    def events(self):
        """
        """
        return self._events

    # Utilities

    def copy(self):
        """
        """
        copy = GAContext(session=self.session, request=self.request)
        copy.parent_object = self.parent_object
        copy.object = self.object.copy() if self.object else None
        copy.objects = self.objects

        return copy

    def merge_contexts(self, contexts):
        """
        """
        for context in contexts:

            if context.has_errors():
                self.add_errors(context.errors)

            if context.has_events():
                self.add_events(context.events)

            # this is not a merge! this is stupid, but this is better that nothing
            # at least it works when you use a single plugin
            if context.object:
                self.object = context.object

            if context.objects:
                self.objects = context.objects

            self.user_info.update(context.user_info)

    # Event management

    def add_events(self, events):
        """
        """
        self._events += events

    def add_event(self, event):
        """
        """
        self._events.append(event)

    def has_events(self):
        """
        """
        return len(self._events) > 0

    # Errors management

    def add_errors(self, errors):
        """
        """
        self._errors += errors

    def add_error(self, error):
        """
        """
        self._errors.append(error)

    def has_errors(self):
        """
        """
        return len(self._errors) > 0

    def clear_errors(self):
        """
        """
        self._errors = []


    # Response management

    def make_response(self):
        """
        """
        if self.has_errors():
            return GAResponseFailure(content=self.errors)

        response = None

        if self.request.action is GARequest.ACTION_READALL:
            response = GAResponseSuccess(content=self.objects)
        else:
            response = GAResponseSuccess(content=self.object)

        response.total_count = self.total_count
        response.page = self.request.page
        response.page_size = self.request.page_size

        return response
