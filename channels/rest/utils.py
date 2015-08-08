# -*- coding: utf-8 -*-

import json

from werkzeug.exceptions import HTTPException


class GarudaHTTPException(HTTPException):
    """  """

    data = dict()

    def __init__(self, code, data):
        """ Initialize

        """
        super(GarudaHTTPException, self).__init__()
        self.code = code
        self.data = data

    def get_body(self, environ):
        """ Get the JSON body

        """
        return json.dumps(self.data)

    def get_headers(self, environ):
        """ Get a list of headers

        """
        return [('Content-Type', 'application/json'),
                ('Content-Length', len(self.get_body(environ))),
                ('Access-Control-Max-Age', '1')]
