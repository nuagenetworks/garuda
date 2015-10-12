# -*- coding: utf-8 -*-

from uuid import uuid4


class GAResponse(object):
    """

    """
    def __init__(self, content, status=None):
        """
        """
        self._uuid = str(uuid4())
        self.status = status
        self.content = content

    @property
    def uuid(self):
        """
        """
        return self._uuid


class GAResponseSuccess(GAResponse):
    """
    """
    def __init__(self, content, parameters={}):
        """
        """
        super(GAResponseSuccess, self).__init__(content=content)


class GAResponseFailure(GAResponse):
    """
    """
    def __init__(self, content, parameters={}):
        """
        """
        super(GAResponseFailure, self).__init__(content=content)
