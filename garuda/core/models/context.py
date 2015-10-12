# -*- coding: utf-8 -*-

from copy import deepcopy

from .errors import GAErrorsList


class GAContext(object):
    """

    """

    def __init__(self, session, request):
        """
        """
        self.session = session
        self.request = request
        self.parent_object = None
        self.total_count = 0
        self.object = None
        self.objects = []
        self.user_info = {}

        self._errors_list = GAErrorsList()
        self._events = []

    @property
    def errors(self):
        """
        """
        return self._errors_list

    @property
    def events(self):
        """
        """
        return self._events

    def add_event(self, event):
        """
        """
        self._events.append(event)

    def copy(self):
        """
        """
        copy = GAContext(session=self.session, request=self.request)
        copy.parent_object = self.parent_object
        copy.object = self.object.copy()
        copy.objects = self.objects

        return copy

    def merge_contexts(self, contexts):
        """
        """
        for context in contexts:
            if context.has_errors():
                self._errors_list.merge(context._errors_list)

            # if context.object:
            self.user_info.update(content.user_info)

    def has_errors(self):
        """
        """
        return self._errors_list.has_errors()

    def report_errors(self, errors):
        """
        """
        self._errors_list.add_errors(errors)

    def report_error(self, error):
        """
        """
        self._errors_list.add_error(error)

    def clear_errors(self):
        """
        """
        self._errors.clear()
