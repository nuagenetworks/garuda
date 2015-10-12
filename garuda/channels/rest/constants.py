# -*- coding: utf-8 -*-


class RESTConstants(object):
    """

    """
    HTTP_GET = 'GET'
    HTTP_PATCH = 'PATCH'
    HTTP_POST = 'POST'
    HTTP_PUT = 'PUT'
    HTTP_DELETE = 'DELETE'
    HTTP_HEAD = 'HEAD'
    HTTP_OPTIONS = 'OPTIONS'

    @classmethod
    def all_methods(cls):
        """
        """
        return [HTTP_GET, HTTP_PATCH, HTTP_POST, HTTP_PUT, HTTP_DELETE, HTTP_HEAD, HTTP_OPTIONS]