# -*- coding: utf-8 -*-

from .abstracts import GAPlugin


class GAModelControllerPlugin(GAPlugin):
    """
    """

    def should_manage(self, resource_name, identifier):
        """
        """
        return True

    def instantiate(self, resource_name):
        """
        """
        raise NotImplementedError("%s should implement instantiate method" % self)

    def get(self, resource_name, identifier):
        """
        """
        raise NotImplementedError("%s should implement get method" % self)

    def get_all(self, parent, resource_name):
        """
        """
        raise NotImplementedError("%s should implement get_all method" % self)

    def save(self, resource, parent=None):
        """
        """
        raise NotImplementedError("%s should implement save method" % self)

    def delete(self, resource):
        """
        """
        raise NotImplementedError("%s should implement delete method" % self)
