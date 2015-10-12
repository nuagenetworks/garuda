# -*- coding: utf-8 -*-

from uuid import uuid4


class GAResponse(object):
    """

    """
    def __init__(self, content, status=None, total_count=None, page=None, page_size=None, order_by=None, filter=None):
        """
        """
        self.status = status
        self.content = content
        self.filter = filter
        self.total_count = total_count
        self.order_by = order_by
        self.page = page
        self.page_size = page_size

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
