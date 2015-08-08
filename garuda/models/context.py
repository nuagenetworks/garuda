# -*- coding: utf-8 -*-

from copy import deepcopy


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

        error['descriptions'].append({u'title': title, u'description': description, u'suggestion': suggestion})

    def clear_errors(self):
        """
        """
        self._errors = []
