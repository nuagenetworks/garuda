# -*- coding: utf-8 -*-


class GAError(object):
    """
    """
    TYPE_INVALID = 'invalid'
    TYPE_NOTFOUND = 'not found'
    TYPE_CONFLICT = 'conflict'
    TYPE_UNKNOWN = 'unknown'
    TYPE_NOTALLOWED = 'not allowed'
    TYPE_AUTHENTICATIONFAILURE = 'authentication failed'
    TYPE_UNAUTHORIZED = 'unauthorized'

    def __init__(self, type, title, description, suggestion=None, property_name=''):
        """
        """
        self.type = type
        self.title = title
        self.description = description
        self.suggestion = suggestion
        self.property_name = property_name

    def to_dict(self):
        """
        """
        d = dict()

        d['title'] = self.title
        d['description'] = self.description

        return d
