# -*- coding: utf-8 -*-

from uuid import uuid4


class GAResponse(object):
    """

    """
    def __init__(self, content):
        """
        """
        self.content = content

        self.status = None
        self.filter = None
        self.total_count = None
        self.order_by = None
        self.page = None
        self.page_size = None

        self._uuid = str(uuid4())

    @property
    def uuid(self):
        """
        """
        return self._uuid


class GAResponseSuccess(GAResponse):
    """
    """
    def __init__(self, content):
        """
        """
        super(GAResponseSuccess, self).__init__(content=content)


class GAResponseFailure(GAResponse):
    """
    """
    def __init__(self, content):
        """
        """
        super(GAResponseFailure, self).__init__(content=content)
