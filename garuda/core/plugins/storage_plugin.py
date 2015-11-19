# -*- coding: utf-8 -*-

from garuda.core.models import GAPlugin

class GAStoragePlugin(GAPlugin):
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

    def count(self, user_identifier, parent, resource_name, filter=None):
        """
        """
        raise NotImplementedError("%s must implement count method" % self)

    def get(self, user_identifier, resource_name, identifier=None, filter=None):
        """
        """
        raise NotImplementedError("%s must implement get method" % self)

    def get_all(self, user_identifier, parent, resource_name, page=None, page_size=None, filter=None, order_by=None):
        """
        """
        raise NotImplementedError("%s must implement get_all method" % self)

    def create(self, user_identifier, resource, parent=None):
        """
        """
        raise NotImplementedError("%s must implement create method" % self)

    def update(self, user_identifier, resource):
        """
        """
        raise NotImplementedError("%s must implement update method" % self)

    def delete(self, user_identifier, resource):
        """
        """
        raise NotImplementedError("%s must implement delete method" % self)

    def delete_multiple(self, user_identifier, resources):
        """
        """
        raise NotImplementedError("%s must implement delete_multiple method" % self)

    def assign(self, user_identifier, resource_name, resources, parent):
        """
        """
        raise NotImplementedError("%s must implement assign method" % self)
