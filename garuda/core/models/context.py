# -*- coding: utf-8 -*-


class GAContext(object):
    """

    """
    def __init__(self, session=None, request=None):
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
        copy.object = self.object.copy()
        copy.objects = self.objects

        return copy

    def merge_contexts(self, contexts):
        """
        """
        for context in contexts:
            if context.has_errors():
                self.report_errors(context.errors)

            # if context.object:
            self.user_info.update(context.user_info)

    # Event management

    def add_event(self, event):
        """
        """
        self._events.append(event)

    # Errors management

    def has_errors(self):
        """
        """
        return len(self._errors) > 0

    def report_errors(self, errors):
        """
        """
        self._errors += errors

    def report_error(self, error):
        """
        """
        self._errors.append(error)

    def clear_errors(self):
        """
        """
        self._errors = []
