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
        raise NotImplementedErrorError("%s should implement instantiate method" % self)

    def count(self, parent, resource_name, filter=None):
        """
        """
        raise NotImplementedErrorError("%s must implement count method" % self)

    def get(self, resource_name, identifier=None, filter=None):
        """
        """
        raise NotImplementedErrorError("%s must implement get method" % self)

    def get_all(self, parent, resource_name, page=None, page_size=None, filter=None, order_by=None):
        """
        """
        raise NotImplementedErrorError("%s must implement get_all method" % self)

    def create(self, resource, parent=None, user_identifier=None):
        """
        """
        raise NotImplementedErrorError("%s must implement create method" % self)

    def update(self, resource, user_identifier=None):
        """
        """
        raise NotImplementedErrorError("%s must implement update method" % self)

    def delete(self, resource, cascade=True, user_identifier=None):
        """
        """
        raise NotImplementedErrorError("%s must implement delete method" % self)

    def delete_multiple(self, resources, cascade=True, user_identifier=None):
        """
        """
        raise NotImplementedErrorError("%s must implement delete_multiple method" % self)

    def assign(self, resource_name, resources, parent, user_identifier=None):
        """
        """
        raise NotImplementedErrorError("%s must implement assign method" % self)
