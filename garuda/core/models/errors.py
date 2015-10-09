# -*- coding: utf-8 -*-


class GAPropertyError(object):
    """

    """

    def __init__(self, type, property_name):
        """
        """
        self.type = type
        self.property_name = property_name
        self.errors = []

    def add_error(self, error):
        """
        """
        self.errors.append(error)

    def add_errors(self, errors):
        """
        """
        for error in errors:
            self.add_error(error)

    def to_dict(self):
        """
        """
        d = dict()

        d['property'] = self.property_name
        # d['type'] = self.type
        d['descriptions'] = [error.to_dict() for error in self.errors]  # descriptions to match VSD behavior

        return d


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
        # d['suggestion'] = self.suggestion

        return d


class GAErrorsList(list):
    """
    """
    def __init__(self):
        """
        """
        self.type = None

    def add_errors(self, errors):
        """

        """
        for error in errors:
            property_error = self._get_property_error(error.property_name)

            if property_error is None:
                self.type = error.type # that really sucks
                property_error = GAPropertyError(type=error.type, property_name=error.property_name)
                self.append(property_error)

            property_error.add_error(error)

    def add_error(self, error):
        """
        """
        self.add_errors([error])

    def merge(self, error_list):
        """
        """
        for perror in error_list:
            property_error = self._get_property_error(perror.property)

            if property_error is None:
                self.append(perror)
            else:
                property_error.add_errors(perror.errors)

    def _get_property_error(self, property_name):
        """
        """
        for error in self:
            if error.property_name == property_name:
                return error

        return None

    def has_errors(self):
        """
        """
        return self.type or len(self) > 0

    def clear(self):
        """
        """
        del self[:]
        self.type = None

    def to_dict(self):
        """
        """
        return [error.to_dict() for error in self]
