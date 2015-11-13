# -*- coding: utf-8 -*

from .errors import GAError


class GAStoragePluginQueryResponse(object):
    """
    """

    def __init__(self, data=None, count=None, errors=None):
        """
        """
        self._data = data
        self._errors = errors
        self._count = count

    @classmethod
    def init_with_error(cls, error_type, title, description):
        """
        """
        return GAStoragePluginQueryResponse(errors=[GAError(type=error_type, title=title, description=description)])

    @classmethod
    def init_with_errors(cls, errors):
        """
        """
        r = GAStoragePluginQueryResponse(errors=errors)
        return r

    @classmethod
    def init_with_data(cls, data, count=None):
        """
        """
        return cls(data=data, count=count)

    @property
    def data(self):
        """
        """
        return self._data

    @property
    def errors(self):
        """
        """
        return self._errors

    @property
    def count(self):
        """
        """
        return self._count

    @property
    def has_errors(self):
        """
        """
        if not self._errors:
            return False

        return len(self._errors) > 0
