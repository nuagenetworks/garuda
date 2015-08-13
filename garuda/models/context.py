# -*- coding: utf-8 -*-

from copy import deepcopy

from .errors import GAErrorsList


class GAContext(object):
    """

    """

    def __init__(self, session, request):
        """
        """
        self._errors_list = GAErrorsList()
        self.session = session
        self.request = request
        self.parent_object = None
        self.object = None
        self.objects = []

    @property
    def errors(self):
        """
        """
        return self._errors_list

    def copy(self):
        """
        """
        copy = GAContext(session=self.session, request=self.request)
        copy._errors_list = GAErrorsList()  # Don't need to forward errors no ?

        if self.parent_object:
            copy.parent_object = self.parent_object.copy()

        if self.object:
            copy.object = self.object.copy()

        if self.objects:
            copy.objects = [obj.copy() for obj in self.objects]

        return copy

    def merge_contexts(self, contexts):
        """
        """
        for context in contexts:
            if context.has_errors():
                self._errors_list.merge(context._errors_list)

            # TODO: Merge context object here...
            # Add the conflict in errors

            # Merge user_info

    def has_errors(self):
        """
        """
        return self._errors_list.has_errors()


    def report_error(self, type, property, title, description, suggestion=None):
        """
        """
        self._errors_list.add_error(type=type, property=property, title=title, description=description, suggestion=suggestion)

    def clear_errors(self):
        """
        """
        self._errors.clear()
